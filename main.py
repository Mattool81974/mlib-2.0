from mlib import *
from math import *
import pygame
from random import randint
from time import sleep, time_ns

#TAILLE = (700, 394)
TAILLE = (900, 900)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], console=False, printFps=True)
mapp.setBackgroundColor((0, 0, 0))

phrase = "Le T-90 est un char de combat russe associant le char T-72B et certains sous-systèmes du T-80U.\nEntré en service dans l'armée russe en novembre 1992, le T-90 est actuellement utilisé par dix pays."
phrase = ""
for i in range(100):
    phrase += str(i) + "-" + "123456789\n"[len(str(i))+1:]
phrase = phrase[:-1]
phrase = ""
nb = 0
temps = 0

texte = MText(phrase, 300, 0, 600, 900, mapp)
texte.setSelectionBackgroundColor((25, 102, 255))
texte.setDynamicTextCut(True)
texte.setFont("Consolas")
texte.setFontSize(17)
texte.setFrameColor((0, 0, 255))
texte.setFrameWidth(5)
texte.setInput(True)
texte.setSelectionTextColor((255, 255, 255))
texte.setTextOffset(5)
texte.setTextX(0)
texte.setTextY(0)

#CuttedText : 0.0013

while True:
    mapp.frameEvent()

    if len(texte.getText()):
        texte.setTextX(-50)

    mapp.frameGraphics()
    pygame.display.flip()