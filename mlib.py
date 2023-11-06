import math
import pygame
import pyperclip
import os
import time

pygame.init()

#MLib version
VERSION = "2.3.1"

#Number of existing widget
_nbWidget = 0

class MObject:
    """Main MLib object class
    """

    nbObject = 0

    def __init__(self, app, objectType: str = "MObject") -> None:
        self._id = MObject.nbObject
        self._mapp = app
        self._type = objectType

        MObject.nbObject += 1

        if app != 0:
            app._declaringObject(self)

    def softResetObject(self):
        """Reset without graphics modification
        """
        pass

    def _lastUpdate(self, deltaTime: float):
        """Function usefull for heritage, call by MApp every frame after event handle and user program

        Args:
            deltaTime (float): time between the last frame and this frame
        """
        pass

    def _lateUpdate(self, deltaTime: float):
        """Function usefull for heritage, call by MApp every frame after event handle

        Args:
            deltaTime (float): time between the last frame and this frame
        """
        pass

    def _update(self, deltaTime: float):
        """Function usefull for heritage, call by MApp every frame

        Args:
            deltaTime (float): time between the last frame and this frame
        """
        pass

class MWidget(MObject):
    """Base widget class, herit from MObject
    """

    def __init__(self, x: float, y: float, width: float, height: float, parent, widgetType: str = "MWidget") -> None:
        """MWidget's constructor

        Args:
            x (float): x pos of the widget
            y (float): y pos of the widget
            width (float): width of the widget
            height (float): height of the widget
            parent (MWidget): parent widget of the widget
            widgetType (str, optional): type of the widget. Defaults to "MWidget".
        """
        super().__init__(0, widgetType)
        self.backgroundColor = (255, 255, 255)
        self.cursorOnOverflight = pygame.SYSTEM_CURSOR_ARROW
        self.focused = False
        self.height = height
        self.ignoreUserEvent = False
        self.mouseDown = []
        self.mouseUp = []
        self.overflighted = False
        self.parent = 0
        self.setShouldModify(True)
        self.visible = True
        self.width = width
        self.x = x
        self.y = y
        self._BACKGROUNDCOLOR = self.backgroundColor
        self._children = []
        self._isMovingAtThisFrame = False
        self._isResizedAtThisFrame = False
        self._lastSurface = 0

        if parent != 0:
            self.setParent(parent)

        if self._type != "MApp": #Register the widget into the MApp object
            self.parent._declaringWidget(self)
        
            if self._mapp.getConsole():
                self._mapp.writeConsole("New MWidget object", indentation=0, writer=self)

    def absolutePos(self): #Return the pos according to the MApp object
        return self.absoluteX(), self.absoluteY()
    
    def absoluteX(self): #Return x according to the MApp object
        if self._type == "MApp":
            return 0
        else:
            x = self.getX()
            x += self.parent.absoluteX()
            return x
        
    def absoluteY(self): #Return y according to the MApp object
        if self._type == "MApp":
            return 0
        else:
            y = self.getY()
            y += self.parent.absoluteY()
            return y

    def containsChild(self, id): #Return if the widget contains the child with the id
        for i1, i2 in enumerate(self._children): #Search through all the children to find the one with the good id
            if i2.getID() == id:
                return i1
        return -1
    
    def delete(self): #Delete a widget from the mlib ecosystem
        self._mapp._undeclaringWidget(self)
        self.getParent()._removeChild(self)

    def getBackgroundColor(self): #Return the value of backgroundColor
        return self.backgroundColor
    
    def getChildren(self): #Report the list of all the children of the widget
        return self._children
    
    def getChildrenAtIndex(self, index): #Report the widget at the index "index" in the list _children
        return self._children[index]
    
    def getCursorOnOverflight(self): #Return the value of cursorOnOverflight
        return self.cursorOnOverflight
    
    def getFocused(self): #Return the value of focused
        return self.focused

    def getHeight(self): #Return the value of height
        return self.height
    
    def getIgnoreUserEvent(self): #Return ignoreUserEvent
        return self.ignoreUserEvent

    def getID(self): #Return the value of _id
        return self._id
    
    def getMouseDown(self): #Return the value of mouseDown
        return self.mouseDown
    
    def getMouseUp(self): #Return the value of mouseUp
        return self.mouseUp
    
    def getOverflighted(self): #Return if the widget is overflighted or not
        return self.overflighted

    def getParent(self): #Return the value of parent
        return self.parent
    
    def getRect(self): #Return (x, y, width, height)
        return (self.getX(), self.getY(), self.getWidth(), self.getHeight())
    
    def getShouldModify(self): #Return the value of should modify
        return self.shouldModify
    
    def getVisible(self): #Return the value of visible
        return self.visible
    
    def getWidth(self): #Return the value of width
        return self.width
    
    def getX(self): #Return the value of X
        return self.x
    
    def getY(self): #Return the value of Y
        return self.y
    
    def isMoving(self): #Return _isMovingAtThisFrame
        return self._isMovingAtThisFrame

    def isResized(self): #Return _isResizeAtThisFrame
        return self._isResizedAtThisFrame

    def move(self, newX, newY): #Change the value of X and Y in one function
        self.setX(newX)
        self.setY(newY)

    def posIn(self, pos): #Check if "pos" is in the widget
        if pos[0] >= self.absoluteX() and pos[1] > self.absoluteY() and pos[0] < self.absoluteX() + self.getWidth() and pos[1] < self.absoluteY() + self.getHeight():
            return True
        return False
    
    def promoveChild(self, child): #Promove the rendering of a child
        self._removeChild(child)
        self._addChild(child)
    
    def resetWidget(self): #Reset the widget as its initial state (with no events)
        self.backgroundColor = self._BACKGROUNDCOLOR
        self.setShouldModify(True)

    def resize(self, newWidth, newHeight): #Change the value of width and height in one function
        self.setHeight(newHeight)
        self.setWidth(newWidth)

    def setBackgroundColor(self, backgroundColor, constant = True): #Change the value of backgroundColor
        if not (self.backgroundColor == self._BACKGROUNDCOLOR and self.backgroundColor == backgroundColor):
            self.backgroundColor = backgroundColor
            if constant:
                self._BACKGROUNDCOLOR = backgroundColor
            else:
                if self._type == "MApp":
                    self._addWidgetToReset(self)
                else:
                    self._mapp._addWidgetToReset(self)
            self.setShouldModify(True)

    def setCursorOnOverflight(self, cursorOnOverflight): #Return the value of cursorOnOverflight
        self.cursorOnOverflight = cursorOnOverflight
    
    def setHeight(self, newHeight): #Change the value of height
        if self.getHeight() != newHeight:
            self.height = newHeight
            self._isResizedAtThisFrame = True
            self.setShouldModify(True)

    def setIgnoreUserEvent(self, ignoreUserEvent): #Change the value of ignoreUserEvent
        self.ignoreUserEvent = ignoreUserEvent
    
    def setParent(self, newParent): #Change the value of parent
        if self.parent != 0:
            self.parent._removeChild(self)

        self.parent = newParent
        self.setShouldModify(True)

        newParent._addChild(self)

    def setShouldModify(self, shouldModify): #Change the value of shouldModify
        if shouldModify:
            self.shouldModify = True
            if self.parent != 0:
                self.parent.setShouldModify(True)
        else:
            self.shouldModify = False
            
    def setVisible(self, visible): #Return the value of visible
        if visible != self.visible:
            self.visible = visible
            self.setShouldModify(True)

    def setWidth(self, newWidth): #Change the value of width
        if self.getWidth() != newWidth:
            self.width = newWidth
            self._isResizedAtThisFrame = True
            self.setShouldModify(True)

    def setX(self, newX): #Change the value of X
        relativeMove = newX - self.getX()
        self.x = newX
        self._isMoving(0, relativeMove)
        self._isMovingAtThisFrame = True
        self.getParent().setShouldModify(True)

    def setY(self, newY): #Change the value of Y
        relativeMove = newY - self.getY()
        self.y = newY
        self._isMoving(1, relativeMove)
        self._isMovingAtThisFrame = True
        self.getParent().setShouldModify(True)

    def softResetWidget(self):
        """Reset without graphics modification
        """
        self.mouseDown = []
        self.mouseUp = []
        self.overflighted = False
        self._isMovingAtThisFrame = False
        self._isResizedAtThisFrame = False

    def _addChild(self, child): #Add a child to the widget
        if self.containsChild(child.getID()) == -1:
            self._children.append(child)

    def _declaringWidget(self, widget): #Declare widget to the MApp if the widget is a MApp (function defined in MApp) or pass hit to his parent
        self.parent._declaringWidget(widget)

    def _isGettingMouseDown(self, button, relativePos): #Function usefull for heritage, call by MApp when the widget is clicked (called for only one frame) with button = left button (1) and right button (2)
        pass

    def _isGettingMouseUp(self, button, relativePos): #Function usefull for heritage, call by MApp when the widget is stopping of being clicked (called for only one frame) with button = left button (1) and right button (2)
        pass

    def _isGettingOverflighted(self, relativePos): #Function usefull for heritage, call by MApp when the widget is overflighted (applicated for only one frame)
        pass

    def _isKeyGettingDropped(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is dropped on the keyboard (applicated for only one frame)
        pass

    def _isKeyGettingPressed(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is pressed on the keyboard (applicated for only one frame)
        pass

    def _isMoving(self, axis, relativeMove): #Function usefull for heritage, call by setX and setY when the widget is moving
        pass

    def _isNotFocusedAnymore(self): #Function usefull for heritage, call by MApp when the widget is not focused anymore
        pass

    def _isNotOverflightedAnymore(self): #Function usefull for heritage, call by MApp when the widget is not overflighted anymore
        pass

    def _isTextGettingEntered(self, text): #Function usefull for heritage, call by MApp when the widget is focused and the user is typing a text
        pass
    
    def _mouseMove(self, buttons, pos, relativeMove): #Function usefull for heritage, call by MApp when the widget is focused and the mouse is moved
        pass

    def _mouseWheel(self, rotation): #Function usefull for heritage, call by MApp when the widget is focused nad the mouse whell is rotating
        pass

    def _removeChild(self, child): #Remove a child to the widget
        self._children.remove(child)

    def _render(self): #Render widget and return rendering

        if self.getShouldModify(): #If the widget should do the render, do it
            widgetSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

            surfaceABlit = self._renderBeforeHierarchy(widgetSurface).convert_alpha()
            widgetSurface.blit(surfaceABlit, (0, 0, self.getWidth(), self.getHeight()))
            surfaceABlit = self._renderHierarchy(widgetSurface).convert_alpha()
            widgetSurface.blit(surfaceABlit, (0, 0, self.getWidth(), self.getHeight()))
            surfaceABlit = self._renderAfterHierarchy(widgetSurface).convert_alpha()
            widgetSurface.blit(surfaceABlit, (0, 0, self.getWidth(), self.getHeight()))

            self._lastSurface = widgetSurface #Store the last generated surface into _lastSurface

            self.setShouldModify(False) #Update shouldModify
            return widgetSurface
        #Else, use _lastSurface
        return self._lastSurface
    
    def _renderAfterHierarchy(self, surface): #Render widget on surface after hierarchy render
        return surface
    
    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        surface.fill(self.backgroundColor, (0, 0, self.getWidth(), self.getHeight()))
        return surface
    
    def _renderHierarchy(self, surface): #Render hierarchy on surface
        for child in self._children: #Get the _render of all the children
            if child.getVisible():
                surface.blit(child._render(), child.getRect())
        return surface

class MApp(MWidget):
    """Main application class, inherits from MWidget
    """
    def __init__(self, pygameWindow, windowTitle, windowWidth, windowHeight, console = False, printFps = False, windowIcon = ""): #MApp's constructor
        MWidget.__init__(self, 0, 0, windowWidth, windowHeight, 0, "MApp") #Parent class constructor call
        self.console = console
        self.consoleContent = ""
        self.consoleFile = ""
        self.deltaTime = 0
        self.frameCount = 0
        self.focusedWidget = self
        self.fps = 0
        self.maxFps = -1
        self.mousePos = (0, 0)
        self.pressedKey = []
        self.printFps = printFps
        self.windowIcon = ""
        self.setWindowIcon(windowIcon)
        self.setWindowTitle(windowTitle)
        self._deltaTimeCache = time.time_ns()
        self._fpsCount = 0
        self._fpsDuration = 0
        self._lastOverflightedWidget = 0
        self._modifiedWidget = []
        self._objects = []
        self._pygameWindow = pygameWindow
        self._widgets = []

        self.setConsoleFile("console.txt")

        if self.getConsole():
            self.writeConsole("New MWidget object", indentation=0, writer=self)
            self.writeConsole("New MApp object", indentation=1, writer=self)

    def frame(self): #Do a frame in the application
        self.frameEvent()
        self.frameGraphics()

    def frameEvent(self): #Do all events updates in the application
        self.deltaTime = (time.time_ns() - self._deltaTimeCache)/(10**9)
        self._deltaTimeCache = time.time_ns() #Calculate deltaTime

        self._fpsDuration += self.deltaTime
        if self._fpsDuration >= 1: #Handle fps counting
            self.fps = self._fpsCount
            self._fpsDuration -= 1
            self._fpsCount = 0

            if self.printFps:
                print(self.fps)

            if self.getConsole():
                self.writeConsole("New fps count : " + str(self.fps) + " fps", 0, self)

            if self.getConsole():
                consoleFile = open(self.getConsoleFile(), "a")
                consoleFile.write(self.getConsoleContent())
                consoleFile.close()

                self.setConsoleContent("")

        if self.getMaxFps() != -1: #Gérer le nombre maximum de fps
            if self.getDeltaTime() > 0:
                fpsRatio = ((1/self.getMaxFps()) - (self.getDeltaTime())) * 2
                #print(fpsRatio)
                if fpsRatio > 0:
                    temp = time.time_ns()
                    while (time.time_ns() - temp)/(10**9) < fpsRatio:
                        pass
            else:
                fpsRatio = (1/self.getMaxFps())*10**9
                temp = time.time_ns()
                while (time.time_ns() - temp) < fpsRatio:
                    pass

        self._fpsCount += 1

        self.pressedKey.clear()

        for i in self._widgets: #Update and soft reset all widget
            if self.frameCount > 0:
                i.softResetWidget()
            i._update(self.getDeltaTime())

        for i in self._objects: #Update and soft reset all objects
            if self.frameCount > 0:
                i.softResetObject()
            i._update(self.getDeltaTime())

        for i in self._modifiedWidget: #Reset all modified widget in the last call of frameEvent
            i.resetWidget()

        self._modifiedWidget.clear()

        cursor = self.getCursorOnOverflight()

        self.mousePos = pygame.mouse.get_pos() #Get mouse position

        overflightedWidget = self
        i = 0
        while i < len(overflightedWidget.getChildren()): #Find the overflighted widget
            widget = overflightedWidget.getChildrenAtIndex(-(i + 1))
            if widget.posIn(self.mousePos) and widget.getVisible() and not widget.getIgnoreUserEvent():
                overflightedWidget = widget
                i = -1
            i += 1

        cursor = overflightedWidget.getCursorOnOverflight()
        overflightedWidget.overflighted = True
        pygame.mouse.set_cursor(cursor)
        if self._lastOverflightedWidget != overflightedWidget:
            if self._lastOverflightedWidget != 0: self._lastOverflightedWidget._isNotOverflightedAnymore()
            self._lastOverflightedWidget = overflightedWidget
        overflightedWidget._isGettingOverflighted((self.mousePos[0] - overflightedWidget.absoluteX(), self.mousePos[1] - overflightedWidget.absoluteY()))

        events = pygame.event.get()
        for event in events: #Event handler
            if event.type == pygame.QUIT: #Quit pygame
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is clicked
                if overflightedWidget.mouseDown.count(event.button) == 0: overflightedWidget.mouseDown.append(event.button)
                if self.focusedWidget != overflightedWidget:
                    self.setWidgetToFocus(overflightedWidget)
                overflightedWidget._isGettingMouseDown(event.button, (event.pos[0] - overflightedWidget.absoluteX(), event.pos[1] - overflightedWidget.absoluteY()))
            elif event.type == pygame.MOUSEBUTTONUP: #If the mouse is stopping of being clicked
                if overflightedWidget.mouseUp.count(event.button) == 0: overflightedWidget.mouseUp.append(event.button)
                self.focusedWidget._isGettingMouseUp(event.button, (event.pos[0] - overflightedWidget.absoluteX(), event.pos[1] - overflightedWidget.absoluteY()))
            elif event.type == pygame.MOUSEMOTION: #If hte mouse is moving
                self.focusedWidget._mouseMove(event.buttons, (event.pos[0] - self.focusedWidget.absoluteX(), event.pos[1] - self.focusedWidget.absoluteY()), event.rel)
            elif event.type == pygame.MOUSEWHEEL: #If the wheel is rotating
                if self.getConsole():
                    self.writeConsole("Wheel turned", indentation = 0, writer = self.focusedWidget)
                self.focusedWidget._mouseWheel(event.precise_y)
            elif event.type == pygame.KEYDOWN: #If a key is pressed on the keyboard
                if self.getConsole():
                    self.writeConsole("Key " + str(event.key) + " pressed", indentation = 0, writer = self.focusedWidget)
                self.focusedWidget._isKeyGettingPressed(event.key)
                self.pressedKey.append(event.key)
            elif event.type == pygame.KEYUP: #If a key is dropped on the keyboard
                if self.getConsole():
                    self.writeConsole("Key " + str(event.key) + " not pressed anymore", indentation = 0, writer = self.focusedWidget)
                self.focusedWidget._isKeyGettingDropped(event.key)
            elif event.type == pygame.TEXTINPUT: #If the user is enterring text
                if self.getConsole():
                    self.writeConsole("New text \"" + event.text + "\" entered", indentation = 0, writer = self.focusedWidget)
                self.focusedWidget._isTextGettingEntered(event.text)

        for i in self._widgets: #Late update every widgets
            i._lateUpdate(self.getDeltaTime())

        for i in self._objects: #Late update every widgets
            i._lateUpdate(self.getDeltaTime())

        self.frameCount += 1

    def frameGraphics(self): #Do all graphics updates in the application
        for i in self._widgets: #Last update every widgets
            i._lastUpdate(self.getDeltaTime())

        for i in self._objects: #Last update every widgets
            i._lastUpdate(self.getDeltaTime())

        self._pygameWindow.blit(self._render(), (0, 0, self.width, self.height))

    def getConsole(self): #Return console
        return self.console

    def getConsoleContent(self): #Return consoleContent
        return self.consoleContent

    def getConsoleFile(self): #Return consoleFile
        return self.consoleFile

    def getDeltaTime(self): #Return deltaTime
        return self.deltaTime
    
    def getFps(self): #Return fps
        return self.fps
    
    def getMaxFps(self): #Return maxFps
        return self.maxFps

    def getMousePos(self): #Return mousePos
        return self.mousePos

    def getPressedKey(self): #Return pressedKey
        return self.pressedKey
    
    def getPrintFps(self): #Return printFps
        return self.printFps
    
    def getWidgets(self): #Return _widget
        return self._widgets
    
    def getWindowIcon(self): #Return windowIcon
        return self.windowIcon

    def getWindowTitle(self): #Return windowTitle
        return self.windowTitle

    def isKeyPressed(self, key): #Return if the key is pressed
        for i in self.pressedKey:
            if key == i:
                return True
        return False
    
    def setConsole(self, console): #Change the value of console
        self.console = console

    def setConsoleContent(self, consoleContent): #Change the value of consoleContent
        self.consoleContent = consoleContent

    def setConsoleFile(self, consoleFile): #Change the value of consoleFile
        if self.consoleFile != "":
            os.remove(self.consoleFile)

        self.consoleFile = consoleFile
        if os.path.exists(self.consoleFile):
            f = open(self.consoleFile, "w")
            f.write("")
            f.close()

    def setMaxFps(self, maxFps): #Change the value of maxFfps
        if self.maxFps != maxFps:
            self.maxFps = maxFps

    def setPrintFps(self, printFps): #Change the value of printFps
        self.printFps = printFps

    def setWidgetToFocus(self, widgetToFocus): #Change the widget focused
        self.focusedWidget.focused = False
        if self.getConsole():
            self.writeConsole("Widget not focused anymore", indentation = 0, writer = self.focusedWidget)
        self.focusedWidget._isNotFocusedAnymore()
        self.focusedWidget = widgetToFocus
        self.focusedWidget.focused = True
        if self.getConsole():
            self.writeConsole("Mouse clicked", indentation = 0, writer = self.focusedWidget)

    def setWindowIcon(self, windowIcon): #Change the value of windowIcon
        if windowIcon != "" and windowIcon != self.getWindowIcon() and os.path.exists(windowIcon):
            self.windowIcon = windowIcon
            pygame.display.set_icon(pygame.image.load(windowIcon))

    def setWindowTitle(self, windowTitle): #Change the title of the window
        self.windowTitle = windowTitle

        pygame.display.set_caption(windowTitle)

    def writeConsole(self, toWrite, indentation = 0, writer = 0): #Write something into the console
        tns = time.time_ns()/(10**9)
        
        date = time.localtime(tns)
        dateStr = str(date.tm_mday) + "/" + str(date.tm_mon) + "/" + str(date.tm_year) + "-" + str(date.tm_hour) + ":" + str(date.tm_min) + ":" + str(date.tm_sec)
        indent = (" " * (indentation * 2))
        toAdd = dateStr + " | frame : " + str(self.frameCount) + "\n" #French system pattern
        if writer != 0:
            toAdd = " type : " + writer._type + " | id : " + str(writer.getID()) + " | " + toAdd
        self.setConsoleContent(self.getConsoleContent() + indent + toWrite + " - " + toAdd)

    def _addWidgetToReset(self, widget): #Add a widget _modifiedWidget
        self._modifiedWidget.append(widget)

    def _containsWidget(self, widget): #Return if a widget is stored into _widgets
        for i in self._widgets:
            if i.getID() == widget.getID():
                return True
        return False

    def _declaringObject(self, object: MObject) -> None:
        """Declare an object to the MApp

        Args:
            object (MObject): object to declares to the MApp
        """
        if self._objects.count(object) == 0:
            self._objects.append(object)

    def _declaringWidget(self, widget: MWidget) -> None:
        """Declare widget to the MApp if the widget is a MApp or pass hit to his parent (function defined in MWidget)

        Args:
            widget (MWidget): widget to declare
        """
        if not self._containsWidget(widget):
            self._widgets.append(widget)
            widget._mapp = self

    def _undeclaringWidget(self, widget): #Undeclare widget and cut all links with it
        if self._containsWidget(widget):
            self._widgets.remove(widget)

###################### Usefull class to do widget with frame
class MFrame(MWidget):
    def __init__(self, x, y, width, height, parent, widgetType = "MFrame"):
        super().__init__(x, y, width, height, parent, widgetType)

        self.frameBeforeHierarchy = True
        self.frameBottomWidth = 0
        self.frameColor = (0, 0, 0)
        self.frameLeftWidth = 0
        self.frameRightWidth = 0
        self.frameTopWidth = 0
        self.leftBottomCornerRadius = 0
        self.leftTopCornerRadius = 0
        self.rightBottomCornerRadius = 0
        self.rightTopCornerRadius = 0

        if self._mapp.getConsole():
            self._mapp.writeConsole("New MFrame object", indentation = 1, writer = self)

    def getCornerRadius(self, index = 0): #Return the value of leftTopCornerRadius if 0, leftBottomCornerRadius if 1, rightBottomCornerRadius if 2, rightTopCornerRadius if 3
        if index == 0:
            return self.leftTopCornerRadius
        elif index == 1:
            return self.leftBottomCornerRadius
        elif index == 2:
            return self.rightBottomCornerRadius
        else:
            return self.rightTopCornerRadius

    def getFrameBeforeHierarchy(self): #Return the value of frameBeforeHierarchy
        return self.frameBeforeHierarchy
    
    def getFrameColor(self): #Return frameColor
        return self.frameColor
    
    def getFrameRendered(self, surface: pygame.Surface) -> pygame.Surface:
        """Return a surface with the frame rendered on it

        Args:
            surface (pygame.Surface): surface where to draw the frame

        Returns:
            pygame.Surface: surface with the frame rendered on it
        """
        pygame.draw.rect(surface, self.getFrameColor(), (0, 0, self.getFrameWidth(1), self.getHeight()))
        pygame.draw.rect(surface, self.getFrameColor(), (0, 0, self.getWidth(), self.getFrameWidth(0)))
        pygame.draw.rect(surface, self.getFrameColor(), (self.getWidth() - self.getFrameWidth(3), 0, self.getFrameWidth(3), self.getHeight()))
        pygame.draw.rect(surface, self.getFrameColor(), (0, self.getHeight() - self.getFrameWidth(2), self.getWidth(), self.getFrameWidth(2)))
        return surface

    def getFrameWidth(self, index = 0): #Return the value of frameBottomWidth if 1, frameLeftWidth if 2, frameRightWidth if 3, frameTopWidth if 4
        if index == 0:
            return self.frameTopWidth
        elif index == 1:
            return self.frameLeftWidth
        elif index == 2:
            return self.frameBottomWidth
        else:
            return self.frameRightWidth
        
    def setCornerRadius(self, cornerRadius, index = -1): #Return the value of leftTopCornerRadius if 0, leftBottomCornerRadius if 1, rightBottomCornerRadius if 2, rightTopCornerRadius if 3
        if index == 0:
            if self.leftTopCornerRadius != cornerRadius:
                self.leftTopCornerRadius = cornerRadius
                self.setShouldModify(True)
        elif index == 1:
            if self.leftBottomCornerRadius != cornerRadius:
                self.leftBottomCornerRadius = cornerRadius
                self.setShouldModify(True)
        elif index == 2:
            if self.rightBottomCornerRadius != cornerRadius:
                self.rightBottomCornerRadius = cornerRadius
                self.setShouldModify(True)
        elif index == 3:
            if self.rightTopCornerRadius != cornerRadius:
                self.rightTopCornerRadius = cornerRadius
                self.setShouldModify(True)
        else:
            if not (self.leftTopCornerRadius == cornerRadius and self.leftBottomCornerRadius == cornerRadius and self.rightBottomCornerRadius == cornerRadius and self.rightTopCornerRadius == cornerRadius):
                self.leftTopCornerRadius = cornerRadius
                self.leftBottomCornerRadius = cornerRadius
                self.rightBottomCornerRadius = cornerRadius
                self.rightTopCornerRadius = cornerRadius
                self.setShouldModify(True)
    
    def setFrameBeforeHierarchy(self, frameBeforeHierarchy): #Change the value of frameBeforeHierarchy
        if self.frameBeforeHierarchy != frameBeforeHierarchy:
            self.frameBeforeHierarchy = frameBeforeHierarchy
            self.setShouldModify(True)

    def setFrameColor(self, color): #Change the value of frameColor
        if self.frameColor != color:
            self.frameColor = color
            self.setShouldModify(True)

    def setFrameWidth(self, frameWidth, index = -1): #Change the value of frameBottomWidth if 1, frameLeftWidth if 2, frameRightWidth if 3, frameTopWidth if 4
        if index == 0:
            if self.frameTopWidth != frameWidth:
                self.frameTopWidth = frameWidth
                self.setShouldModify(True)
        elif index == 1:
            if self.frameLeftWidth != frameWidth:
                self.frameLeftWidth = frameWidth
                self.setShouldModify(True)
        elif index == 2:
            if self.frameBottomWidth != frameWidth:
                self.frameBottomWidth = frameWidth
                self.setShouldModify(True)
        elif index == 3:
            if self.frameRightWidth != frameWidth:
                self.frameRightWidth = frameWidth
                self.setShouldModify(True)
        else:
            if not (self.frameTopWidth == frameWidth and self.frameLeftWidth == frameWidth and self.frameBottomWidth == frameWidth and self.frameRightWidth == frameWidth):
                self.frameBottomWidth = frameWidth
                self.frameLeftWidth = frameWidth
                self.frameRightWidth = frameWidth
                self.frameTopWidth = frameWidth
                self.setShouldModify(True)

    def _renderAfterHierarchy(self, surface: pygame.Surface): #Render widget on surface after hierarchy render
        if self.getFrameBeforeHierarchy():
            return self.getFrameRendered(surface)
        return surface

    def _renderBeforeHierarchy(self, surface: pygame.Surface): #Render widget on surface before hierarchy render
        surface = super()._renderBeforeHierarchy(surface)
        if not self.getFrameBeforeHierarchy():
            return self.getFrameRendered(surface)
        return surface

###################### Usefull class to display image
class MImage(MFrame):
    def __init__(self, imageLink, x, y, width, height, parent, widgetType = "MImage"):
        super().__init__(x, y, width, height, parent, widgetType)

        self.imageHorizontalAlignment = 0
        self.imageLink = ""
        self.imagePosition = (0, 0)
        self.imageReframing = 0
        self.imageSize = (0, 0)
        self.imageVerticalAlignment = 0
        self._image = 0

        if self._mapp.getConsole():
            self._mapp.writeConsole("New MImage object", indentation = 2, writer = self)

        self.setImageLink(imageLink)

    def getImageHorizontalAlignment(self): #Return "imageAlignment"
        return self.imageHorizontalAlignment

    def getImageLink(self): #Return "imageLink"
        return self.imageLink
    
    def getImagePosition(self): #Return "imagePosition"
        return self.imagePosition
    
    def getImageReframing(self): #Return "imageReframing"
        return self.imageReframing
    
    def getImageSize(self): #Return "imageSize"
        return self.imageSize
    
    def getImageVerticalAlignment(self): #Return "imageVerticalAlignment"
        return self.imageVerticalAlignment
    
    def setImageHorizontalAlignment(self, imageHorizontalAlignment): #Change "imageAlignment"
        if imageHorizontalAlignment != self.imageHorizontalAlignment:
            self.imageHorizontalAlignment = imageHorizontalAlignment
            self.setShouldModify(True)
    
    def setImageLink(self, imageLink, editSize = True): #Change "imageLink"
        if os.path.exists(imageLink):
            if imageLink != self.imageLink:
                self.imageLink = imageLink
                self._image = pygame.image.load(imageLink)
                self._imageToDraw = self._image

                if editSize:
                    self.imageSize = self._image.get_size()
                self._resizeImage()
                self.setShouldModify(True)
        else:
            print("Attention, l'image au lien ", imageLink, "n'existe pas.")

    def setImagePosition(self, imagePosition): #Change "imagePosition"
        if imagePosition != self.imagePosition:
            self.imagePosition = imagePosition
            if self.getImageHorizontalAlignment() == -1 or self.getImageVerticalAlignment() == -1:
                self.setShouldModify(True)

    def setImageReframing(self, imageReframing): #Change imageReframing
        if self.imageReframing != imageReframing:
            self.imageReframing = imageReframing
            self._resizeImage()
            self.setShouldModify(True)

    def setImageSize(self, imageSize): #Change imageSize
        if self.imageSize != imageSize:
            self.imageSize = imageSize
            if self.getImageReframing() == 4:
                self._resizeImage()
                self.setShouldModify(True)

    def setImageVerticalAlignment(self, imageVerticalAlignment): #Change imageVerticalAlignment
        if imageVerticalAlignment != self.imageVerticalAlignment:
            self.imageVerticalAlignment = imageVerticalAlignment
            self.setShouldModify(True)

    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        surface = super()._renderBeforeHierarchy(surface)

        if self._image != 0:
            imageToDraw = self._imageToDraw
            x = 0
            y = 0

            if self.getImageHorizontalAlignment() == -1:
                x = self.getImagePosition()[0]
            elif self.getImageHorizontalAlignment() == 0:
                x = self.getFrameWidth(1)
            elif self.getImageHorizontalAlignment() == 1:
                x = self.getWidth()/2 - imageToDraw.get_width()/2
            else:
                x = self.getWidth() - (self.getFrameWidth(3) + imageToDraw.get_width())

            if self.getImageVerticalAlignment() == -1:
                y = self.getImagePosition()[1]
            elif self.getImageVerticalAlignment() == 0:
                y = self.getFrameWidth(0)
            elif self.getImageVerticalAlignment() == 1:
                y = self.getHeight()/2 - imageToDraw.get_height()/2
            else:
                y = self.getHeight() - (self.getFrameWidth(2) + imageToDraw.get_height())

            surface.blit(imageToDraw, (x, y, imageToDraw.get_width(), imageToDraw.get_height()))

        return surface

    def _resizeImage(self): #Resize image (only with reframing)
        if self.getImageReframing() != 0:
            if self.getImageReframing() == 1:
                resizeNumber = (self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)))/self._image.get_width()
                self._imageToDraw = pygame.transform.scale(self._image, (self._image.get_width() * resizeNumber, self._image.get_height() * resizeNumber))
            elif self.getImageReframing() == 2:
                resizeNumber = (self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2)))/self._image.get_height()
                self._imageToDraw = pygame.transform.scale(self._image, (self._image.get_width() * resizeNumber, self._image.get_height() * resizeNumber))
            elif self.getImageReframing() == 3:
                resizeNumberW = (self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)))/self._image.get_width()
                resizeNumberH = (self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2)))/self._image.get_height()
                self._imageToDraw = pygame.transform.scale(self._image, (self._image.get_width() * resizeNumberW, self._image.get_height() * resizeNumberH))
            else:
                resizeNumberW = self.getImageSize()[0]/self._image.get_width()
                resizeNumberH = self.getImageSize()[1]/self._image.get_height()
                self._imageToDraw = pygame.transform.scale(self._image, (self._image.get_width() * resizeNumberW, self._image.get_height() * resizeNumberH))
            self.setShouldModify(True)

