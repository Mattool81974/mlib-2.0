from mlib import *
from math import *
import pygame
from random import randint
from time import sleep

#TAILLE = (700, 394)
TAILLE = (750, 750)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, TAILLE[0], TAILLE[1], backgroundColor=(255, 255, 255))

carreTaille = (25, 25)
widgets = []
for i in range(carreTaille[0]):
    widgetsSub = []
    for j in range(carreTaille[1]):
        color = (0, 0, 0)
        widget = MWidget((TAILLE[0] / carreTaille[0]) * i, (TAILLE[1] / carreTaille[1]) * j, (TAILLE[0] / carreTaille[0]), (TAILLE[1] / carreTaille[1]), mapp, backgroundColor=(color))
        widgetsSub.append(widget)
    widgets.append(widgetsSub)

def carreCentral(color = (0, 0, 0)):
    widgets[floor(carreTaille[0]/2)][floor(carreTaille[1]/2)].setBackgroundColor(color)

def carreExterieur(color = (0, 0, 0)):
    for i in range(carreTaille[1]):
        widgets[0][i].setBackgroundColor(color)

    for i in range(carreTaille[1]):
        widgets[carreTaille[0] - 1][i].setBackgroundColor(color)

    for i in range(carreTaille[0]):
        widgets[i][0].setBackgroundColor(color)

    for i in range(carreTaille[0]):
        widgets[i][carreTaille[1] - 1].setBackgroundColor(color)

def carreInterne(color = (0, 0, 0), n = 0):
    n2 = ceil(carreTaille[0]/2) - (ceil(carreTaille[0]/2) - n)

    ns = 0
    if carreTaille[0]%2 == 1:
        ns = 1

    for i in range(n2):
        ns += 2
    
    for i in range(ns):
        nb = floor(carreTaille[0]/2) - floor(ns/2)
        widgets[nb][i + nb].setBackgroundColor(color)

    for i in range(ns):
        nb = floor(carreTaille[0]/2) - floor(ns/2)
        nb2 = floor(carreTaille[0]/2) + floor(ns/2)
        widgets[nb2][i + nb].setBackgroundColor(color)

    for i in range(ns):
        nb = floor(carreTaille[0]/2) - floor(ns/2)
        widgets[i + nb][nb].setBackgroundColor(color)

    for i in range(ns):
        nb = floor(carreTaille[0]/2) - floor(ns/2)
        nb2 = floor(carreTaille[0]/2) + floor(ns/2)
        widgets[i + nb][nb2].setBackgroundColor(color)

t = True

while True:
    mapp.frame()

    n = ceil(carreTaille[0]/2) - 1

    if t:
        t = False
        carreCentral((255, 0, 0))

        o = False
        for i in range(n):
            if o:
                o = False
                carreInterne((255, 0, 0), 1 + i)
            else:
                o = True
                carreInterne((0, 0, 0), 1 + i)
    else:
        t = True
        carreCentral((0, 0, 0))
        carreExterieur((0, 0, 0))

        o = True
        for i in range(n):
            if o:
                o = False
                carreInterne((255, 0, 0), 1 + i)
            else:
                o = True
                carreInterne((0, 0, 0), 1 + i)


    pygame.display.flip()