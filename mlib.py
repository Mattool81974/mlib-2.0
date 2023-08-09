from pygame import *
import pygame

pygame.init()

#Nombre de widget existants
_nbWidget = 0

class MWidget:
    def __init__(self, x, y, width, height, parent):
        global _nbWidget
        self.height = height
        self.parent = 0
        self.shouldModify = True
        self.width = width
        self.x = x
        self.y = y
        self._children = []
        self._id = _nbWidget
        self._lastSurface = 0

        _nbWidget += 1

        if parent != 0:
            self.setParent(parent)

    def containsChild(self, id):
        for i1, i2 in enumerate(self._children):
            if i2.getID() == id:
                return i1
        return -1

    def getHeight(self):
        return self.height
    
    def getID(self):
        return self._id

    def getParent(self):
        return self.parent
    
    def getWidth(self):
        return self.width
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def move(self, newX, newY):
        self.setX(newX)
        self.setY(newY)

    def resize(self, newWidth, newHeight):
        self.setHeight(newHeight)
        self.setWidth(newWidth)
    
    def setHeight(self, newHeight):
        self.height = newHeight
        self.shouldModify = True
    
    def setParent(self, newParent):
        if self.parent != 0:
            self.parent._removeChild(self)

        self.parent = newParent
        self.parent.shouldModify = True
        self.shouldModify = True

        newParent._addChild(self)

    def setWidth(self, newWidth):
        self.width = newWidth
        self.shouldModify = True

    def setX(self, newX):
        self.x = newX
        self.shouldModify = True

    def setY(self, newY):
        self.y = newY
        self.shouldModify = True

    def _addChild(self, child):
        if self.containsChild(child.getID()) == -1:
            self._children.append(child)
    
    def _removeChild(self, child):
        id = self.containsChild(child.getId())
        if id != -1:
            self._children = self._children[:id] + self._children[id:]

    def _render(self, surface):

        widgetSurface = Surface((self.width, self.height))
        widgetSurface.blit(self._renderBeforeHierarchy(surface))
        widgetSurface.blit(self._renderAfterHierarchy(surface))

        surface.blit(widgetSurface)

        return surface
    
    def _renderAfterHierarchy(self, surface):
        return surface
    
    def _renderBeforeHierarchy(self, surface):
        return surface

class MApp(MWidget):
    def __init__(self, pygameWindow, windowWidth, windowHeight):
        MWidget.__init__(self, 0, 0, windowWidth, windowHeight, 0)
        self._pygameWindow = pygameWindow

    def frame(self):
        self.frameEvent()

    def frameEvent(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()