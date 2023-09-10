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

texte = MText("", 300, 0, 600, 900, mapp)
texte.setCursorVisible(True)
texte.setDynamicTextCut(True)
texte.setFontSize(19)
texte.setInput(True)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()