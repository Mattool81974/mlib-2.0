from mlib import *
from math import *
import pygame
from random import randint
from time import sleep

#TAILLE = (700, 394)
TAILLE = (500, 500)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], backgroundColor=(255, 255, 255))
widgets = []

cursors = [pygame.SYSTEM_CURSOR_ARROW, pygame.SYSTEM_CURSOR_CROSSHAIR, pygame.SYSTEM_CURSOR_HAND, pygame.SYSTEM_CURSOR_CROSSHAIR, pygame.SYSTEM_CURSOR_NO]

for j in range(5):
    widgetColumn = []
    for i in range(5):
        color = ((255/5) * i, 0, (255/5) * j)
        widgetColumn.append(MWidget(i * 100, j * 100, 100, 100, mapp, color, cursors[randint(0, 4)]))
    widgets.append(widgetColumn)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()