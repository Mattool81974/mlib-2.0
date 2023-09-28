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

img = MImage("C:/Users/Matt_o/Videos/Captures/Loading... 24_07_2023 18_16_28 (1).png", 0, 0, 300, 1200, mapp)

scrolleur = MScrollArea(img, 0, 0, 600, 600, mapp)
scrolleur.setBackgroundColor((0, 0, 0))

img.resize(300, 300)

texte = MText(phrase, 600, 0, 300, 300, mapp)
texte.setDynamicTextCut(True)
texte.setFontSize(23)
texte.setAntiAnaliasing(True)

texte = MText(phrase, 600, 300, 300, 300, mapp)
texte.setDynamicTextCut(True)
texte.setFontSize(23)
texte.setAntiAnaliasing(False)

t = 0

while True:
    mapp.frameEvent()

    t += mapp.getDeltaTime()
    ta = 500 * floor(t/3)
    img.resize(300 + ta, 300 + ta)
    
    mapp.frameGraphics()
    pygame.display.flip()