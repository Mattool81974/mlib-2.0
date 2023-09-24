from mlib import *
from math import *
import pygame
from random import randint
from time import sleep, time_ns

#TAILLE = (700, 394)
TAILLE = (900, 900)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], console=False, printFps=True)
mapp.setBackgroundColor((255, 255, 255))

phrase = "Le T-90 est un char de combat russe associant le char T-72B et certains sous-systèmes du T-80U.\nEntré en service dans l'armée russe en novembre 1992, le T-90 est actuellement utilisé par dix pays."

texte = MText(phrase, 300, 0, 600, 900, mapp)
texte.setFont("Consolas")
texte.setFontSize(17)
texte.setFrameColor((0, 0, 255))
texte.setFrameWidth(5)
texte.setInput(True)
texte.setSelectionTextColor((255, 255, 255))

effacer = MButton("Effacer", 0, 0, 280, 100, mapp)
effacer.setTextColor((255, 255, 255))

effacer.setFontSize(22)
effacer.setFontSizeOnOverflight(18)
effacer.setChangeFontSizeOnOnOverflight(True)

effacer.setFrameWidth(0)

while True:
    mapp.frameEvent()

    if effacer.isGettingLeftClicked():
        texte.setText("")
    else:
        texte.setText(phrase)

    if effacer.isGettingRightClicked():
        texte.setTextColor((255, 0, 0))
    else:
        texte.setTextColor((0, 0, 0))

    mapp.frameGraphics()
    pygame.display.flip()