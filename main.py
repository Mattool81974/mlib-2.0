from mlib import *
from math import *
import pygame
from random import randint
from time import sleep

#TAILLE = (700, 394)
TAILLE = (700, 700)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], backgroundColor=(255, 255, 255), printFps=True)

colors = []
widgets = []

cursors = [pygame.SYSTEM_CURSOR_ARROW, pygame.SYSTEM_CURSOR_CROSSHAIR, pygame.SYSTEM_CURSOR_HAND, pygame.SYSTEM_CURSOR_CROSSHAIR, pygame.SYSTEM_CURSOR_NO]

for j in range(7):
    colorColumn = []
    widgetColumn = []
    for i in range(7):
        color = ((255/7) * i, 0, (255/7) * j)
        colorColumn.append(color)
        widgetColumn.append(MWidget(i * 100, j * 100, 100, 100, mapp, color, cursors[randint(0, 4)]))
    colors.append(colorColumn)
    widgets.append(widgetColumn)

while True:
    mapp.frameEvent()

    clicked1 = 0

    for j in range(7):
        for i in range(7):
            widgets[i][j].setBackgroundColor(colors[i][j])
            if widgets[i][j].getFocused() == 1:
                clicked1 = (i, j)

    if clicked1 != 0:
        colors[clicked1[0]][clicked1[1]] = (255, 255, 255)
        widgets[clicked1[0]][clicked1[1]].setBackgroundColor((255, 255, 255))

    mapp.frameGraphics()
    pygame.display.flip()