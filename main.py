from mlib import *
from math import *
import pygame
from random import randint
from time import sleep

#TAILLE = (700, 394)
TAILLE = (700, 700)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], printFps=True)
mapp.setBackgroundColor((0, 0, 0))

texte = MText("", 0, 0, TAILLE[0], TAILLE[1], mapp)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()