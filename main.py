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
phrase = ""
for i in range(100):
    phrase += str(i) + "-" + "123456789\n"[len(str(i))+1:]
phrase = phrase[:-1]
nb = 0
temps = 0

texte = MText(phrase, 300, 0, 600, 900, mapp)
texte.setSelectionBackgroundColor((25, 102, 255))
#texte.setDynamicTextCut(True)
texte.setFont("Consolas")
texte.setFontSize(17)
texte.setInput(True)
texte.setSelectionTextColor((255, 255, 255))
texte.setTextY(0)

e = -2500
t = 0

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()