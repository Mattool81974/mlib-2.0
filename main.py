from mlib import *
from math import *
import pygame
from random import randint
from time import sleep, time_ns

#TAILLE = (700, 394)
TAILLE = (900, 900)

fenetre = pygame.display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], console=False, printFps=True)
mapp.setBackgroundColor((255, 255, 255))

phrase = "Le T-90 est un char de combat russe associant le char T-72B et certains sous-systèmes du T-80U.\nEntré en service dans l'armée russe en novembre 1992, le T-90 est actuellement utilisé par dix pays."

img = MImage("C:/Users/Matt_o/Videos/Captures/Loading... 24_07_2023 18_16_28 (1).png", 0, 0, 300, 1200, mapp)

scrolleur = MScrollArea(img, 0, 0, 600, 600, mapp)
scrolleur.setBackgroundColor((0, 0, 0))

img.resize(800, 800)

texte = MText(phrase, 600, 0, 300, 300, mapp)
texte.setDynamicTextCut(True)
texte.setFontSize(23)
texte.setAntiAnaliasing(True)

texte2 = MText(phrase, 600, 300, 300, 300, mapp)
texte2.setDynamicTextCut(True)
texte2.setFontSize(23)
texte2.setAntiAnaliasing(False)

bouton = MButton("A", 0, 600, 100, 50, mapp)
lol = MWidget(0, 350, 100, 50, mapp)
lol.setVisible(False)

entre = MText("", 100, 600, 200, 50, mapp)
entre.setFrameWidth(2)
entre.setInput(True)

while True:
    mapp.frameEvent()
    
    mapp.frameGraphics()
    pygame.display.flip()