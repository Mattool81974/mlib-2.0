from pygame import *
import pygame

pygame.init()

#Nombre de widget existants
_nbWidget = 0

class MWidget:
    def __init__(self, x, y, width, height, parent):
        self.height = height
        self.shouldModify = True
        self.width = width
        self.x = x
        self.y = y
        self._children = []
        self._id = _nbWidget
        self._lastSurface = 0

        _nbWidget += 1

        self.setParent(parent)

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
        self.parent = newParent
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
        if not self._containsChild(child.getId()):
            self._children.append(child)

    def _containsChild(self, id):
        for i in self._children:
            if i.getID() == id:
                return True
        return False

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
    def __init__(self, pygameWindow):
        self._pygameWindow = pygameWindow

    def frame(self):
        pass