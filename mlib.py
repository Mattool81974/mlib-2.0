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

    def _isKeyGettingDropped(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is dropped on the keyboard (applicated for only one frame)
        pass

    def _isKeyGettingPressed(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is pressed on the keyboard (applicated for only one frame)
        pass

    def _isTextGettingEntered(self, text): #Function usefull for heritage, call by MApp when the widget is focused and the user is typing a text
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
        self.pressedKey = []
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

        self.pressedKey.clear()

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
            elif event.type == pygame.KEYDOWN: #If a key is pressed on the keyboard
                overflightedWidget._isKeyGettingPressed(event.key)
                self.pressedKey.append(event.key)
            elif event.type == pygame.KEYUP: #If a key is dropped on the keyboard
                overflightedWidget._isKeyGettingDropped(event.key)
            elif event.type == pygame.TEXTINPUT: #If the user is enterring text
                overflightedWidget._isTextGettingEntered(event.text)

    def frameGraphics(self): #Do all graphics updates in the application
        self._pygameWindow.blit(self._render(), (0, 0, self.width, self.height))

    def getDeltaTime(self): #Return deltaTime
        return self.deltaTime
    
    def getFps(self): #Return fps
        return self.fps
    
    def getPressedKey(self): #Return pressedKey
        return self.pressedKey
    
    def getPrintFps(self): #Return printFps
        return self.printFps
    
    def getWidgets(self): #Return _widget
        return self._widgets
    
    def isKeyPressed(self, key): #Return if the key is pressed
        for i in self.pressedKey:
            if key == i:
                return True
        return False
    
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
                print(self.leftTopCornerRadius, cornerRadius)
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

    def _renderAfterHierarchy(self, surface): #Render widget on surface after hierarchy render
        if not self.frameBeforeHierarchy:
            pygame.draw.rect(surface, self.frameColor, (0, 0, self.getWidth(), self.getHeight()), 0, 0, self.leftTopCornerRadius, self.rightTopCornerRadius, self.leftBottomCornerRadius, self.rightBottomCornerRadius)
        return surface

    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        if self.frameBeforeHierarchy:
            pygame.draw.rect(surface, self.frameColor, (0, 0, self.getWidth(), self.getHeight()), 0, 0, self.leftTopCornerRadius, self.rightTopCornerRadius, self.leftBottomCornerRadius, self.rightBottomCornerRadius)
        pygame.draw.rect(surface, self.backgroundColor, (self.getFrameWidth(1), self.getFrameWidth(0), self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3)), self.getHeight() - (self.getFrameWidth(0) + self.getFrameWidth(2))), 0, 0, self.leftTopCornerRadius, self.rightTopCornerRadius, self.leftBottomCornerRadius, self.rightBottomCornerRadius)
        return surface

class MText(MFrame):
    def __init__(self, text, x, y, width, height, parent, widgetType = "MText"):
        super().__init__(x, y, width, height, parent, widgetType)

        self.dynamicTextCut = False
        self.dynamicTextCutType = 1
        self.font = "arial"
        self.fontSize = 12
        self.input = False
        self.text = text
        self.textColor = (0, 0, 0)

    def getDynamicTextCut(self): #Return dynamicTextCut
        return self.dynamicTextCut
    
    def getDynamicTextCutType(self): #Return dynamicTextCutType
        return self.dynamicTextCutType

    def getFont(self): #Return font
        return self.font
    
    def getFontSize(self): #Return fontSize
        return self.fontSize
    
    def getInput(self): #Return input
        return self.input

    def getText(self): #Return text
        return self.text
    
    def getTextColor(self): #Return textColor
        return self.textColor
    
    def setDynamicTextCut(self, dynamicTextCut): #Change the value of dynamicTextCut
        if self.dynamicTextCut != dynamicTextCut:
            self.dynamicTextCut = dynamicTextCut
            self.setShouldModify(True)

    def setDynamicTextCutType(self, dynamicTextCutType): #Return dynamicTextCutType
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

    def setInput(self, input): #Change the value of input
        self.input = input
    
    def setText(self, text): #Change the value of text
        if self.text != text:
            self.text = text
            self.setShouldModify(True)

    def setTextColor(self, textColor): #Change the value of textColor
        if self.textColor != textColor:
            self.textColor = textColor
            self.setShouldModify(True)

    def appendText(self, text): #Append "text" to text
        self.setText(self.getText() + text)

    def _isKeyGettingPressed(self, key): #Function usefull for heritage, call by MApp when the widget is focused and a key is pressed on the keyboard (applicated for only one frame)
        if self.getInput():
            if key == pygame.K_BACKSPACE:
                self.setText(self.getText()[:-1])
            elif key == pygame.K_RETURN:
                self.appendText("\n")

    def _isTextGettingEntered(self, text): #Function usefull for heritage, call by MApp when the widget is focused and the user is entering a text (applicated for only one frame)
        if self.getInput():
            self.appendText(text)

    def _renderBeforeHierarchy(self, surface): #Render widget on surface before hierarchy render
        surface = super()._renderBeforeHierarchy(surface)

        generator = pygame.font.SysFont(self.font, self.fontSize)
        pieces = []
        spaceWidth = generator.size(" ")[0]
        textWidth = self.getWidth() - (self.getFrameWidth(1) + self.getFrameWidth(3))
        x = self.getFrameWidth(1)
        y = self.getFrameWidth(0)

        if self.dynamicTextCut: #Cut lines into pieces
            pieces = self.text.split("\n")
        else:
            lines = self.text.split("\n")
            for line in lines:
                firstI = 0
                lastI = 0
                lineWidth = 0
                toAnalyze = line
                if self.dynamicTextCutType == 1:
                    toAnalyze = line.split(" ")

                for letter in toAnalyze: #Analyze caracter by caracter/word by word
                    letterSize = generator.size(letter)
                    if lineWidth + letterSize[0] > textWidth and firstI != lastI:
                        toAdd = ""
                        for i in range(firstI, lastI):
                            toAdd += toAnalyze[i]
                            if self.dynamicTextCutType == 1 and i != lastI - 1:
                                toAdd += " "
                        pieces.append(toAdd)
                        firstI = lastI
                        lineWidth = 0
                    lastI += 1
                    lineWidth += letterSize[0]
                    if self.dynamicTextCutType == 1:
                        lineWidth += spaceWidth

                if firstI < len(toAnalyze):
                    toAdd = ""
                    for i in range(firstI, len(toAnalyze)):
                        toAdd += toAnalyze[i]
                        if self.dynamicTextCutType == 1 and i != len(toAnalyze) - 1:
                            toAdd += " "
                    pieces.append(toAdd)

        for piece in pieces: #Render text into pieces
            textSurface = generator.render(piece, False, self.textColor)
            surface.blit(textSurface, (x, y, textSurface.get_width(), textSurface.get_height()))
            y += textSurface.get_height()

        return surface