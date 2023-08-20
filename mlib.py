from pygame import *
import pygame
from time import time_ns

pygame.init()

#Nombre de widget existants
_nbWidget = 0

###################### Base widget class
class MWidget:
    def __init__(self, x, y, width, height, parent, widgetType = "MWidget"): #MWidget's constructor
        global _nbWidget
        self.backgroundColor = (255, 255, 255)
        self.cursorOnOverflight = pygame.SYSTEM_CURSOR_ARROW
        self.focused = False
        self.height = height
        self.mouseDown = -1
        self.mouseUp = -1
        self.overflighted = False
        self.parent = 0
        self.setShouldModify(True)
        self.visible = True
        self.width = width
        self.x = x
        self.y = y
        self._BACKGROUNDCOLOR = self.backgroundColor
        self._children = []
        self._id = _nbWidget
        self._lastSurface = 0
        self._type = widgetType

        _nbWidget += 1

        if parent != 0:
            self.setParent(parent)

        if self._type != "MApp": #Register the widget into the MApp object
            self.parent._declaringWidget(self)

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
    
    def move(self, newX, newY): #Change the value of X and Y in one function
        self.setX(newX)
        self.setY(newY)

    def posIn(self, pos): #Check if "pos" is in the widget
        if pos[0] >= self.absoluteX() and pos[1] > self.absoluteY() and pos[0] < self.absoluteX() + self.getWidth() and pos[1] < self.absoluteY() + self.getHeight():
            return True
        return False
    
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
        self.height = newHeight
        self.setShouldModify(True)
    
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
        self.width = newWidth
        self.setShouldModify(True)

    def setX(self, newX): #Change the value of X
        self.x = newX
        self.setShouldModify(True)

    def setY(self, newY): #Change the value of Y
        self.y = newY
        self.setShouldModify(True)

    def softResetWidget(self): #Reset without graphics modification
        self.mouseDown = -1
        self.mouseUp = -1
        self.overflighted = False

    def _addChild(self, child): #Add a child to the widget
        if self.containsChild(child.getID()) == -1:
            self._children.append(child)

    def _declaringWidget(self, widget): #Declare widget to the MApp if the widget is a MApp (function defined in MApp) or pass hit to his parent
        self.parent._declaringWidget(widget)

    def _isGettingMouseDown(self, button): #Function usefull for heritage, call by MApp when the widget is clicked (called for only one frame) with button = left button (1) and right button (2)
        pass

    def _isGettingMouseUp(self, button): #Function usefull for heritage, call by MApp when the widget is stopping of being clicked (called for only one frame) with button = left button (1) and right button (2)
        pass

    def _isGettingOverflighted(self): #Function usefull for heritage, call by MApp when the widget is overflighted (applicated for only one frame)
        pass
    
    def _removeChild(self, child): #Remove a child to the widget
        id = self.containsChild(child.getId())
        if id != -1:
            self._children = self._children[:id] + self._children[id:]

    def _render(self): #Render widget and return rendering

        if self.getShouldModify(): #If the widget should do the render, do it
            widgetSurface = Surface((self.width, self.height), pygame.SRCALPHA)

            widgetSurface.blit(self._renderBeforeHierarchy(widgetSurface), (0, 0, self.getWidth(), self.getHeight()))
            widgetSurface.blit(self._renderHierarchy(widgetSurface), (0, 0, self.getWidth(), self.getHeight()))
            widgetSurface.blit(self._renderAfterHierarchy(widgetSurface), (0, 0, self.getWidth(), self.getHeight()))

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

