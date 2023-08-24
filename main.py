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

phrase = ""

texte = MText(phrase, 0, 0, TAILLE[0], TAILLE[1], mapp)
texte.setFontSize(22)
texte.setFrameWidth(5)
texte.setInput(True)
texte.setDynamicTextCutType(1)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()