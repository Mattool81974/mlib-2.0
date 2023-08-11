from pygame import *
import pygame

pygame.init()

#Nombre de widget existants
_nbWidget = 0

###################### Base widget class
class MWidget:
    def __init__(self, x, y, width, height, parent, backgroundColor = (0, 0, 0)): #MWidget's constructor
        global _nbWidget
        self.backgroundColor = backgroundColor
        self.height = height
        self.parent = 0
        self.setShouldModify(True)
        self.width = width
        self.x = x
        self.y = y
        self._children = []
        self._id = _nbWidget
        self._lastSurface = 0

        _nbWidget += 1

        if parent != 0:
            self.setParent(parent)

    def containsChild(self, id): #Return if the widget contains the child with the id
        for i1, i2 in enumerate(self._children): #Search through all the children to find the one with the good id
            if i2.getID() == id:
                return i1
        return -1
    
    def getBackgroundColor(self): #Return the value of backgroundColor
        return self.backgroundColor

    def getHeight(self): #Return the value of height
        return self.height
    
    def getID(self): #Return the value of _id
        return self._id

    def getParent(self): #Return the value of parent
        return self.parent
    
    def getRect(self): #Return (x, y, width, height)
        return (self.getX(), self.getY(), self.getWidth(), self.getHeight())
    
    def getShouldModify(self): #Return the value of should modify
        return self.shouldModify
    
    def getWidth(self): #Return the value of width
        return self.width
    
    def getX(self): #Return the value of X
        return self.x
    
    def getY(self): #Return the value of Y
        return self.y
    
    def move(self, newX, newY): #Change the value of X and Y in one function
        self.setX(newX)
        self.setY(newY)

    def resize(self, newWidth, newHeight): #Change the value of width and height in one function
        self.setHeight(newHeight)
        self.setWidth(newWidth)

    def setBackgroundColor(self, backgroundColor): #Change the value of backgroundColor
        self.backgroundColor = backgroundColor
        self.setShouldModify(True)
    
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

    def setWidth(self, newWidth): #Change the value of width
        self.width = newWidth
        self.setShouldModify(True)

    def setX(self, newX): #Change the value of X
        self.x = newX
        self.setShouldModify(True)

    def setY(self, newY): #Change the value of Y
        self.y = newY
        self.setShouldModify(True)

    def _addChild(self, child): #Add a child to the widget
        if self.containsChild(child.getID()) == -1:
            self._children.append(child)
    
    def _removeChild(self, child): #Remove a child to the widget
        id = self.containsChild(child.getId())
        if id != -1:
            self._children = self._children[:id] + self._children[id:]

    def _render(self): #Render widget and return rendering

        if self.getShouldModify(): #If the widget should do the render, do it
            widgetSurface = Surface((self.width, self.height), pygame.SRCALPHA)
            widgetSurface.fill(self.backgroundColor, (0, 0, self.getWidth(), self.getHeight()))

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
        return surface
    
    def _renderHierarchy(self, surface): #Render hierarchy on surface
        for child in self._children: #Get the _render of all the children
            surface.blit(child._render(), child.getRect())
        return surface

###################### Main application class
class MApp(MWidget):
    def __init__(self, pygameWindow, windowWidth, windowHeight, backgroundColor = (0, 0, 0)): #MApp's constructor
        self._type = "MApp"

        MWidget.__init__(self, 0, 0, windowWidth, windowHeight, 0, backgroundColor) #Parent class constructor call
        self._pygameWindow = pygameWindow

    def frame(self): #Do a frame in the application
        self.frameEvent()
        self.frameGraphics()

    def frameEvent(self): #Do all events updates in the application
        events = pygame.event.get()
        for event in events: #Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def frameGraphics(self): #DO all graphics updates in the application
        self._pygameWindow.blit(self._render(), (0, 0, self.width, self.height))