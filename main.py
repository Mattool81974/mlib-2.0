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

for i in range(300):
    p = ""
    for i in range(7):
        p += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[randint(0, 25)]
    phrase += (p + " ")

texte = MText(phrase, 0, 0, TAILLE[0], TAILLE[1], mapp)
texte.setFontSize(22)
texte.setFrameWidth(5)
texte.setDynamicTextCutType(1)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()