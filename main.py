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

slider = MSlider(1, 0, 500000, 610, 10, 15, 600, mapp)
slider.setStep(1)
texte = MText("0", 630, 10, 200, 50, mapp)
texte.setFontSize(22)
texte.setTextHorizontalAlignment(1)
texte.setTextVerticalAlignment(1)

while True:
    mapp.frameEvent()

    texte.setText(str(slider.getValue()))
    
    mapp.frameGraphics()
    pygame.display.flip()