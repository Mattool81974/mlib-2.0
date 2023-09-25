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

texte = MText(phrase, 300, 300, 600, 300, mapp)
texte.setFont("Consolas")
texte.setFontSize(17)
texte.setFrameColor((0, 0, 255))
texte.setFrameWidth(5)
texte.setInput(True)
texte.setSelectionTextColor((255, 255, 255))

barH = MBar(0, 0, 100, 1, 300, 600, 600, 20, mapp)
barV = MBar(1, 0, 100, 1, 280, 300, 20, 300, mapp)

texteBH = MText("0", 150, 550, 50, 50, mapp)
texteBH.setFontSize(35)
texteBH.setTextHorizontalAlignment(1)
texteBH.setTextVerticalAlignment(1)
texteBV = MText("0", 150, 300, 50, 50, mapp)
texteBV.setFontSize(35)
texteBV.setTextHorizontalAlignment(1)
texteBV.setTextVerticalAlignment(1)

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

    texteBH.setText(str(barH.getValue()))
    texteBV.setText(str(barV.getValue()))

    mapp.frameGraphics()
    pygame.display.flip()