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
    tex = []
    for j in range(3):
        texte = MText(phrase, (TAILLE[0]/3)*i, (TAILLE[0]/3)*j, TAILLE[0]/3, TAILLE[1]/3, mapp)
        texte.setCursorPosition(len(texte.getText()))
        texte.setCursorVisible(True)
        texte.setFontSize(22)
        texte.setFrameWidth(5)
        texte.setInput(True)
        texte.setDynamicTextCut(True)
        texte.setDynamicTextCutType(0)
        texte.setTextHorizontalAlignment(i)
        texte.setTextVerticalAlignment(j)
        tex.append(texte)
    textes.append(tex)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()