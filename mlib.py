from pygame import *
import pygame

pygame.init()

class MWidget:
    def __init__(self, x, y, width, height, parent):
        self.height = height
        self.parent = parent
        self.shouldModify = True
        self.width = width
        self.x = x
        self.y = y
        self._lastSurface = 0

    def getHeight(self):
        return self.height

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

    def setWidth(self, newWidth):
        self.width = newWidth
        self.shouldModify = True

    def setX(self, newX):
        self.x = newX
        self.shouldModify = True

    def setY(self, newY):
        self.y = newY
        self.shouldModify = True

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