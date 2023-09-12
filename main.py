from mlib import *
from math import *
import pygame
from random import randint
from time import sleep

#TAILLE = (700, 394)
TAILLE = (900, 400)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], printFps=True)
mapp.setBackgroundColor((0, 0, 0))

phrase = "Le T-90 est un char de combat russe associant le char T-72B et certains sous-systèmes du T-80U.\nEntré en service dans l'armée russe en novembre 1992, le T-90 est actuellement utilisé par dix pays."
phrase = ""
for i in range(10):
    phrase += "123456789\n"
phrase = phrase[:-1]
nb = 0
temps = 0

texte = MText(phrase, 300, 0, 600, 400, mapp)
texte.setSelectionBackgroundColor((25, 102, 255))
texte.setDynamicTextCut(True)
texte.setFont("Consolas")
texte.setFontSize(17)
texte.setInput(True)
texte.setSelectionPos(0, 72)
texte.setSelectionTextColor((255, 255, 255))

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()