###################### Main application class
class MApp(MWidget):
    def __init__(self, pygameWindow, windowTitle, windowWidth, windowHeight, printFps = False): #MApp's constructor
        MWidget.__init__(self, 0, 0, windowWidth, windowHeight, 0, "MApp") #Parent class constructor call
        self.deltaTime = 0
        self.focusedWidget = self
        self.fps = 0
        self.printFps = printFps
        self.setWindowTitle(windowTitle)
        self._deltaTimeCache = time_ns()
        self._fpsCount = 0
        self._fpsDuration = 0
        self._modifiedWidget = []
        self._pygameWindow = pygameWindow
        self._widgets = []

    def frame(self): #Do a frame in the application
        self.frameEvent()
        self.frameGraphics()

    def frameEvent(self): #Do all events updates in the application
        self.deltaTime = (time_ns() - self._deltaTimeCache)/(10**9)
        self._deltaTimeCache = time_ns() #Calculate deltaTime

        self._fpsDuration += self.deltaTime
        if self._fpsDuration >= 1: #Handle fps counting
            self.fps = self._fpsCount
            self._fpsDuration -= 1
            self._fpsCount = 0

            if self.printFps:
                print(self.fps)

        self._fpsCount += 1

        for i in self._widgets: #Soft reset all widget
            i.softResetWidget()

        for i in self._modifiedWidget: #Reset all modified widget in the last call of frameEvent
            i.resetWidget()

        self._modifiedWidget.clear()

        cursor = self.getCursorOnOverflight()

        mousePos = pygame.mouse.get_pos() #Get mouse position

        overflightedWidget = self
        i = 0
        while i < len(overflightedWidget.getChildren()): #Find the overflighted widget
            widget = overflightedWidget.getChildrenAtIndex(i)
            if widget.posIn(mousePos):
                overflightedWidget = widget
                i = -1
            i += 1

        cursor = overflightedWidget.getCursorOnOverflight()
        overflightedWidget.overflighted = True
        pygame.mouse.set_cursor(cursor)
        overflightedWidget._isGettingOverflighted()

        events = pygame.event.get()
        for event in events: #Event handler
            if event.type == pygame.QUIT: #Quit pygame
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: #If the mouse is clicked
                overflightedWidget.mouseDown = event.button
                overflightedWidget._isGettingMouseDown(event.button)
                self.focusedWidget.focused = False
                self.focusedWidget = overflightedWidget
                self.focusedWidget.focused = True
            elif event.type == pygame.MOUSEBUTTONUP: #If the mouse is stopping of being clicked
                overflightedWidget.mouseUp = event.button
                overflightedWidget._isGettingMouseUp(event.button)

    def frameGraphics(self): #Do all graphics updates in the application
        self._pygameWindow.blit(self._render(), (0, 0, self.width, self.height))

    def getDeltaTime(self): #Return deltaTime
        return self.deltaTime
    
    def getFps(self): #Return fps
        return self.fps
    
    def getPrintFps(self): #Return printFps
        return self.printFps
    
    def getWidgets(self): #Return _widget
        return self._widgets
    
    def setPrintFps(self, printFps): #Change the value of printFps
        self.printFps = printFps

    def setWindowTitle(self, windowTitle): #Change the title of the window
        self.windowTitle = windowTitle

        pygame.display.set_caption(windowTitle)

    def _addWidgetToReset(self, widget): #Add a widget _modifiedWidget
        self._modifiedWidget.append(widget)

    def _containsWidget(self, widget): #Return if a widget is stored into _widgets
        for i in self._widgets:
            if i.getID() == widget.getID():
                return True
        return False

    def _declaringWidget(self, widget): #Declare widget to the MApp if the widget is a MApp or pass hit to his parent (function defined in MWidget)
        if not self._containsWidget(widget):
            self._widgets.append(widget)
            widget._mapp = self

class MFrame(MWidget):
    def __init__(self, x, y, width, height, parent):
        super().__init__(x, y, width, height, parent, "MFrame")

        self.frameBeforeHierarchy = True
        self.frameBottomWidth = 0
        self.frameColor = (0, 0, 0)
        self.frameLeftWidth = 0
        self.frameRightWidth = 0
        self.frameTopWidth = 0

    def getFrameBeforeHierarchy(self): #Return the value of frameBeforeHierarchy
        return self.frameBeforeHierarchy
    
    def getFrameColor(self): #Return frameColor
        return self.frameColor
    
    def getFrameWidth(self, index = 0): #Return the value of frameBottomWidth if 1, frameLeftWidth if 2, frameRightWidth if 3, frameTopWidth if 4
        if index == 0:
            return self.frameTopWidth
        elif index == 1:
            return self.frameLeftWidth
        elif index == 2:
            return self.frameBottomWidth
        else:
            return self.frameRightWidth
    
    def setFrameBeforeHierarchy(self, frameBeforeHierarchy): #Return the value of frameBeforeHierarchy
        if self.frameBeforeHierarchy != frameBeforeHierarchy:
            self.frameBeforeHierarchy = frameBeforeHierarchy
            self.setShouldModify(True)

    def setFrameColor(self, color): #Return frameColor
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

    def _renderAfterHierarchy(self, surface): #Render widget on surface after hierarchy render
        if not self.frameBeforeHierarchy:
            surface.fill(self.frameColor, (0, 0, self.getWidth(), self.getHeight()))
        surface.fill(self.backgroundColor, (self.getFrameWidth(1), self.getFrameWidth(0), self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)), self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2))))
        return surface

    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        if not self.frameBeforeHierarchy:
            surface.fill(self.frameColor, (0, 0, self.getWidth(), self.getHeight()))
        return surface