###################### Usefull class to use text
class MText(MFrame):
    def __init__(self, text, x, y, width, height, parent, widgetType = "MText"):
        super().__init__(x, y, width, height, parent, widgetType)

        self.antiAnaliasing = False
        self.authorizedCaracter = ""
        self.cursorPosition = 0
        self.cursorVisible = False
        self.cursorWidth = 2
        self.dynamicTextCut = False
        self.dynamicTextCutType = 1
        self.font = "arial"
        self.fontSize = 12
        self.forbiddenCaracter = ""
        self.input = False
        self.maxTextLength = 0
        self.selection = False
        self.selectionBackgroundColor = (25, 102, 255)
        self.selectionStart = 0
        self.selectionStop = 0
        self.selectionTextColor = (0, 0, 0)
        self.text = text
        self.textBottomOffset = 0
        self.textColor = (0, 0, 0)
        self.textHorizontalAlignment = 0
        self.textLeftOffset = 0
        self.textRightOffset = 0
        self.textTopOffset = 0
        self.textVerticalAlignment = 0
        self.textX = 0
        self.textY = 0
        self._backspacePressed = False
        self._backspacePressedTime = 0
        self._backspaceNumber = 0
        self._baseSelection = 0
        self._bottomArrowPressed = False
        self._bottomArrowPressedAtThisFrame = False
        self._bottomArrowPressedTime = 0
        self._bottomArrowNumber = 0
        self._controlPressed = False
        self._cursorFlashingTime = 0.5
        self._cursorIsVisible = True
        self._cursorVisibleTime = 0
        self._leftArrowPressed = False
        self._leftArrowPressedTime = 0
        self._leftArrowNumber = 0
        self._longestLineSize = 0
        self._returnPressed = False
        self._returnPressedTime = 0
        self._returnNumber = 0
        self._rightArrowPressed = False
        self._rightArrowPressedTime = 0
        self._rightArrowNumber = 0
        self._shiftPressed = False
        self._topArrowPressed = False
        self._topArrowPressedAtThisFrame = False
        self._topArrowPressedTime = 0
        self._topArrowNumber = 0

        if self._mapp.getConsole():
            self._mapp.writeConsole("New MText object", indentation = 2, writer=self)

    def appendText(self, text, appendAtCursor = True, moveCursor = True): #Append "text" to text
        i = 0
        while i < len(text): #Delete ord(13) weird caracter and forbidden caracters
            if(ord(text[i])) == 13 or self.getForbiddenCaracter().count(text[i]) != 0 or (self.getAuthorizedCaracter() != "" and self.getAuthorizedCaracter().count(text[i]) == 0):
               text = text[:i] + text[i+1:len(text)]
               i -= 1
            i += 1
        
        if text != "":
            newText = self.getText()
            if appendAtCursor:
                newText = newText[0:self.getCursorPosition()] + text + newText[self.getCursorPosition():]
            else:
                newText += text

            self.setText(newText)

            if moveCursor:
                self.setCursorPosition(self.getCursorPosition() + len(text))

    def getAntiAnaliasing(self): #Return antiAnaliasing
        return self.antiAnaliasing

    def getAuthorizedCaracter(self): #Return authorizedCaracter
        return self.authorizedCaracter

    def getCursorPosition(self): #Return cursorPosition
        return self.cursorPosition
    
    def getCursorVisible(self): #Return cursorVisible
        return self.cursorVisible
    
    def getCursorWidth(self): #Return cursorWidth
        return self.cursorWidth
    
    def getCuttedText(self, all = False, generator = 0):
        if generator == 0:
            generator = self.getGenerator()

        addLineToCursor = [] #Boolean list to see if the line is natural or not to the cursor
        length = 0
        lengthAtStart = 0
        lineAtStart = 0
        pieces = []
        spaceWidth = generator.size(" ")[0]
        textWidth = self._getTextDisplaySize()[0]
        textY = self.getTextY()
        textYStart = 0
        textYStartAssigned = False
        textYStop = 0

        if not self.getDynamicTextCut(): #Cut lines into pieces
            cutted = self.getText().split("\n")
            j = 0
            for i in cutted:
                if not all:
                    lineHeight = generator.size(i)[1]
                    if textY < self._getTextDisplaySize()[1]:
                        if textY + lineHeight > 0:
                            addLineToCursor.append(2)
                            pieces.append(i)
                            if not textYStartAssigned:
                                lengthAtStart = length
                                lineAtStart = j
                                textYStart = textY
                                textYStartAssigned = True
                    else:
                        textYStop = textY
                        break
                    textY += lineHeight
                else:
                    addLineToCursor.append(2)
                    pieces.append(i)
                j += 1
                length += len(i) + 1
        else:
            j = 0
            lines = self.getText().split("\n")
            for line in lines:
                firstI = 0
                lastI = 0
                lineWidth = 0
                toAnalyze = line
                if self.dynamicTextCutType == 1:
                    toAnalyze = line.split(" ")

                for letter in toAnalyze: #Analyze caracter by caracter/word by word
                    letterSize = generator.size(letter)
                    if lineWidth + letterSize[0] > textWidth and firstI != lastI: #If words are bigger than one line
                        toAdd = ""
                        for i in range(firstI, lastI):
                            toAdd += toAnalyze[i]
                            if self.dynamicTextCutType == 1 and i != lastI - 1:
                                toAdd += " "
                        
                        if not all:
                            lineHeight = generator.size(toAdd)[1]
                            if textY < self._getTextDisplaySize()[1]:
                                if textY + lineHeight > 0:
                                    if self.getDynamicTextCutType() == 0:
                                        addLineToCursor.append(0) #Cut by a caracter
                                    else:
                                        addLineToCursor.append(1) #Cut by a space
                                    pieces.append(toAdd)
                                    if not textYStartAssigned:
                                        lengthAtStart = length
                                        lineAtStart = j
                                        textYStart = textY
                                        textYStartAssigned = True
                            else:
                                textYStop = textY
                                break
                            j += 1
                            textY += lineHeight
                        else:
                            if self.getDynamicTextCutType() == 0:
                                addLineToCursor.append(0) #Cut by a caracter
                            else:
                                addLineToCursor.append(1) #Cut by a space
                                length += 1
                            j += 1
                            pieces.append(toAdd)
                        firstI = lastI
                        lineWidth = 0
                    lastI += 1
                    lineWidth += letterSize[0]
                    if self.dynamicTextCutType == 1:
                        lineWidth += spaceWidth

                if firstI < len(toAnalyze): #If last word/caracter didn't get analyzed
                    toAdd = ""
                    for i in range(firstI, len(toAnalyze)):
                        toAdd += toAnalyze[i]
                        if self.dynamicTextCutType == 1 and i != len(toAnalyze) - 1:
                            toAdd += " "

                    if not all:
                        lineHeight = generator.size(toAdd)[1]
                        if textY < self._getTextDisplaySize()[1]:
                            if textY + lineHeight > 0:
                                pieces.append(toAdd)
                                if not textYStartAssigned:
                                    lengthAtStart = length
                                    lineAtStart = j
                                    textYStart = textY
                                    textYStartAssigned = True
                        else:
                            textYStop = textY
                            break
                        textY += lineHeight
                    else:
                        pieces.append(toAdd)

                if len(toAnalyze) == 0: #If the line is empty
                    toAdd = ""
                    if not all:
                        lineHeight = generator.size(toAdd)[1]
                        if textY < self._getTextDisplaySize()[1]:
                            if textY + lineHeight > 0:
                                pieces.append(toAdd)
                                if not textYStartAssigned:
                                    lengthAtStart = length
                                    lineAtStart = j
                                    textYStart = textY
                                    textYStartAssigned = True
                        else:
                            textYStop = textY
                            break
                        textY += lineHeight
                    else:
                        pieces.append(toAdd)

                if len(addLineToCursor) <= len(pieces) - 1:
                    addLineToCursor.append(2) #Cut by a line breaker

                j += 1
                length += len(line) + 1

        return pieces.copy(), addLineToCursor.copy(), (textYStart, textYStop, lengthAtStart, lineAtStart)

    def getDynamicTextCut(self): #Return dynamicTextCut
        return self.dynamicTextCut
    
    def getDynamicTextCutType(self): #Return dynamicTextCutType
        return self.dynamicTextCutType

    def getFont(self): #Return font
        return self.font
    
    def getFontSize(self): #Return fontSize
        return self.fontSize
    
    def getForbiddenCaracter(self): #Return forbiddenCaracter
        return self.forbiddenCaracter

    def getGenerator(self): #Return the generator of the mtext
        if os.path.exists(self.getFont()):
            return pygame.font.Font(self.getFont(), self.getFontSize())
        return pygame.font.SysFont(self.getFont(), self.getFontSize())

    def getInput(self): #Return input
        return self.input

    def getMaxTextLengt(self): #Return maxTextLength
        return self.maxTextLength

    def getSelectedText(self): #Return the selected text into the mtext
        if self.getSelection() and self.getSelectionStart() != self.getSelectionStop():
            return self.getText()[self.getSelectionStart():self.getSelectionStop()]
        else:
            return -1

    def getSelection(self): #Return selection
        return self.selection

    def getSelectionBackgroundColor(self): #Return selectionBackgroundColor
        return self.selectionBackgroundColor

    def getSelectionStart(self): #Return selectionStart
        return self.selectionStart
    
    def getSelectionStop(self): #Return selectionStart
        return self.selectionStop

    def getSelectionTextColor(self): #Return selectionTextColor
        return self.selectionTextColor

    def getText(self): #Return text
        return self.text
    
    def getTextColor(self): #Return textColor
        return self.textColor
    
    def getTextHorizontalAlignment(self): #Return textHorizontalAlignment
        return self.textHorizontalAlignment
    
    def getTextOffset(self, index): #Return textTopOffset if index = 0, textLeftOffset if index = 1, textBottomOffset if index = 2, textRightOffset if index = 3
        if index == 0:
            return self.textTopOffset
        elif index == 1:
            return self.textLeftOffset
        elif index == 2:
            return self.textBottomOffset
        else:
            return self.textRightOffset
    
    def getTextVerticalAlignment(self): #Return textVerticalAlignment
        return self.textVerticalAlignment
    
    def getTextX(self): #Return textX
        return self.textX
    
    def getTextY(self): #Return textY
        return self.textY
    
    def setAntiAnaliasing(self, antiAnaliasing): #Change the value of antiAnaliasing
        if self.getAntiAnaliasing() != antiAnaliasing:
            self.antiAnaliasing = antiAnaliasing
            self.setShouldModify(True)

    def setAuthorizedCaracter(self, authorizedCaracter): #Return authorizedCaracter
        if self.getAuthorizedCaracter() != authorizedCaracter:
            self.authorizedCaracter = authorizedCaracter

    def setCursorPosition(self, cursorPosition): #Change the value of cursorPosition
        if self.cursorPosition != cursorPosition and cursorPosition >= 0 and cursorPosition <= len(self.getText()):
            self.cursorPosition = cursorPosition
            self.setShouldModify(True)
    
    def setCursorVisible(self, cursorVisible): #Change the value of cursorVisible
        if self.cursorVisible != cursorVisible:
            self.cursorVisible = cursorVisible
            self.setShouldModify(True)

    def setCursorWidth(self, cursorWidth): #Change the value of cursorWidth
        if self.cursorWidth != cursorWidth:
            self.cursorWidth = cursorWidth
            if self.getCursorVisible() and self._getCursorIsVisible():
                self.setShouldModify(True)
    
    def setDynamicTextCut(self, dynamicTextCut): #Change the value of dynamicTextCut
        if self.dynamicTextCut != dynamicTextCut:
            self.dynamicTextCut = dynamicTextCut
            self.setShouldModify(True)

    def setDynamicTextCutType(self, dynamicTextCutType): #Change the value of dynamicTextCutType
        if self.dynamicTextCutType != dynamicTextCutType:
            self.dynamicTextCutType = dynamicTextCutType
            self.setShouldModify(True)
    
    def setFont(self, font): #Change the value of font
        if self.font != font:
            self.font = font
            self.setShouldModify(True)
    
    def setFontSize(self, fontSize): #Change the value of fontSize
        if self.fontSize != fontSize:
            self.fontSize = fontSize
            self.setShouldModify(True)

    def setForbiddenCaracter(self, forbiddenCaracter): #Return forbiddenCaracter
        if self.getForbiddenCaracter() != forbiddenCaracter:
            self.forbiddenCaracter = forbiddenCaracter

    def setInput(self, input): #Change the value of input
        self.input = input
        self.setCursorVisible(input)
        self.setSelection(input)
    
    def setMaxTextLengt(self, maxTextLength): #Return maxTextLength
        if self.getMaxTextLengt() != maxTextLength:
            self.maxTextLength = maxTextLength
            if len(self.getText()) > maxTextLength:
                self.setText(self.getText[:maxTextLength])

    def setSelection(self, selection): #Change the value of selection
        if selection != self.getSelection():
            self.selection = selection
            if self.selectionStart != self.selectionStop:
                self.setShouldModify(True)

    def setSelectionBackgroundColor(self, selectionBackgroundColor): #Change the value of selectionBackgroundColor
        if selectionBackgroundColor != self.getSelectionBackgroundColor():
            self.selectionBackgroundColor = selectionBackgroundColor
            if self.getSelection() and self.getSelectionStart() != self.getSelectionStop():
                self.setShouldModify(True)

    def setSelectionPos(self, selectionStart, selectionStop): #Change the value of selectionStart and selectionStop more easily
        self.setSelectionStop(len(self.getText()) + 1) #Neutralize _checkSelection effect
        self.setSelectionStart(0)
        self.setSelectionStop(selectionStop) #Apply modifications
        self.setSelectionStart(selectionStart)

    def setSelectionStart(self, selectionStart): #Change the value of selectionStart
        if selectionStart != self.getSelectionStart():
            self.selectionStart = selectionStart
            if self.selectionStart < 0:
                self.selectionStart = 0
            if self.getSelectionStart() > self.getSelectionStop():
                s = self.getSelectionStart()
                self.setSelectionStart(self.getSelectionStop())
                self.setSelectionStop(s)
            else:
                if self.getSelection():
                    self.setShouldModify(True)

    def setSelectionStop(self, selectionStop): #Change the value of selectionStop
        if selectionStop != self.getSelectionStop():
            self.selectionStop = selectionStop
            if self.getSelectionStop() > len(self.getText()) + 1:
                self.setSelectionStop(len(self.getText()) + 1)
            if self.getSelectionStop() < self.getSelectionStart():
                s = self.getSelectionStart()
                self.setSelectionStart(self.getSelectionStop())
                self.setSelectionStop(s)
            else:
                if self.getSelection():
                    self.setShouldModify(True)

    def setSelectionTextColor(self, selectionTextColor): #Change the value of selectionTextColor
        if selectionTextColor != self.getSelectionTextColor():
            self.selectionTextColor = selectionTextColor
            if self.getSelection() and self.getSelectionStart() != self.getSelectionStop():
                self.setShouldModify(True)

    def setText(self, text): #Change the value of text
        if self.text != text:
            if self.getMaxTextLengt() != 0 and len(text) > self.getMaxTextLengt():
                text = text[:self.getMaxTextLengt()]
            self.text = text
            self._checkSelection()
            self._cursorVisibleTime = 0
            self._setCursorIsVisible(True)
            if len(text) < self.getCursorPosition():
                self.setCursorPosition(len(text))
            self.setShouldModify(True)

    def setTextColor(self, textColor): #Change the value of textColor
        if self.textColor != textColor:
            self.textColor = textColor
            self.setShouldModify(True)

    def setTextHorizontalAlignment(self, textHorizonAlignment): #Change the value of textAlignment
        if self.textHorizontalAlignment != textHorizonAlignment:
            self.textHorizontalAlignment = textHorizonAlignment
            self.setShouldModify(True)

    def setTextOffset(self, textOffset, index = -1): #Change the value of textTopOffset if index = 0, textLeftOffset if index = 1, textBottomOffset if index = 2, textRightOffset if index = 3
        if index == 0 and self.textTopOffset != textOffset:
            self.textTopOffset = textOffset
            self.setShouldModify(True)
        elif index == 1 and self.textLeftOffset != textOffset:
            self.textLeftOffset = textOffset
            self.setShouldModify(True)
        elif index == 2 and self.textBottomOffset != textOffset:
            self.textBottomOffset = textOffset
            self.setShouldModify(True)
        elif index == 3 and self.textRightOffset != textOffset:
            self.textRightOffset = textOffset
            self.setShouldModify(True)
        elif not (self.textTopOffset != textOffset and self.textLeftOffset == textOffset and self.textBottomOffset == textOffset and self.textRightOffset == textOffset):
            self.textTopOffset = textOffset
            self.textLeftOffset = textOffset
            self.textBottomOffset = textOffset
            self.textRightOffset = textOffset
            self.setShouldModify(True)

    def setTextVerticalAlignment(self, textVerticalAlignment): #Change the value of textAlignment
        if self.textVerticalAlignment != textVerticalAlignment:
            self.textVerticalAlignment = textVerticalAlignment
            self.setShouldModify(True)

    def setTextX(self, textX): #Change the value of textX
        if self.textX != textX:
            if textX > 0 or self._longestLineSize <= self._getTextDisplaySize()[0]:
                textX = 0
            elif -textX > self._longestLineSize - self._getTextDisplaySize()[0]:
                textX = -self._longestLineSize + self._getTextDisplaySize()[0]
            self.textX = textX
            self.setShouldModify(True)
    
    def setTextY(self, textY): #Change the value of textY
        if self.textY != textY:
            if textY > 0 or self._getTextHeight() <= self._getTextDisplaySize()[1]:
                textY = 0
            elif textY < -(self._getTextHeight() - self._getTextDisplaySize()[1]):
                textY = -(self._getTextHeight() - self._getTextDisplaySize()[1])
            self.textY = textY
            self.setShouldModify(True)

    def _checkSelection(self): #Check if the selection is still good according to the text
        if self.selection:
            if self.getSelectionStart() < 0:
                self.setSelectionStart(0)
            if self.getSelectionStop() > len(self.getText()) + 1:
                self.setSelectionStop(len(self.getText()) + 1)
            if self.getSelectionStart() > self.getSelectionStop():
                s = self.getSelectionStart()
                self.setSelectionStart(self.getSelectionStop())
                self.setSelectionStop(s)

    def _cursorBottom(self): #Put up the cursor into the line at the top
        self._setCursorIsVisible(True)

        if self._controlPressed:
            self.setTextY(self.getTextY() - 30)
        else:
            generator = pygame.font.SysFont(self.getFont(), self.getFontSize())
            heightCursor = generator.size(" ")[1]

            x = self._getPositionX(generator, self.getCursorPosition())
            y = self._getPositionY(generator, self.getCursorPosition()) + heightCursor + heightCursor/2

            pos = self._getPositionAtPos(generator, (x, y))

            if self.getSelection() and self._shiftPressed:
                if self.getSelectedText() == -1:
                    self.setSelectionPos(self.getCursorPosition(), pos)
                else:
                    if self._baseSelection < pos:
                        self.setSelectionPos(self._baseSelection, pos)
                    else:
                        self.setSelectionPos(pos, self._baseSelection)
            else:
                self.setSelectionPos(0, 0)
            self.setCursorPosition(pos)

    def _cursorLeft(self): #Put the cursor at the left
        leftOffset = 1
        if self._controlPressed:
            firstCar = ""
            firstToPass = False
            leftOffset = 0
            textToAnalyse = self.getText()[:self.getCursorPosition()]
            toVerify = " .-'"
            if toVerify.count(textToAnalyse[-1]):
                if textToAnalyse[-1] == textToAnalyse[-2]:
                    firstCar = textToAnalyse[-1]
                    firstToPass = True
                leftOffset = 1
                textToAnalyse = textToAnalyse[:-1]

            for j in range(len(textToAnalyse)):
                i = textToAnalyse[::-1][j]
                if toVerify.count(i):
                    j2 = j + 1
                    if firstToPass:
                        while toVerify.count(textToAnalyse[::-1][j2]) and textToAnalyse[::-1][j2] == firstCar and j2 < len(textToAnalyse):
                            leftOffset += 1
                            textToAnalyse = textToAnalyse[:-1]
                        leftOffset += 1
                    break
                leftOffset += 1
        
        if self.getSelection() and self._shiftPressed:
            if self.getSelectedText() == -1:
                self.setSelectionPos(self.getCursorPosition() - leftOffset, self.getCursorPosition())
            else:
                if self._baseSelection < self.getCursorPosition() - leftOffset:
                    self.setSelectionPos(self._baseSelection, self.getCursorPosition() - leftOffset)
                else:
                    self.setSelectionPos(self.getCursorPosition() - leftOffset, self._baseSelection)
        else:
            self.setSelectionPos(0, 0)
        self.setCursorPosition(self.getCursorPosition() - leftOffset)

    def _cursorRight(self): #Put the cursor at the right
        rightOffset = 1
        if self._controlPressed:
            firstCar = ""
            firstToPass = False
            rightOffset = 0
            textToAnalyse = self.getText()[self.getCursorPosition():]
            toVerify = " .-'"
            if toVerify.count(textToAnalyse[0]):
                if textToAnalyse[0] == textToAnalyse[1]:
                    firstCar = textToAnalyse[0]
                    firstToPass = True
                rightOffset = 1
                textToAnalyse = textToAnalyse[1:]

            for j in range(len(textToAnalyse)):
                i = textToAnalyse[j]
                if toVerify.count(i):
                    j2 = j + 1
                    if firstToPass:
                        while toVerify.count(textToAnalyse[j2]) and textToAnalyse[j2] == firstCar and j2 < len(textToAnalyse):
                            rightOffset += 1
                            textToAnalyse = textToAnalyse[1:]
                        rightOffset += 1
                    break
                rightOffset += 1
        
        if self.getSelection() and self._shiftPressed:
            if self.getSelectedText() == -1:
                self.setSelectionPos(self.getCursorPosition(), self.getCursorPosition() + rightOffset)
            else:
                if self._baseSelection < self.getCursorPosition() + rightOffset:
                    self.setSelectionPos(self._baseSelection, self.getCursorPosition() + rightOffset)
                else:
                    self.setSelectionPos(self.getCursorPosition() + rightOffset, self._baseSelection)
        else:
            self.setSelectionPos(0, 0)
        self.setCursorPosition(self.getCursorPosition() + rightOffset)

    def _cursorTop(self): #Put down the cursor into the line at the top
        if self._controlPressed:
            self.setTextY(self.getTextY() - 30)
        else:
            self._setCursorIsVisible(True)

            generator = pygame.font.SysFont(self.getFont(), self.getFontSize())
            heightCursor = generator.size(" ")[1]

            x = self._getPositionX(generator, self.getCursorPosition())
            y = self._getPositionY(generator, self.getCursorPosition()) - heightCursor/2

            pos = self._getPositionAtPos(generator, (x, y))
            if y < 0:
                pos = 0

            if self.getSelection() and self._shiftPressed:
                if self.getSelectedText() == -1:
                    self.setSelectionPos(pos, self.getCursorPosition())
                else:
                    if self._baseSelection <= pos:
                        self.setSelectionPos(pos, self._baseSelection)
                    else:
                        self.setSelectionPos(pos, self._baseSelection)
            else:
                self.setSelectionPos(0, 0)
            self.setCursorPosition(pos)
    
    def _doBackspaceEffet(self): #Do the effect of the pression fo the backspace touch
        if self.getInput():
            if self.getSelection() and self.getSelectedText() != -1:
                self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                self.setSelectionPos(0, 0)
            else:
                self._removeTextAtPos(1, self.getCursorPosition())

    def _getCursorIsVisible(self): #Return the value of _cursorIsVisible
        return self._cursorIsVisible
    
    def _getPositionLine(self, generator, position): #Return the line of the cursor
        pieces, piecesLineReturn, textYStart = self.getCuttedText(all=True, generator=generator)

        i = 0
        yCursor = 0
        textLength = 0
        for piece in pieces: #Analyze text line par line
            textLength += len(piece)

            offset = 0
            if piecesLineReturn[i] != 0:
                textLength += 1
            else:
                offset = 1

            if textLength <= position - offset:
                yCursor += 1
            else:
                return yCursor
            
            i += 1
        return yCursor

    def _getPositionAtPos(self, generator, pos): #Return the position in the text at one pos
        pieces = self.getCuttedText(all=True, generator=generator)
        
        i = 0
        lineLength = 0
        textLength = 0
        x = self.getFrameWidth(1) + self.getTextOffset(1) + self.getTextX()
        y = self.getFrameWidth(0) + self.getTextOffset(0)

        if self.getTextVerticalAlignment() == 1:
            y = self.getFrameWidth(0) + self.getTextOffset(0)
            y += (((self.getHeight()-(self.getFrameWidth(0)+self.getFrameWidth(2)+self.getTextOffset(0)+self.getTextOffset(2)))/2) - self._getTextHeight(generator)/2)
        elif self.getTextVerticalAlignment() == 2:
            y = self.getHeight() - (self.getFrameWidth(2) + self._getTextHeight(generator) + self.getTextOffset(2))

        y += self.getTextY()

        if pos[1] < y:
            return 0

        for piece in pieces[0]: #Search for y
            size = generator.size(piece)

            lineLength = size[0]
            y += size[1]
            if y > pos[1]:
                break
            else:
                textLength += len(piece)

            if pieces[1][i] != 0:
                textLength += 1

            i += 1

        if i == len(pieces[0]):
            i -= 1

        if self.getTextHorizontalAlignment() == 1:
            x = self.getTextOffset(1) + ((self.getWidth()-(self.getTextOffset(1)+self.getTextOffset(3)))/2) - lineLength/2
        elif self.getTextHorizontalAlignment() == 2:
            x = self.getWidth() - (self.getFrameWidth(3) + lineLength + self.getTextOffset(3))

        for piece in pieces[0][i]: #Search for x
            textLength += 1
            toAdd = generator.size(piece)[0]
            x += toAdd
            if x > pos[0]:
                if (x - pos[0]) > (pos[0] - (x - toAdd)):
                    textLength -= 1
                break

        return textLength

    def _getPositionX(self, generator, position): #Return the x pos of the cursor
        pieces, piecesLineReturn, textYStart = self.getCuttedText(all=True, generator=generator)

        i = -1
        lineSize = 0
        textLength = 0
        textSize = -1
        for piece in pieces: #Analyze each lines
            i += 1

            textLength += len(piece)
            if textLength >= position:
                lineSize = generator.size(piece)[0]
                textSize = generator.size(piece[0:(position-(textLength-len(piece)))])[0] + self.getTextX()
                break

            if piecesLineReturn[i] != 0:
                textLength += 1

        if textSize == -1:
            lineSize = generator.size(pieces[-1])[0]
            textSize = lineSize

        #return textSize
        if self.getTextHorizontalAlignment() == 0: #Apply alignment modification
            return textSize + self.getFrameWidth(1) + self.getTextOffset(1)
        elif self.getTextHorizontalAlignment() == 1:
            return self.getTextOffset(1) + ((self.getWidth()-(self.getTextOffset(1)+self.getTextOffset(3)))/2-lineSize/2) + textSize
        else:
            return self.getWidth() - (self.getFrameWidth(3) + (lineSize - textSize) + self.getTextOffset(3))
    
    def _getPositionY(self, generator, position): #Return the y pos of the cursor
        pieces, addLineToCursor, textY = self.getCuttedText(all=False,generator=generator)

        i = textY[3]
        line = self._getPositionLine(generator, position)
        spaceHeight = generator.size(" ")[1]
        if i > line or i + len(pieces) < line:
            return -spaceHeight
        
        textHeight = 0
        textLengt = 0
        yAssignee = True
        yCursor = -1
        for piece in pieces: #Analyze each lines
            textHeight += generator.size(piece)[1]
            textLengt += len(piece)

            if i >= line and yAssignee:
                yAssignee = False
                yCursor = textHeight - generator.size(piece)[1]
                
            i += 1

        if yCursor == -1:
            yCursor = textHeight - generator.size(pieces[-1])[1]

        yCursor += textY[0]

        if self.getTextVerticalAlignment() == 0: #Apply alignment modification
            yCursor += self.getFrameWidth(0) + self.getTextOffset(0)
        elif self.getTextVerticalAlignment() == 1:
            yCursor += self.getFrameWidth(0) + self.getTextOffset(0) + ((self.getHeight()-(self.getFrameWidth(0)+self.getFrameWidth(2)+self.getTextOffset(0)+self.getTextOffset(2)))/2-textHeight/2)
        else:
            yCursor = (self.getHeight()-((textHeight-yCursor)+self.getFrameWidth(2)+self.getTextOffset(2)))

        return yCursor
    
    def _getTextDisplaySize(self): #Return the size of the display of the text
        return (self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3) + self.getTextOffset(1) + self.getTextOffset(3)), #Width
                self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2) + self.getTextOffset(0) + self.getTextOffset(2))) #Height

    def _getTextHeight(self, generator=0): #Return the height of the text
        if generator == 0:
            generator = self.getGenerator()
        
        pieces = self.getCuttedText(all=True, generator=generator)[0]
        textHeight = 0

        for piece in pieces:
            textHeight += generator.size(piece)[1]
        return textHeight
    
    def _getTextRendered(self, all=False, generator=0): #Return a list with all the text rendered
        if generator == 0:
            generator = self.getGenerator()
        
        pieces, addLineToReturn, textY = self.getCuttedText(all=all, generator=generator)
        textYStart = textY[0]
        textYStop = textY[1]
        
        i = 0
        isSelected = False
        selectionStarted = False
        selectionStartOffset = -1
        surfaces = []
        textLength = textY[2]
        textY = self.getTextY()
        self._longestLineSize = 0
        for piece in pieces: #Render text into pieces
            textHeight = generator.size(piece)[1]
            textLength += len(piece)
            if addLineToReturn[i] != 0:
                textLength += 1
            if self.getSelection() and self.getSelectionStart() != self.getSelectionStop() and textLength > self.getSelectionStart() + selectionStartOffset and (not selectionStarted or isSelected): #If the selection start at this line
                if not selectionStarted: #Start selection
                    isSelected = True
                    selectionStarted = True
                    if textLength > self.getSelectionStop() + selectionStartOffset: #And end at this line too
                        textSurface1 = generator.render(piece[:len(piece)-(textLength-self.getSelectionStart()+selectionStartOffset)], self.getAntiAnaliasing(), self.getTextColor()).convert_alpha()
                        textSurface2 = generator.render(piece[len(piece)-(textLength-self.getSelectionStart()+selectionStartOffset):len(piece)-(textLength-self.getSelectionStop()+selectionStartOffset)], self.getAntiAnaliasing(), self.getSelectionTextColor()).convert_alpha()
                        textSurface3 = generator.render(piece[len(piece)-(textLength-self.getSelectionStop()+selectionStartOffset):], self.getAntiAnaliasing(), self.getTextColor()).convert_alpha()
                        surfaceSelectionBackground = pygame.Surface((textSurface2.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        surfaceSelectionBackground.fill(self.getSelectionBackgroundColor())
                        textSurface = pygame.Surface((textSurface1.get_width() + textSurface2.get_width() + textSurface3.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        textSurface.blit(surfaceSelectionBackground, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        textSurface.blit(textSurface1, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface2, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        textSurface.blit(textSurface3, (textSurface1.get_width() + textSurface2.get_width(), 0, textSurface3.get_width(), textSurface3.get_height()))
                        surfaces.append(textSurface)
                        isSelected = False
                    else:
                        textSurface1 = generator.render(piece[:len(piece)-(textLength-self.getSelectionStart()+selectionStartOffset)], self.getAntiAnaliasing(), self.getTextColor()).convert_alpha()
                        textSurface2 = generator.render(piece[len(piece)-(textLength-self.getSelectionStart()+selectionStartOffset):len(piece)-(textLength-self.getSelectionStop())], self.getAntiAnaliasing(), self.getSelectionTextColor()).convert_alpha()
                        surfaceSelectionBackground = pygame.Surface((textSurface2.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        surfaceSelectionBackground.fill(self.getSelectionBackgroundColor())
                        textSurface = pygame.Surface((textSurface1.get_width() + textSurface2.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        textSurface.blit(surfaceSelectionBackground, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        textSurface.blit(textSurface1, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface2, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        surfaces.append(textSurface)
                elif isSelected: #Line in the middle of the selection
                    if textLength <= self.getSelectionStop() + selectionStartOffset: #And end at this line too
                        textSurface1 = generator.render(piece, self.getAntiAnaliasing(), self.getSelectionTextColor()).convert_alpha()
                        surfaceSelectionBackground = pygame.Surface((textSurface1.get_width(), textSurface1.get_height()), pygame.SRCALPHA)
                        surfaceSelectionBackground.fill(self.getSelectionBackgroundColor())
                        textSurface = pygame.Surface((textSurface1.get_width(), textSurface1.get_height()), pygame.SRCALPHA)
                        textSurface.blit(surfaceSelectionBackground, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface1, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        surfaces.append(textSurface)
                    else: #End selection in a another line than the first selection position
                        textSurface1 = generator.render(piece[:len(piece)-(textLength-self.getSelectionStop() + selectionStartOffset)], self.getAntiAnaliasing(), self.getSelectionTextColor()).convert_alpha()
                        textSurface2 = generator.render(piece[len(piece)-(textLength-self.getSelectionStop() + selectionStartOffset):], self.getAntiAnaliasing(), self.getTextColor()).convert_alpha()
                        surfaceSelectionBackground = pygame.Surface((textSurface1.get_width(), textSurface1.get_height()), pygame.SRCALPHA)
                        surfaceSelectionBackground.fill(self.getSelectionBackgroundColor())
                        textSurface = pygame.Surface((textSurface1.get_width() + textSurface2.get_width(), textSurface2.get_height()), pygame.SRCALPHA)
                        textSurface.blit(surfaceSelectionBackground, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface1, (0, 0, textSurface1.get_width(), textSurface1.get_height()))
                        textSurface.blit(textSurface2, (textSurface1.get_width(), 0, textSurface2.get_width(), textSurface2.get_height()))
                        surfaces.append(textSurface)
                        isSelected = False
            else:
                textSurface = generator.render(piece, self.getAntiAnaliasing(), self.textColor).convert_alpha()
                surfaces.append(textSurface)
            i += 1
            textY += textHeight

            if surfaces[-1].get_width() > self._longestLineSize:
                self._longestLineSize = surfaces[-1].get_width()
        
        return surfaces, textYStart
    
    def _isGettingMouseDown(self, button, relativePos): #Function usefull for heritage, call by MApp when the widget is clicked by the mouse
        if button == 1:
            cursorPos = self._getPositionAtPos(pygame.font.SysFont(self.font, self.fontSize), relativePos)
            if self.getCursorVisible():
                self._cursorIsVisible = True
                self._cursorVisibleTime = 0
                self.setCursorPosition(cursorPos)
                self.setShouldModify(True)
            self.setSelectionPos(cursorPos, cursorPos)
            self._baseSelection = cursorPos

    def _isGettingMouseUp(self, button, relativePos): ##Function usefull for heritage, call by MApp when the widget isn't clicked by the mouse anymore
        if button == 1:
            cursorPos = self._getPositionAtPos(pygame.font.SysFont(self.font, self.fontSize), relativePos)
            if self.getCursorVisible():
                self.setCursorPosition(cursorPos)
                
    def _isKeyGettingDropped(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is dropped on the keyboard (applicated for only one frame)
        if key == pygame.K_DOWN:
            self._bottomArrowPressed = False
            self._bottomArrowPressedTime = 0
            self._bottomArrowNumber = 0
        elif key == pygame.K_LEFT:
            self._leftArrowPressed = False
            self._leftArrowPressedTime = 0
            self._leftArrowNumber = 0
        elif key == pygame.K_RIGHT:
            self._rightArrowPressed = False
            self._rightArrowPressedTime = 0
            self._rightArrowNumber = 0
        elif key == pygame.K_UP:
            self._topArrowPressed = False
            self._topArrowPressedTime = 0
            self._topArrowNumber = 0
        elif key == pygame.K_BACKSPACE:
            self._backspacePressed = False
            self._backspacePressedTime = 0
            self._backspaceNumber = 0
        elif key == pygame.K_RCTRL or key == pygame.K_LCTRL:
            self._controlPressed = False
        elif key == pygame.K_RETURN:
            self._returnPressed = False
            self._returnPressedTime = 0
            self._returnNumber = 0
        elif key == pygame.K_RCTRL or key == pygame.K_LCTRL:
            self._controlPressed = False
        elif key == pygame.K_RSHIFT or key == pygame.K_LSHIFT:
            self._baseSelection = 0
            self._shiftPressed = False

    def _isKeyGettingPressed(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is pressed on the keyboard (applicated for only one frame)
        if self.getCursorVisible(): #Cursor navigation
            if key == pygame.K_DOWN:
                self._cursorBottom()
                self._bottomArrowPressedAtThisFrame = True
                self.setShouldModify(True)

                self._bottomArrowPressed = True
                self._bottomArrowPressedTime = 0
                self._bottomArrowNumber = 0
            elif key == pygame.K_LEFT and len(self.getText()) > 0:
                self._cursorLeft()
                self._cursorVisibleTime = 0
                self._setCursorIsVisible(True)

                self._leftArrowPressed = True
                self._leftArrowPressedTime = 0
                self._leftArrowNumber = 0
            elif key == pygame.K_RIGHT and len(self.getText()) > 0:
                self._cursorRight()
                self._cursorVisibleTime = 0
                self._setCursorIsVisible(True)

                self._rightArrowPressed = True
                self._rightArrowPressedTime = 0
                self._rightArrowNumber = 0
            elif key == pygame.K_UP:
                self._cursorTop()
                self._topArrowPressedAtThisFrame = True
                self.setShouldModify(True)

                self._topArrowPressed = True
                self._topArrowPressedTime = 0
                self._topArrowNumber = 0
        
        if self.getInput(): #Special touch handle
            if key == pygame.K_BACKSPACE:
                self._doBackspaceEffet()
                self._backspacePressed = True
                self._backspacePressedTime = 0
                self._backspaceNumber = 0
            elif key == pygame.K_RETURN:
                if self.getSelection() and self.getSelectedText() != -1:
                    self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                    self.setSelectionPos(0, 0)
                self.appendText("\n")
                self._returnPressed = True
                self._returnPressedTime = 0
                self._returnNumber = 0
            elif key == pygame.K_a and self._controlPressed:
                self.setCursorPosition(len(self.getText()))
                self.setSelectionPos(0, len(self.getText()))
            elif key == pygame.K_c and self._controlPressed:
                if self.getSelection() and self.getSelectedText() != -1:
                    pyperclip.copy(self.getSelectedText())
            elif key == pygame.K_v and self._controlPressed:
                if self.getSelection() and self.getSelectedText() != -1:
                    self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                    self.setSelectionPos(0, 0)
                self.appendText(pyperclip.paste())
            elif key == pygame.K_x and self._controlPressed:
                if self.getSelection() and self.getSelectedText() != -1:
                    pyperclip.copy(self.getSelectedText())
                    self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                    self.setSelectionPos(0, 0)

        if key == pygame.K_RCTRL or key == pygame.K_LCTRL:
            self._controlPressed = True
        elif key == pygame.K_RSHIFT or key == pygame.K_LSHIFT:
            self._baseSelection = self.getCursorPosition()
            self._shiftPressed = True

    def _isNotFocusedAnymore(self): #Function usefull for heritage, call by MApp when the widget is not focused anymore
        self._bottomArrowPressed = False
        self._bottomArrowPressedTime = 0
        self._bottomArrowNumber = 0
        self._backspacePressed = False
        self._backspacePressedTime = 0
        self._backspaceNumber = 0
        self._controlPressed = False
        self._leftArrowPressed = False
        self._leftArrowPressedTime = 0
        self._leftArrowNumber = 0
        self._returnPressed = False
        self._returnPressedTime = 0
        self._returnNumber = 0
        self._rightArrowPressed = False
        self._rightArrowPressedTime = 0
        self._rightArrowNumber = 0
        self._shiftPressed = False
        self._topArrowPressed = False
        self._topArrowPressedTime = 0
        self._topArrowNumber = 0
        
        self.setSelectionPos(0, 0)

        if self.getCursorVisible() or self.getSelection():
            self.setShouldModify(True)

    def _isTextGettingEntered(self, text): #Function usefull for heritage, call by MApp when the widget is focused and the user is entering a text (applicated for only one frame)
        if self.getInput():
            if self.getSelection() and self.getSelectedText() != -1:
                self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                self.setSelectionPos(0, 0)
            self.appendText(text)

    def _mouseMove(self, buttons, pos, relativeMove): #Function usefull for heritage, call by MApp when the widget is focused and the mouse is moving
        if buttons.count(1) > 0:
            if self.getCursorVisible() or self.getSelection():
                cursorPos = self._getPositionAtPos(pygame.font.SysFont(self.font, self.fontSize), pos)
                if self.getCursorVisible():
                    self.setCursorPosition(cursorPos)
                if self.getSelection():
                    if cursorPos >= self.getSelectionStop():
                        self.setSelectionPos(self._baseSelection, cursorPos)
                    else:
                        self.setSelectionPos(cursorPos, self._baseSelection)

    def _mouseWheel(self, rotation): #Function usefull for heritage, call by MApp when the widget is focused and the wheel is rotating
        multiplicator = 30
        if self._controlPressed:
            self.setTextX(self.getTextX() + rotation * multiplicator)
        else:
            self.setTextY(self.getTextY() + rotation * multiplicator)

    def _removeTextAtPos(self, length, pos): #Remove a length-sized piece of text at the cursor
        firstI = pos - length
        if firstI <= -1:
            firstI = 0
        if self.getCursorPosition() >= pos:
            self.setCursorPosition(self.getCursorPosition() - length)
        elif self.getCursorPosition() >= pos - length:
            self.setCursorPosition(pos - length)
        self.setText(self.getText()[:firstI] + self.getText()[pos:])

    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        surface = super()._renderBeforeHierarchy(surface)

        generator = self.getGenerator()
        heightCursor = generator.size(" ")[1]
        x = self.getFrameWidth(1) + self.getTextOffset(1)
        y = self.getFrameWidth(0) + self.getTextOffset(0)

        textSurface = self._renderTextImage(generator)
        surface.blit(textSurface, (x, y, textSurface.get_width(), textSurface.get_height()))

        if self.getCursorVisible() and self._getCursorIsVisible() and self.getFocused(): #Draw cursor
            xCursor = self._getPositionX(generator, self.getCursorPosition())
            yCursor = self._getPositionY(generator, self.getCursorPosition())
            pygame.draw.rect(surface, (0, 0, 0), (xCursor, yCursor, self.getCursorWidth(), heightCursor))

        return surface
    
    def _renderTextImage(self, generator=0):
        if generator == 0:
            generator = self.getGenerator()

        x = 0
        y = 0
        
        if self.getTextVerticalAlignment() == 2:
            y = self.getHeight()

        surfaces, textYStart = self._getTextRendered(all=False, generator=generator) #Get the text rendered into surface
        textHeight = 0
        for textSurface in surfaces:
            textHeight += textSurface.get_height()

        surface = pygame.Surface(self._getTextDisplaySize(), pygame.SRCALPHA)

        if self.getTextVerticalAlignment() == 1: #Calculate y including vertical alignment particularity
            y = (surface.get_height()/2 - textHeight/2)

        if self.getTextVerticalAlignment() == 2:
            surfaces = surfaces[::-1]

        for textSurface in surfaces: #Place text
            if self.getTextHorizontalAlignment() == 1:
                x = ((surface.get_width())/2) - textSurface.get_width()/2
            elif self.getTextHorizontalAlignment() == 2:
                x = surface.get_width() - textSurface.get_width()

            if self.getTextVerticalAlignment() == 2:
                y -= textSurface.get_height()

            surface.blit(textSurface, (x + self.getTextX(), y, textSurface.get_width(), textSurface.get_height()))
            
            if self.getTextVerticalAlignment() != 2:
                y += textSurface.get_height()

        x = 0
        w = surface.get_width()
        if w < 0:
            w = 0
            x = 0

        surface = surface.subsurface((x, 0, w, surface.get_height()))
        surface = surface.subsurface((0, -textYStart, surface.get_width(), surface.get_height() + (textYStart)))

        return surface

    def _setCursorIsVisible(self, _cursorIsVisible): #Change the value of _cursorIsVisible
        if self._cursorIsVisible != _cursorIsVisible:
            self._cursorIsVisible = _cursorIsVisible
            self.setShouldModify(True)

    def _update(self, deltaTime):

        if self._backspacePressed:
            self._backspacePressedTime += deltaTime
            if self._backspacePressedTime > 0.5:
                n = (self._backspacePressedTime - 0.5)*10
                if math.ceil(n) >= self._backspaceNumber:
                    self._doBackspaceEffet()
                    self._backspaceNumber += 0.5

        if self._bottomArrowPressed:
            self._bottomArrowPressedTime += deltaTime
            if self._bottomArrowPressedTime > 0.5:
                n = (self._bottomArrowPressedTime - 0.5)*10
                if math.ceil(n) >= self._bottomArrowNumber:
                    self._bottomArrowPressedAtThisFrame = True
                    self._bottomArrowNumber += 0.5
                    self._cursorBottom()

        if self._leftArrowPressed:
            self._leftArrowPressedTime += deltaTime
            if self._leftArrowPressedTime > 0.5:
                n = (self._leftArrowPressedTime - 0.5)*10
                if math.ceil(n) >= self._leftArrowNumber:
                    self._cursorLeft()
                    self._cursorVisibleTime = 0
                    self._setCursorIsVisible(True)
                    self._leftArrowNumber += 0.5

        if self._returnPressed:
            self._returnPressedTime += deltaTime
            if self._returnPressedTime > 0.5:
                n = (self._returnPressedTime - 0.5)*10
                if math.ceil(n) >= self._returnNumber:
                    if self.getSelection() and self.getSelectedText() != -1:
                        self._removeTextAtPos(len(self.getSelectedText()), self.getSelectionStop())
                        self.setSelectionPos(0, 0)
                    self.appendText("\n")
                    self._returnNumber += 0.5

        if self._rightArrowPressed:
            self._rightArrowPressedTime += deltaTime
            if self._rightArrowPressedTime > 0.5:
                n = (self._rightArrowPressedTime - 0.5)*10
                if math.ceil(n) >= self._rightArrowNumber:
                    self._cursorRight()
                    self._cursorVisibleTime = 0
                    self._setCursorIsVisible(True)
                    self._rightArrowNumber += 0.5

        if self._topArrowPressed:
            self._topArrowPressedTime += deltaTime
            if self._topArrowPressedTime > 0.5:
                n = (self._topArrowPressedTime - 0.5)*10
                if math.ceil(n) >= self._topArrowNumber:
                    self._topArrowPressedAtThisFrame = True
                    self._topArrowNumber += 0.5
                    self._cursorTop()

        if self.getCursorVisible() and self.getFocused():
            self._cursorVisibleTime += deltaTime
            if self._cursorVisibleTime >= self._cursorFlashingTime:
                self._cursorVisibleTime -= self._cursorFlashingTime
                self._setCursorIsVisible(not self._cursorIsVisible)

###################### Secondary class to create a simple button
class MButton(MText):
    def __init__(self, text, x, y, width, height, parent, widgetType="MButton"):
        super().__init__(text, x, y, width, height, parent, widgetType)

        self.backgroundColorOnOverflight = (210, 207, 200)
        self.changeBackgroundColorOnOnOverflight = False
        self.changeTextColorOnOnOverflight = False
        self.changeFontSizeOnOnOverflight = False
        self.leftClicked = False
        self.rightClicked = False
        self.fontSizeOnOverflight = 24
        self.textColorOnOverflight = (50, 47, 40)
        self._baseBackgroundColor = (0, 0, 0)
        self._baseFontSize = 0
        self._baseTextColor = (0, 0, 0)

        self.setBackgroundColor((180, 177, 170), True)
        self.setCursorOnOverflight(pygame.SYSTEM_CURSOR_HAND)
        self.setFontSize(22)
        self.setFrameWidth(1)
        self.setTextColor((0, 0, 0))
        self.setTextHorizontalAlignment(1)
        self.setTextVerticalAlignment(1)

    def getBackgroundColorOnOverflight(self):
        return self.backgroundColorOnOverflight

    def getChangeBackgroundColorOnOnOverflight(self):
        return self.changeBackgroundColorOnOnOverflight
    
    def getChangeFontSizeOnOnOverflight(self):
        return self.changeFontSizeOnOnOverflight
    
    def getChangeTextColorOnOnOverflight(self):
        return self.changeTextColorOnOnOverflight
    
    def getFontSizeOnOverflight(self):
        return self.fontSizeOnOverflight
    
    def getTextColorOnOverflight(self):
        return self.textColorOnOverflight

    def isGettingLeftClicked(self, oneFrame = True):
        if oneFrame:
            return self.mouseDown.count(1)
        return self.leftClicked
    
    def isGettingRightClicked(self, oneFrame = True):
        if oneFrame:
            return self.mouseDown.count(3)
        return self.rightClicked
    
    def setBackgroundColor(self, backgroundColor, notButton = True):
        if notButton:
            self._baseBackgroundColor = backgroundColor
            self.setBackgroundColor(backgroundColor, False)
        else:
            super().setBackgroundColor(backgroundColor, constant=True)

    def setBackgroundColorOnOverflight(self, backgroundColorOnOverflight):
        if self.backgroundColorOnOverflight != backgroundColorOnOverflight:
            self.backgroundColorOnOverflight = backgroundColorOnOverflight
            if self.getChangeBackgroundColorOnOnOverflight() and self.getOverflighted():
                self.setShouldModify(True)
    
    def setChangeBackgroundColorOnOnOverflight(self, changeBackgroundColorOnOnOverflight):
        if self.changeBackgroundColorOnOnOverflight != changeBackgroundColorOnOnOverflight:
            self.changeBackgroundColorOnOnOverflight = changeBackgroundColorOnOnOverflight
            if self.getOverflighted():
                self.setShouldModify(True)

    def setChangeFontSizeOnOnOverflight(self, changeFontSizeOnOnOverflight):
        if self.changeFontSizeOnOnOverflight != changeFontSizeOnOnOverflight:
            self.changeFontSizeOnOnOverflight = changeFontSizeOnOnOverflight
            if self.getOverflighted():
                self.setShouldModify(True)

    def setChangeTextColorOnOnOverflight(self, changeTextColorOnOnOverflight):
        if self.changeTextColorOnOnOverflight != changeTextColorOnOnOverflight:
            self.changeTextColorOnOnOverflight = changeTextColorOnOnOverflight
            if self.getOverflighted():
                self.setShouldModify(True)

    def setFontSize(self, fontSize, notButton = True):
        if notButton:
            self._baseFontSize = fontSize
            self.setFontSize(fontSize, False)
        else:
            super().setFontSize(fontSize)

    def setFontSizeOnOverflight(self, fontSizeOnOverflight):
        if self.fontSizeOnOverflight != fontSizeOnOverflight:
            self.fontSizeOnOverflight = fontSizeOnOverflight
            if self.getChangeFontSizeOnOnOverflight() and self.getOverflighted():
                self.setShouldModify(True)

    def setTextColor(self, textColor, notButton = True):
        if notButton:
            self._baseTextColor = textColor
            self.setTextColor(textColor, False)
        else:
            super().setTextColor(textColor)

    def setTextColorOnOverflight(self, textColorOnOverflight):
        if self.textColorOnOverflight != textColorOnOverflight:
            self.textColorOnOverflight = textColorOnOverflight
            if self.getChangeTextColorOnOnOverflight() and self.getOverflighted():
                self.setShouldModify(True)

    def _doNotOverflightedEffect(self):
        self.setBackgroundColor(self._baseBackgroundColor)
        self.setFontSize(self._baseFontSize)
        self.setTextColor(self._baseTextColor)

    def _doOverflightedEffect(self):
        if self.getChangeBackgroundColorOnOnOverflight():
            self.setBackgroundColor(self.getBackgroundColorOnOverflight(), False)

        if self.getChangeFontSizeOnOnOverflight():
            self.setFontSize(self.getFontSizeOnOverflight(), False)

        if self.getChangeTextColorOnOnOverflight():
            self.setTextColor(self.getTextColorOnOverflight(), False)
    
    def _isGettingMouseDown(self, button, relativePos):
        if button == 1:
            self.leftClicked = True
        elif button == 3:
            self.rightClicked = True

    def _isGettingMouseUp(self, button, relativePos):
        if button == 1:
            self.leftClicked = False
        elif button == 3:
            self.rightClicked = False

    def _isGettingOverflighted(self, relativePos):
        self._doOverflightedEffect()

    def _isNotFocusedAnymore(self):
        self.leftClicked = False
        self.rightClicked = False

    def _isNotOverflightedAnymore(self):
        self._doNotOverflightedEffect()

###################### Secondary class which represents slider
class MSlider(MFrame):
    ORIENTATION_BOTTOM_TO_TOP = 3
    ORIENTATION_LEFT_TO_RIGHT = 0
    ORIENTATION_RIGHT_TO_LEFT = 2
    ORIENTATION_TOP_TO_BOTTOM = 1

    def __init__(self, orientation, minValue, maxValue, x, y, width, height, parent, widgetType="MSlider"): #Construct an MSlider object
        super().__init__(x, y, width, height, parent, widgetType)

        self.buttonBackgroundColor = (130, 127, 120)
        self.buttonBackgroundColorOnOverflight = (180, 177, 170)
        self.buttonOrientationLength = (self.getHeight() - 2) / 10
        if orientation == MSlider.ORIENTATION_LEFT_TO_RIGHT or orientation == MSlider.ORIENTATION_RIGHT_TO_LEFT:
            self.buttonOrientationLength = (self.getWidth() - 2) / 10
        self.changeButtonBackgroundColorOnOverflight = False
        self.maxValue = maxValue
        self.minValue = minValue
        self.posAtClick = (0, 0)
        self.step = 0
        self.value = minValue
        self.wheelMultiplicator = 10
        self.ORIENTATION = orientation
        self._buttonClicked = False
        self._buttonOverflighted = False
        self._valueChanged = False

        self.setChangeButtonBackgroundColorOnOverflight(True)
        self.setFrameWidth(1)

    def getButtonBackgroundColor(self): #Return buttonBackgroundColor
        return self.buttonBackgroundColor
    
    def getButtonBackgroundColorOnOverflight(self): #Return buttonBackgroundColorOnOverflight
        return self.buttonBackgroundColorOnOverflight
    
    def getButtonOrientationLength(self): #Return buttonOrientationLength
        return self.buttonOrientationLength
    
    def getButtonOrientationPos(self): #Return the orientation pos of the button
        frame1 = self.getFrameWidth(1)
        frame4 = self.getFrameWidth(3)
        if self.getOrientation() == 1:
            frame1 = self.getFrameWidth(0)
            frame4 = self.getFrameWidth(2)
        
        if self.getValue() <= self.getMinValue():
            if self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM or self.getOrientation() == MSlider.ORIENTATION_LEFT_TO_RIGHT:
                return 0
            return self.getOrientationAxisLength() - (self.getButtonOrientationLength())

        buttonNavigationLength = self.getWidth() - (frame1 + frame4)
        if self.getOrientation() == MSlider.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM:
            buttonNavigationLength = self.getHeight() - (frame1 + frame4)
        realButtonNavigationLength = buttonNavigationLength - self.getButtonOrientationLength()

        if self.getValue() >= self.getMaxValue():
            if self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM or self.getOrientation() == MSlider.ORIENTATION_LEFT_TO_RIGHT:
                return realButtonNavigationLength + frame1
            return 0

        valuePercentage = (self.getValue() - self.getMinValue()) / (self.getMaxValue() - self.getMinValue())

        if self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM or self.getOrientation() == MSlider.ORIENTATION_LEFT_TO_RIGHT:
            pos = realButtonNavigationLength * valuePercentage
        else:
            pos = realButtonNavigationLength * (1 - valuePercentage)

        return pos
    
    def getChangeButtonBackgroundColorOnOverflight(self): #Return changeButtonBackgroundColorOnOnOverflight
        return self.changeButtonBackgroundColorOnOverflight
    
    def getMaxValue(self): #Return maxValue
        return self.maxValue
    
    def getMinValue(self): #Return maxValue
        return self.minValue
    
    def getOrientation(self): #Return ORIENTATION
        return self.ORIENTATION
    
    def getOrientationAxisLength(self) -> float:
        """Return width or height depending on orientation

        Returns:
            float: width or height depending on orientation
        """
        if self.getOrientation() == MSlider.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM:
            return self.getHeight()
        else:
            return self.getWidth()

    def getStep(self): #Return step
        return self.step
    
    def getValue(self): #Return maxValue
        return self.value
    
    def getValueChanded(self): #Return _valueChanged
        return self._valueChanged
    
    def getWheelMultiplicator(self): #Return wheelMultiplicator
        return self.wheelMultiplicator

    def isValueIn(self, value): #Return if value is between minValue and maxValue
        return value >= self.getMinValue() and value <= self.getMaxValue()
    
    def setChangeButtonBackgroundColorOnOverflight(self, changeButtonBackgroundColorOnOverflight): #Return buttonBackgroundColorOnOverflight
        if self.getChangeButtonBackgroundColorOnOverflight() != changeButtonBackgroundColorOnOverflight:
            self.changeButtonBackgroundColorOnOverflight = changeButtonBackgroundColorOnOverflight
            if self._buttonOverflighted:
                self.setShouldModify(True)
    
    def setButtonBackgroundColor(self, buttonBackgroundColor): #Change the value of buttonBackground
        if self.getButtonBackgroundColor() != buttonBackgroundColor:
            self.buttonBackgroundColor = buttonBackgroundColor
            self.setShouldModify(True)

    def setButtonBackgroundColorOnOverflight(self, buttonBackgroundColorOnOverflight): #Change the value of buttonBackgroundOnOverflight
        if self.getButtonBackgroundColorOnOverflight() != buttonBackgroundColorOnOverflight:
            self.buttonBackgroundColorOnOverflight = buttonBackgroundColorOnOverflight
            self.setShouldModify(True)

    def setButtonOrientationLength(self, buttonOrientationLength: int): #Change the value of buttonOrientationLength
        if self.getButtonOrientationLength() != buttonOrientationLength:
            self.buttonOrientationLength = buttonOrientationLength
            self.setShouldModify(True)
    
    def setMaxValue(self, maxValue: int): #Change the value of maxValue
        if self.getMaxValue() != maxValue and maxValue >= self.getMinValue() and self.getValue() <= maxValue:
            self.maxValue = maxValue
            self.setShouldModify(True)
    
    def setMinValue(self, minValue: int): #Change the value of maxValue
        if self.getMinValue() != minValue and minValue <= self.getMaxValue() and self.getValue() >= minValue:
            self.minValue = minValue
            self.setShouldModify(True)
    
    def setStep(self, step: int): #Change the value of step
        if self.getStep() != step:
            if step != 0:
                range = self.getMaxValue() - self.getMinValue()
                if range/step == round(range/step):
                    self.step = step
                    self.setValue(self.getMinValue())
                    self.setWheelMultiplicator(step)
                    self.setShouldModify(True)
            else:
                self.step = 0
    
    def setValue(self, value: int): #Change the value of value
        if self.getValue() != value:
            if value > self.getMaxValue():
                value = self.getMaxValue()
            elif value < self.getMinValue():
                value = self.getMinValue()
            self.value = value
            self._valueChanged = True
            self.setShouldModify(True)

    def setWheelMultiplicator(self, wheelMultipilcator: int): #Change the value of wheelMultiplicator
        self.wheelMultiplicator = wheelMultipilcator

    def softResetWidget(self): #Reset some attributes without graphics modification
        super().softResetWidget()
        self._valueChanged = False

    def _doNotOverflightEffect(self): #Apply effect on the MSlider when not overflighted by the cursor
        if self._buttonOverflighted:
            self._buttonOverflighted = False
            self.setShouldModify(True)

    def _doOverflightEffect(self, relativePos: tuple): #Apply effect on the MSlider when overflighted by the cursor
        if self._isPosOverButton(relativePos):
            if not self._buttonOverflighted:
                self._buttonOverflighted = True
                self.setShouldModify(True)
        else:
            if self._buttonOverflighted:
                self._buttonOverflighted = False
                self.setShouldModify(True)

    def _getValueAtPos(self, relativePos: tuple): #Return the value at a relative pos
        frame1 = self.getFrameWidth(1)
        frame4 = self.getFrameWidth(3)
        if self.getOrientation() == 1:
            frame1 = self.getFrameWidth(0)
            frame4 = self.getFrameWidth(2)

        if self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM or self.getOrientation() == MSlider.ORIENTATION_LEFT_TO_RIGHT:
            if relativePos <= frame1 + self.getButtonOrientationLength() / 2:
                return self.getMinValue()
        else:
            if relativePos >= self.getOrientationAxisLength() - (frame4 + self.getButtonOrientationLength() / 2):
                return self.getMinValue()

        buttonNavigationLength = self.getOrientationAxisLength() - (frame1 + frame4)
        realButtonNavigationLength = buttonNavigationLength - self.getButtonOrientationLength()

        if self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM or self.getOrientation() == MSlider.ORIENTATION_LEFT_TO_RIGHT:
            if relativePos >= buttonNavigationLength - frame1:
                return self.getMaxValue()
        else:
            if relativePos <= frame1:
                return self.getMaxValue()

        relativePos -= frame1 + self.getButtonOrientationLength()/2

        if self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM or self.getOrientation() == MSlider.ORIENTATION_LEFT_TO_RIGHT:
            toReturn = (relativePos / realButtonNavigationLength) * (self.getMaxValue() - self.getMinValue())
        else:
            toReturn = (1 - relativePos / realButtonNavigationLength) * (self.getMaxValue() - self.getMinValue())

        if self.getStep() != 0:
            toReturn = self.getStep() * round(toReturn/self.getStep())

        return round(toReturn)

    def _isGettingMouseDown(self, button: list, relativePos: tuple): #Function usefull for heritage, call by MApp when the widget is clicked (called for only one frame) with button = left button (1) and right button (2)
        if button == 1:
            self.posAtClick = (relativePos[0], self.getButtonOrientationPos())
            if self.getOrientation() == MSlider.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM:
                self.posAtClick = (relativePos[1], self.getButtonOrientationPos())
            if self._isPosOverButton(relativePos):
                self._buttonClicked = True
            else:
                toAdd = relativePos[0]
                if self.getOrientation() == MSlider.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM:
                    toAdd = relativePos[1]
                toAdd = self._getValueAtPos(toAdd)
                if toAdd > self.getMaxValue(): toAdd = self.getMaxValue()
                if toAdd < self.getMinValue(): toAdd = self.getMinValue(())
                self.setValue(toAdd)

    def _isGettingMouseUp(self, button: list, relativePos: tuple): #Function usefull for heritage, call by MApp when the widget is not clicked anymore (called for only one frame) with button = left button (1) and right button (2)
        if button == 1:
            self._buttonClicked = False

    def _isGettingOverflighted(self, relativePos: tuple): #Function usefull for heritage, call by MApp when the widget is overflighted (applicated for only one frame)
        self._doOverflightEffect(relativePos)

    def _isNotOverflightedAnymore(self): #Function usefull for heritage, call by MApp when the widget is not overflighted anymore
        self._doNotOverflightEffect()

    def _isPosOverButton(self, relativePos: tuple): #Return if pos overflight the button or not
        good = True #Check if the cursor is overflighting the button
        if self.getOrientation() == MSlider.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM: #Vertical
            good = relativePos[0] >= self.getFrameWidth(1) and relativePos[0] <= self.getWidth() - self.getFrameWidth(3)
            good = good and relativePos[1] >= self.getButtonOrientationPos() and relativePos[1] <= self.getButtonOrientationPos() + self.getButtonOrientationLength()
        else: #Horizontal
            good = relativePos[1] >= self.getFrameWidth(0) and relativePos[1] <= self.getHeight() - self.getFrameWidth(2)
            good = good and relativePos[0] >= self.getButtonOrientationPos() and relativePos[0] <= self.getButtonOrientationPos() + self.getButtonOrientationLength()
        
        return good
    
    def _mouseMove(self, buttons: list, pos: tuple, relativeMove: tuple): #Function usefull for heritage, call by MApp when the widget is focused and the mouse is moved
        if self._buttonClicked:
            toAdd = pos[0]
            if self.getOrientation() == MSlider.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MSlider.ORIENTATION_TOP_TO_BOTTOM:
                toAdd = pos[1]
            toAdd -= self.posAtClick[0]
            self.setValue(round(self._getValueAtPos((self.posAtClick[1] + self.getButtonOrientationLength() / 2) + toAdd)))

    def _mouseWheel(self, rotation): #Function usefull for heritage, call by MApp when the widget is focused nad the mosue whell is rotating
        if not self._buttonClicked:
            self.setValue(self.getValue() - rotation * self.getWheelMultiplicator())

    def _renderBeforeHierarchy(self, surface: pygame.Surface): #Render widget on surface before hierarchy render
        surface = super()._renderBeforeHierarchy(surface)

        #Calculate button position
        finalRect = (self.getFrameWidth(1), self.getFrameWidth(0) + self.getButtonOrientationPos(), self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)), self.getButtonOrientationLength())
        if self.getOrientation() == MSlider.ORIENTATION_LEFT_TO_RIGHT or self.getOrientation() == MSlider.ORIENTATION_RIGHT_TO_LEFT:
            finalRect = (self.getFrameWidth(1) + self.getButtonOrientationPos(), self.getFrameWidth(0), self.getButtonOrientationLength(), self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2)))

        #Choose button color
        buttonBackgroundColor = self.getButtonBackgroundColor()
        if self._buttonOverflighted and self.getChangeButtonBackgroundColorOnOverflight():
            buttonBackgroundColor = self.getButtonBackgroundColorOnOverflight()

        pygame.draw.rect(surface, buttonBackgroundColor, finalRect)

        return surface
    
###################### Secondary class which represents an area where we can make a widget scroll in it
class MScrollArea(MWidget):
    def __init__(self, widgetToScroll, x, y, width, height, parent, widgetType="MScrollArea"): #Construct an MScrollArea object
        super().__init__(x, y, width, height, parent, widgetType)
        self.sliderOrientationLength = 15
        self.horizontalSlider = MSlider(0, 0, 10, self.sliderOrientationLength, self.getHeight() - self.sliderOrientationLength, self.getWidth() - (self.sliderOrientationLength), self.sliderOrientationLength, self)
        self.verticalSlider = MSlider(1, 0, 10, 0, 0, self.sliderOrientationLength, self.getHeight() - (self.sliderOrientationLength), self)
        self.widgetToScroll = 0
        self._shiftPressed = False
        self._widgetToScrollOffset = (self.sliderOrientationLength, self.sliderOrientationLength)

        self.horizontalSlider.setChangeButtonBackgroundColorOnOverflight(True)
        self.horizontalSlider.setVisible(False)
        self.verticalSlider.setChangeButtonBackgroundColorOnOverflight(True)
        self.verticalSlider.setVisible(False)

        self.setWidgetToScroll(widgetToScroll)

    def getSliderOrientationLength(self): #Return sliderOrientationLength
        return self.sliderOrientationLength

    def getHorizontalSlider(self): #Return horizontalSlider
        return self.horizontalSlider
    
    def getVerticalSlider(self): #Return verticalSlider
        return self.verticalSlider
    
    def getWidgetToScroll(self): #Return widgetToScroll
        return self.widgetToScroll

    def placeSlider(self): #Place slider into the MScrollArea
        horizontalSliderNecessary = False
        verticalSliderNecessary = False

        if self.getWidgetToScroll() != 0:
            if self.getWidth() < self.getWidgetToScroll().getWidth():
                horizontalSliderNecessary = True

            if self.getHeight() - (self.getSliderOrientationLength() * horizontalSliderNecessary) < self.getWidgetToScroll().getHeight():
                verticalSliderNecessary = True

            if self.getWidth() - (self.getSliderOrientationLength() * verticalSliderNecessary) < self.getWidgetToScroll().getWidth():
                horizontalSliderNecessary = True

        if horizontalSliderNecessary:
            self._widgetToScrollOffset = (0, self.sliderOrientationLength)
        else:
            self._widgetToScrollOffset = (0, 0)

        if verticalSliderNecessary:
            self._widgetToScrollOffset = (self.sliderOrientationLength, self._widgetToScrollOffset[1])
        else:
            self._widgetToScrollOffset = (0, self._widgetToScrollOffset[1])

        if horizontalSliderNecessary:
            if not self.getHorizontalSlider().getVisible():
                maxValue = self.getWidgetToScroll().getWidth() - (self.getWidth() - (self._widgetToScrollOffset[0]))

                self.getHorizontalSlider().setVisible(True)

                bolRatio = (self.getWidth()) / self.getWidgetToScroll().getWidth()
                self.getHorizontalSlider().setButtonOrientationLength((self.getHorizontalSlider().getWidth()) * bolRatio)
                self.getHorizontalSlider().setMinValue(0)
                self.getHorizontalSlider().setMaxValue(maxValue)

            if verticalSliderNecessary:
                self.getHorizontalSlider().setX(self.sliderOrientationLength)
                self.getHorizontalSlider().setWidth(self.getWidth() - self.sliderOrientationLength)
            else:
                self.getHorizontalSlider().setX(0)
                self.getHorizontalSlider().setWidth(self.getWidth())
        else:
            if self.getHorizontalSlider().getVisible():
                self.getHorizontalSlider().setVisible(False)

        if verticalSliderNecessary:
            if not self.getVerticalSlider().getVisible():
                maxValue = self.getWidgetToScroll().getHeight() - (self.getHeight() - (self._widgetToScrollOffset[1]))

                self.getVerticalSlider().setVisible(True)

                bolRatio = (self.getHeight()) / self.getWidgetToScroll().getHeight()
                self.getVerticalSlider().setButtonOrientationLength((self.getVerticalSlider().getHeight()) * bolRatio)
                self.getVerticalSlider().setMinValue(0)
                self.getVerticalSlider().setMaxValue(maxValue)

            if horizontalSliderNecessary:
                self.getVerticalSlider().setHeight(self.getHeight() - self.sliderOrientationLength)
            else:
                self.getVerticalSlider().setHeight(self.getHeight())
        else:
            if self.getVerticalSlider().getVisible():
                self.getVerticalSlider().setVisible(False)

        if self.getWidgetToScroll() != 0:
            self.getWidgetToScroll().move(self._widgetToScrollOffset[0], 0)

    def reload(self): #Reload the MScrollArea after widgetToScroll edit
        temp = self.getWidgetToScroll()
        self.setWidgetToScroll(0)
        self.setWidgetToScroll(temp)

    def setWidgetToScroll(self, widgetToScroll: MWidget): #Change widgetToScroll
        if self.getWidgetToScroll() != widgetToScroll:
            self.widgetToScroll = widgetToScroll
            if widgetToScroll != 0:
                if widgetToScroll.getParent() != self:
                    widgetToScroll.setParent(self)
                    self.promoveChild(self.horizontalSlider)
                    self.promoveChild(self.verticalSlider)
                widgetToScroll.move(self._widgetToScrollOffset[0], 0)
                widgetToScroll.setIgnoreUserEvent(True)
            self.placeSlider()

    def _isKeyGettingDropped(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is dropped on the keyboard (applicated for only one frame)
        if key == pygame.K_RSHIFT or key == pygame.K_LSHIFT:
            self._shiftPressed = False

    def _isKeyGettingPressed(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is pressed on the keyboard (applicated for only one frame)
        if key == pygame.K_RSHIFT or key == pygame.K_LSHIFT:
            self._shiftPressed = True

    def _isNotFocusedAnymore(self): #Function usefull for heritage, call by MApp when the widget is not focused anymore
        self._shiftPressed = False

    def _lastUpdate(self, deltaTime): #Function called every frame after event handle and user actions
        if self.widgetToScroll.isResized():
            self.reload()

    def _lateUpdate(self, deltaTime): #Function called every frame after event handle
        if self.getHorizontalSlider().getValueChanded():
            oldPos = (0, self.getWidgetToScroll().getY() - (self._widgetToScrollOffset[1]))
            newPos = (oldPos[0] + self._widgetToScrollOffset[0] - self.getHorizontalSlider().getValue(), oldPos[1] + self._widgetToScrollOffset[1])
            self.getWidgetToScroll().move(newPos[0], newPos[1])

        if self.getVerticalSlider().getValueChanded():
            oldPos = (self.getWidgetToScroll().getX() - (self._widgetToScrollOffset[0]), 0)
            newPos = (oldPos[0] + self._widgetToScrollOffset[0], oldPos[1] - self.getVerticalSlider().getValue())
            self.getWidgetToScroll().move(newPos[0], newPos[1])

    def _mouseWheel(self, rotation): #Function usefull for heritage, call by MApp when the widget is focused nad the mouse whell is rotating
        if self._shiftPressed:
            if self.getHorizontalSlider().getVisible():
                self.getHorizontalSlider()._mouseWheel(rotation)
        else:
            if self.getVerticalSlider().getVisible():
                self.getVerticalSlider()._mouseWheel(rotation)

###################### Secondary class which represents an symplified mtext for do text input on one line
class MTextInputLine(MText):
    def __init__(self, informationText, x, y, width, height, parent, widgetType="MTextInputLine"):
        super().__init__(informationText, x, y, width, height, parent, widgetType)

        self.informationColor = (70, 70, 70)
        self.informationText = informationText
        self.inputColor = (0, 0, 0)

        self.setForbiddenCaracter(["\n"])
        self.setFrameWidth(2)
        self.setInput(True)
        self.setTextColor(self.informationColor)
        self.setTextVerticalAlignment(1)

    def getInformationColor(self): #Return informationColor
        return self.informationColor

    def getInformationText(self): #Return informationText
        return self.informationText
    
    def getInputColor(self): #Return input color
        return self.inputColor
    
    def setInformationColor(self, informationColor): #Change the value of informationColor
        if self.informationColor != informationColor:
            self.informationColor = informationColor
            if self.getText() == self.getInformationText():
                self.setShouldModify(True)
    
    def setInformationText(self, informationText): #Change the value of informationText
        if self.informationText != informationText:
            lastInformationText = self.informationText
            self.informationText = informationText
            if (self.getText() == "" or self.getText() == lastInformationText) and not self.getFocused():
                self.setShouldModify(True)

    def setInputColor(self, inputColor): #Change the value of inputColor
        if self.inputColor != inputColor:
            self.inputColor = inputColor
            if self.getText() != self.informationText and self.getText() != "":
                self.setShouldModify(True)
    
    def _isGettingMouseDown(self, button, relativePos):
        if self.getText() == self.getInformationText():
            self.setText("")
        self.setTextColor(self.getInputColor())

        super()._isGettingMouseDown(button, relativePos)

    def _isNotFocusedAnymore(self):
        super()._isNotFocusedAnymore()

        if self.getText() == "":
            self.setTextColor(self.getInformationColor())
            self.setText(self.getInformationText())

###################### Secondary class which represents an informational bar
class MBar(MFrame):
    ORIENTATION_BOTTOM_TO_TOP = 3
    ORIENTATION_LEFT_TO_RIGHT = 0
    ORIENTATION_RIGHT_TO_LEFT = 2
    ORIENTATION_TOP_TO_BOTTOM = 1

    def __init__(self, orientation: int, x: int, y: int, width: int, height: int, parent: MWidget, widgetType: str ="MBar") -> None:
        """Construct an MBar object

        Args:
            orientation (int): orientation of the bar (0 if horizontal from left to right, 1 if vertical from top to bottom, 2 if horizontal from right to left, 3 if vertical from bottom to top)
            x (int): x position of the bar
            y (int): y position of the bar
            width (int): width of the bar
            height (int): height of the bar
            parent (MWidget): parent of the bar
            widgetType (str, optional): type of the bar. Defaults to "MBar".
        """
        super().__init__(x, y, width, height, parent, widgetType)

        self.animation = True
        self.animationColor = (0, 180, 0)
        self.animationSpeed = 100
        self.barColor = (0, 255, 0)
        self.maxValue = 100
        self.minValue = 0
        self.ORIENTATION = orientation
        self.value = 0
        self._animationSize = round(self.getWidth()/10)
        if self.getOrientation() == MBar.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MBar.ORIENTATION_TOP_TO_BOTTOM:
            self._animationSize = round(self.getHeight()/10)
        self._animationState = 0

        self.setFrameWidth(1)

    def barRect(self) -> tuple:
        surfaceRect = (self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)), self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2)))

        barHeight = surfaceRect[1]
        barWidth = surfaceRect[0]
        barX = 0
        barY = 0

        if self.getOrientation() == MBar.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MBar.ORIENTATION_TOP_TO_BOTTOM:
            barHeight *= ((self.getValue()-self.getMinValue())/self.getRange())
            barHeight = round(barHeight)
            if self.getOrientation() == MBar.ORIENTATION_BOTTOM_TO_TOP:
                barY = surfaceRect[1] - barHeight
        else:
            barWidth *= ((self.getValue()-self.getMinValue())/self.getRange())
            barWidth = round(barWidth)
            if self.getOrientation() == MBar.ORIENTATION_RIGHT_TO_LEFT:
                barX = surfaceRect[0] - barWidth

        return (barX, barY, barWidth, barHeight)

    def barSurface(self) -> pygame.Surface:
        """Return the surface with the progression bar drew

        Returns:
            pygame.Surface: surface with the progession bar drew
        """
        surface = pygame.Surface((self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)), self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2))), pygame.SRCALPHA)

        barX, barY, barWidth, barHeight = self.barRect()

        pygame.draw.rect(surface, self.getBarColor(), (barX, barY, barWidth, barHeight))

        heightAnim = 0 #Calculate animation rect
        xAnim = 0
        yAnim= 0
        widthAnim = 0

        if self.getOrientation() == MBar.ORIENTATION_BOTTOM_TO_TOP:
            widthAnim = self.getWidth()
            yAnim = self.getHeight() - self._animationState
        elif self.getOrientation() == MBar.ORIENTATION_TOP_TO_BOTTOM:
            widthAnim = self.getWidth()
            yAnim = self._animationState
        elif self.getOrientation() == MBar.ORIENTATION_LEFT_TO_RIGHT:
            heightAnim = self.getHeight()
            xAnim = self._animationState
        else:
            heightAnim = self.getHeight()
            xAnim = self.getWidth() - self._animationState

        for i in range(math.ceil(self._animationSize/2)): #Drawing animation
            ratio = 1-(i / math.ceil(self._animationSize/2))

            color = (self.getBarColor()[0] + (self.getAnimationColor()[0] - self.getBarColor()[0]) * ratio, self.getBarColor()[1] + (self.getAnimationColor()[1] - self.getBarColor()[1]) * ratio, self.getBarColor()[2] + (self.getAnimationColor()[2] - self.getBarColor()[2]) * ratio)
            if self.getOrientation() == MBar.ORIENTATION_TOP_TO_BOTTOM:
                if yAnim - i <= barHeight:
                    pygame.draw.line(surface, color, (xAnim, yAnim - i), (xAnim + widthAnim, yAnim - i))
                if yAnim + i <= barHeight:
                    pygame.draw.line(surface, color, (xAnim, yAnim + i), (xAnim + widthAnim, yAnim + i))
            elif self.getOrientation() == MBar.ORIENTATION_BOTTOM_TO_TOP:
                if yAnim - i >= surface.get_height() - barHeight:
                    pygame.draw.line(surface, color, (xAnim, yAnim - i), (xAnim + widthAnim, yAnim - i))
                if yAnim + i >= surface.get_height() - barHeight:
                    pygame.draw.line(surface, color, (xAnim, yAnim + i), (xAnim + widthAnim, yAnim + i))
            elif self.getOrientation() == MBar.ORIENTATION_LEFT_TO_RIGHT:
                if xAnim - i <= barWidth:
                    pygame.draw.line(surface, color, (xAnim - i, yAnim), (xAnim - i, yAnim + heightAnim))
                if xAnim + i <= barWidth:
                    pygame.draw.line(surface, color, (xAnim + i, yAnim), (xAnim + i, yAnim + heightAnim))
            else:
                if xAnim - i >= surface.get_width() - barWidth:
                    pygame.draw.line(surface, color, (xAnim - i, yAnim), (xAnim - i, yAnim + heightAnim))
                if xAnim + i >= surface.get_width() - barWidth:
                    pygame.draw.line(surface, color, (xAnim + i, yAnim), (xAnim + i, yAnim + heightAnim))

        return surface
    
    def getAnimation(self) -> bool:
        """Return if an animation is played

        Returns:
            bool: if an animation is played
        """
        return self.animation
    
    def getAnimationColor(self) -> tuple:
        """Return the color of the animation part

        Returns:
            tuple: color of the animation part
        """
        return self.animationColor
    
    def getAnimationSpeed(self) -> float:
        """Return the animation speed

        Returns:
            float: animation speed
        """
        return self.animationSpeed
    
    def getBarColor(self) -> tuple:
        """Return the bar color

        Returns:
            tuple: bar color
        """
        return self.barColor
    
    def getBarLengthInOrientationAxis(self) -> float:
        """Return the size of the bar in the orientation axis

        Returns:
            float: size of the bar in the orientation axis
        """
        return self.barRect()[2] if (self.getOrientation() == MBar.ORIENTATION_LEFT_TO_RIGHT or self.getOrientation() == MBar.ORIENTATION_RIGHT_TO_LEFT) else self.barRect()[3]

    def getMaxValue(self) -> float:
        """Return the maximum value storable into the MBar

        Returns:
            float: the maximum value storable into the MBar
        """
        return self.maxValue
    
    def getMinValue(self) -> float:
        """Return the minimum value storable into the MBar

        Returns:
            float: the minimum value storable into the MBar
        """
        return self.minValue
    
    def getRange(self) -> float:
        """Return the range of value in the MBar

        Returns:
            float: range of value in the MBar
        """
        return self.getMaxValue() - self.getMinValue()
    
    def getOrientation(self) -> int:
        """Return orientation of the MBar

        Returns:
            int: orientation of the MBar
        """
        return self.ORIENTATION
    
    def getOrientationAxisLength(self) -> float:
        """Return width or height depending on orientation

        Returns:
            float: width or height depending on orientation
        """
        if self.getOrientation() == MBar.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MBar.ORIENTATION_TOP_TO_BOTTOM:
            return self.getHeight()
        else:
            return self.getWidth()

    def getValue(self) -> float:
        """Return the value stored into the the MBar

        Returns:
            float: the value stored into the the MBar
        """
        return self.value
    
    def setAnimation(self, animation: bool) -> None:
        """Change the value that if the animation is played

        Args:
            animation (bool): new value of if animation is played
        """
        if self.getAnimation() != animation:
            self.animation = True

    def setAnimationColor(self, animationColor: str) -> None:
        """Change the animation color

        Args:
            animationColor (str): new animation color
        
        """
        if self.getAnimationColor() != animationColor:
            self.animationColor = animationColor
            if self.getAnimation():
                self.setShouldModify(True)

    def setAnimationSpeed(self, animationSpeed: float) -> None:
        """Change the value of the animation speed

        Args:
            animationSpeed (float): new animation speed
        """
        if self.getAnimationSpeed()  != animationSpeed:
            self.animationSpeed = animationSpeed
    
    def setBarColor(self, barColor: tuple) -> None:
        """Change the value of the color of the bar

        Args:
            barColor (tuple): new color of the bar
        """
        if self.getBarColor() != barColor:
            self.barColor = barColor

    def setHeight(self, height: float) -> None:
        """Change the height of the widget

        Args:
            height (float): new height of the widget
        """
        super().setHeight(height)
        if self.getOrientation() == MBar.ORIENTATION_BOTTOM_TO_TOP or self.getOrientation() == MBar.ORIENTATION_TOP_TO_BOTTOM:
            self._animationSize = round(self.getHeight()/10)
    
    def setMaxValue(self, maxValue: float) -> None:
        """Change the maximum value storable into the MBar and change value if necessary

        Args:
            maxValue (float): new  maximum value storable into the MBar
        """
        if self.getMaxValue() != maxValue and self.getMinValue() < maxValue:
            self.maxValue = maxValue
            if self.getValue() > maxValue:
                self.setValue(maxValue)
            self.setShouldModify(True)

    def setMinValue(self, minValue: float) -> None:
        """Change the minimum value storable into the MBar and change value if necessary

        Args:
            minValue (float): new  minimum value storable into the MBar
        """
        if self.getMinValue() != minValue and self.getMaxValue() > minValue:
            self.minValue = minValue
            if self.getValue() < minValue:
                self.setValue(minValue)
            self.setShouldModify(True)
    
    def setValue(self, value: float) -> None:
        """Change the value stored into the MBar if value is between minValue and maxValue

        Args:
            value (float): new value to store into the MBar
        """
        if self.getValue() != value and value >= self.minValue and value <= self.maxValue:
            self.value = value
            self.setShouldModify(True)

    def setWidth(self, width: float) -> None:
        """Change the width of the widget

        Args:
            width (float): new width of the widget
        """
        super().setWidth(width)
        if self.getOrientation() == MBar.ORIENTATION_LEFT_TO_RIGHT or self.getOrientation() == MBar.ORIENTATION_RIGHT_TO_LEFT:
            self._animationSize = round(self.getWidth()/10)

    def _renderBeforeHierarchy(self, surface: pygame.Surface) -> pygame.Surface:
        """Draw the graphics element of this MBar

        Args:
            surface (pygame.Surface): surface to draw element

        Returns:
            pygame.Surface: surface after drawing element
        """
        surface = super()._renderBeforeHierarchy(surface)

        bar = self.barSurface()
        surface.blit(bar, (self.getFrameWidth(1), self.getFrameWidth(0), bar.get_width(), bar.get_height()))

        return surface
    
    def _update(self, deltaTime):
        if self.getAnimation():
            self._animationState += self.animationSpeed * deltaTime
            maxLength = self.getBarLengthInOrientationAxis()
            if self._animationState > maxLength:
                self._animationState -= maxLength
            if self._animationState < (self.getBarLengthInOrientationAxis()) or self._animationState - (self.getBarLengthInOrientationAxis()) < self._animationSize / 2:
                self.setShouldModify(True)

class MCheckBox(MObject):
    """Class which make check box creation easier, inherits from MObject
    """

    def __init__(self, app: MApp, objectType: str = "MCheckBox") -> None:
        """Construct an MCheckBox object

        Args:
            app (MApp): main app into the program
            objectType (str, optional): type of the object. Defaults to "MCheckBox".
        """
        super().__init__(app, objectType)
        self.actualChoice = ""
        self.baseDataByButton = {}
        self.buttonsByName = {}
        self.changeFrameColorOnChoice = False
        self.changeFrameWidthOnChoice = False
        self.frameColorOnChoice = (120, 120, 120)
        self.frameWidthOnChoice = 5
        self._lastChoice = ""
        self.nameByButton = {}
        self._isGettindChanged = False

    def addButton(self, name: str, button: MButton) -> None:
        """Add a new button into the MCheckBox

        Args:
            name (str): name of the button
            button (MButton): button to add
        """
        buttons = list(self.buttonsByName.values())
        names = list(self.nameByButton.values())
        if buttons.count(button) == 0 and names.count(name) == 0:
            datas = {"frameColor": button.getFrameColor(), "frameWidth": button.getFrameWidth()}

            self.baseDataByButton[button] = datas
            self.buttonsByName[name] = button
            self.nameByButton[button] = name

    def applyActionOnChoice(self) -> None:
        """Do all action to the chose button
        """
        if self.getActualChoice() != "":
            buttons = list(self.buttonsByName.values())
            for b in buttons:
                datas = self.baseDataByButton[b]
                b.setFrameColor(datas["frameColor"])
                b.setFrameWidth(datas["frameWidth"])

            if self.getChangeFrameColorOnChoice():
                self.buttonsByName[self.getActualChoice()].setFrameColor(self.getFrameColorOnChoice())

            if self.getChangeFrameWidthOnChoice():
                self.buttonsByName[self.getActualChoice()].setFrameWidth(self.getFrameWidthOnChoice())

    def getActualChoice(self) -> str:
        """Return the actual choice

        Returns:
            str: actual choice
        """
        return self.actualChoice
    
    def getChangeFrameColorOnChoice(self) -> bool:
        """Return if the chose button change his frame color

        Returns:
            bool: if the chose button change his frame color
        """
        return self.changeFrameColorOnChoice
    
    def getChangeFrameWidthOnChoice(self) -> bool:
        """Return if the chose button change his frame width

        Returns:
            bool: if the chose button change his frame width
        """
        return self.changeFrameWidthOnChoice
    
    def getFrameColorOnChoice(self) -> tuple:
        """Return the color of the frame to apply to the chosen button

        Returns:
            tuple: color of the frame to apply to the chosen button
        """
        return self.frameColorOnChoice
    
    def getFrameWidthOnChoice(self) -> int:
        """Return the width of the frame to apply to the chosen button

        Returns:
            int: width of the frame to apply to the chosen button
        """
        return self.frameWidthOnChoice
    
    def isChoiceGettingChanged(self) -> tuple:
        """Return if the choice is changed and some information in a tuple

        Returns:
            tuple: tuple (if the choice is changed (only element if False), new choice, last choice)
        """
        if self._isGettindChanged:
            return (True, self.getActualChoice(), self._lastChoice)
        else:
            return (False,)
    
    def setActualChoice(self, actualChoice: str) -> None:
        """Change the value of the actuel choice

        Args:
            actualChoice (str): new actual choice
        """
        names = list(self.nameByButton.values())
        if self.getActualChoice() != actualChoice and names.count(actualChoice) > 0:
            self._lastChoice = self.getActualChoice()
            self.actualChoice = actualChoice
            self._isGettindChanged = True
            self.applyActionOnChoice()
    
    def setChangeFrameColorOnChoice(self, changeFrameColorOnChoice: bool) -> None:
        """Change if the chose button change his frame color

        Args:
            changeFrameColorOnChoice (bool): new if the chose button change his frame color
        """
        if self.getChangeFrameColorOnChoice() != changeFrameColorOnChoice:
            self.changeFrameColorOnChoice = changeFrameColorOnChoice
            self.applyActionOnChoice()

    def setChangeFrameWidthOnChoice(self, changeFrameWidthOnChoice: bool) -> None:
        """Change if the chose button change his frame width

        Args:
            changeFrameWidthOnChoice (bool): new if the chose button change his frame width
        """
        if self.getChangeFrameWidthOnChoice() != changeFrameWidthOnChoice:
            self.changeFrameWidthOnChoice = changeFrameWidthOnChoice
            self.applyActionOnChoice()

    def setFrameColorOnChoice(self, frameColorOnChoice: tuple) -> None:
        """Change the color to apply to the chosen button

        Args:
            frameColorOnChoice (tuple): new color to apply to the chosen button
        """
        if self.getFrameColorOnChoice() != frameColorOnChoice:
            self.frameColorOnChoice = frameColorOnChoice
            self.applyActionOnChoice()

    def setFrameWidthOnChoice(self, frameWidthOnChoice: int) -> None:
        """Change the width of the frame to apply to the chosen button

        Returns:
            int: new width of the frame to apply to the chosen button
        """
        if self.getFrameWidthOnChoice() != frameWidthOnChoice:
            self.frameWidthOnChoice = frameWidthOnChoice
            self.applyActionOnChoice()

    def softResetObject(self):
        self._isGettindChanged = False
    
    def _lateUpdate(self, deltaTime: float):
        """Function usefull for heritage, call by MApp every frame after event handle

        Args:
            deltaTime (float): time between the last frame and this frame
        """
        for b in self.nameByButton:
            if b.isGettingLeftClicked():
                self.setActualChoice(self.nameByButton[b])

class MChrono(MText):
    """Class which allow to do simple chronometer, inherits from MText
    """
    FORMAT_HH_MM_SS = 0
    FORMAT_HH_MM_CS = 1

    def __init__(self, format: int, x: int, y: int, width: int, height: int, parent: MWidget, widgetType: str ="MChrono") -> None:
        """Construct an MChrono object

        Args:
            format (int): format of the chronometer
            x (int): x pos of the widget
            y (int): y pos of the widget
            width (int): width of the widget
            height (int): height of the widget
            parent (MWidget): parent of the widget
            widgetType (str, optional): type of the widget. Defaults to "MChrono".
        """
        super().__init__("0", x, y, width, height, parent, widgetType)

        self.format = format
        self.importantTime = []
        self.speed = 1
        self.started = False
        self.unitSeparation = ":"
        self._nsToAdd = 0

        self.updateChronometer()

    def addNanoSecond(self, ns: float) -> None:
        """Add ns nanoseconds to the MChrono

        Args:
            ns (float): number of nanoseconds to add to the MChrono
        """
        self._nsToAdd += ns
        self.updateChronometer()

    def addSecond(self, second: float) -> None:
        """Add second seconds to the MChrono

        Args:
            second (float): number of seconds to add to the MChrono
        """
        self._nsToAdd += second*(10**9)
        self.updateChronometer()

    def getChronometerWithFormat(self) -> str:
        """Return the time since the chronometer is running with the correct format

        Returns:
            str: time since the chronometer is running with the correct format
        """
        if self.getFormat() == MChrono.FORMAT_HH_MM_SS:
            timeSinceStart = math.floor((math.floor(self.getTimeSinceStart(True)) * self.getSpeed() + self._nsToAdd)/(10**9))

            hour = 0
            while timeSinceStart >= 3600:
                timeSinceStart -= 3600
                hour += 1
            hourInStr = str(hour)
            if len(hourInStr) < 2: hourInStr = "0" + hourInStr

            minute = 0
            while timeSinceStart >= 60:
                timeSinceStart -= 60
                minute += 1
            minuteInStr = str(minute)
            if len(minuteInStr) < 2: minuteInStr = "0" + minuteInStr

            secondInStr = str(timeSinceStart)
            if len(secondInStr) < 2: secondInStr = "0" + secondInStr
            return hourInStr + self.getUnitSeparation() + minuteInStr + self.getUnitSeparation() + secondInStr
        elif self.getFormat() == MChrono.FORMAT_HH_MM_CS:
            timeSinceStart = math.floor((math.floor(self.getTimeSinceStart(True)) * self.getSpeed() + self._nsToAdd)/(10**7))

            minute = 0
            while timeSinceStart >= 6000:
                timeSinceStart -= 6000
                minute += 1
            minuteInStr = str(minute)
            if len(minuteInStr) < 2: minuteInStr = "0" + minuteInStr

            second = 0
            while timeSinceStart >= 100:
                timeSinceStart -= 100
                second += 1
            secondInStr = str(second)
            if len(secondInStr) < 2: secondInStr = "0" + secondInStr

            msInStr = str(timeSinceStart)
            if len(msInStr) < 2: msInStr = "0" + msInStr

            return minuteInStr + self.getUnitSeparation() + secondInStr + self.getUnitSeparation() + msInStr

    def getFormat(self) -> int:
        """Return the format of the chronometer

        Returns:
            int: format of the chronometer
        """
        return self.format
    
    def getSpeed(self) -> float:
        """Return the speed of the chronometer

        Returns:
            float: speed of the chronometer
        """
        return self.speed
    
    def getTimeSinceStart(self, ns: bool = True) -> float:
        """Return the amount of time passed since the first start

        Args:
            ns (bool, optional): if the return is in nano second or not. Defaults to True.

        Returns:
            float: amount of time passed since the first start
        """
        timePassed = 0

        if len(self.importantTime) % 2 == 0:
            for i in range(math.floor(len(self.importantTime)/2)):
                j = i * 2
                timePassed += self.importantTime[j + 1] - self.importantTime[j]
        else:
            for i in range(math.floor((len(self.importantTime) )/2)):
                j = i * 2
                timePassed += self.importantTime[j + 1] - self.importantTime[j]
            timePassed += time.time_ns() - self.importantTime[-1]

        if ns:
            return timePassed
        return timePassed/(10**9)

    def getUnitSeparation(self) -> str:
        """Return the separation of units

        Returns:
            str: separation of units
        """
        return self.unitSeparation
    
    def isStarted(self) -> bool:
        """Return if the chronometer is started or not

        Returns:
            bool: if the chronometer is started or not
        """
        return self.started
    
    def reset(self) -> None:
        """Reset the chronometer
        """
        started = self.isStarted()
        if started: self.stop()
        self.importantTime.clear()
        if started: self.start()
        self.updateChronometer()
    
    def setFormat(self, format: int) -> None:
        """Change the value of the format

        Args:
            format (int): new value of the format
        """
        if self.getFormat() != format:
            self.format = format
            self.updateChronometer()

    def setSpeed(self, speed: float) -> None:
        """Change the value of the speed of the chronometer

        Args:
            speed (float): value of the speed of the chronometer
        """
        if self.getSpeed() != speed and speed != 0:
            self.speed = speed

    def setUnitSeparation(self, unitSeparation: str) -> None:
        """Change the value of the separation of units

        Args:
            unitSeparation (str): value of the separation of units
        """
        if self.getUnitSeparation() != unitSeparation:
            self.unitSeparation = unitSeparation
            self.updateChronometer()

    def start(self, offset: int = 0) -> None:
        """Start the chronometer

        Args:
            offset (int): time in nanosecond where the chronometer should start
        """
        if not self.isStarted():
            self.importantTime.append(time.time_ns() - offset)
            self.started = True

    def stop(self) -> None:
        """Stop the chronometer
        """
        if self.isStarted():
            self.importantTime.append(time.time_ns())
            self.started = False

    def updateChronometer(self) -> None:
        """Update the chronometer text
        """
        newText = self.getChronometerWithFormat()
        self.setText(newText)

    def _update(self, deltaTime):
        if self.isStarted():
            self.updateChronometer()
