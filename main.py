from mlib import *
from math import *
import pygame
from random import randint
from time import sleep

#TAILLE = (700, 394)
TAILLE = (900, 900)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], printFps=True)
mapp.setBackgroundColor((0, 0, 0))

phrase = "Le T-90 est un char de combat russe associant le char T-72B et certains sous-systèmes du T-80U.\nEntré en service dans l'armée russe en novembre 1992, le T-90 est actuellement utilisé par dix pays."
nb = 0
temps = 0

textes = []

for i in range(3):
    texte = MText(phrase, 100, 300 * i, 300, 300, mapp)
    texte.setCursorVisible(True)
    texte.setFontSize(22)
    texte.setFrameColor((255, 0, 0))
    texte.setFrameWidth(2)
    texte.setFrameWidth(20, 2)
    texte.setInput(True)
    texte.setTextVerticalAlignment(i)
    texte.setTextOffset(10, 0)
    texte.setTextOffset(40, 2)

    texte2 = MText(phrase, 500, 300 * i, 300, 300, mapp)
    texte2.setCursorVisible(True)
    texte2.setDynamicTextCut(True)
    texte2.setFontSize(22)
    texte2.setFrameColor((255, 0, 0))
    texte2.setFrameWidth(2)
    texte2.setFrameWidth(20, 2)
    texte2.setInput(True)
    texte2.setTextVerticalAlignment(i)
    texte2.setTextOffset(10, 0)
    texte2.setTextOffset(40, 2)

    textes.append(texte)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()