from mlib import *
from math import *
import pygame
from random import randint
from time import sleep

#TAILLE = (700, 394)
TAILLE = (1000, 1000)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], printFps=True)
mapp.setBackgroundColor((0, 0, 0))

phrase = "Le T-90 est un char de combat russe associant le char T-72B et certains sous-systèmes du T-80U.\nEntré en service dans l'armée russe en novembre 1992, le T-90 est actuellement utilisé par dix pays."
nb = 0
temps = 0

image1 = MImage("C:\\Users\\there\\Pictures\\donaldTrump.png", 0, 0, 500, 500, mapp)
image1.setFrameWidth(3)
image1.setImageHorizontalAlignment(0)
image1.setImageReframing(1)
image1.setImageSize((250, 250))

image2 = MImage("C:\\Users\\there\\Pictures\\donaldTrump.png", 500, 0, 500, 500, mapp)
image2.setFrameWidth(3)
image2.setImageReframing(2)
image2.setImageSize((250, 250))

image3 = MImage("C:\\Users\\there\\Pictures\\donaldTrump.png", 0, 500, 500, 500, mapp)
image3.setFrameWidth(3)
image3.setImageReframing(3)
image3.setImageSize((250, 250))

image4 = MImage("C:\\Users\\there\\Pictures\\donaldTrump.png", 500, 500, 500, 500, mapp)
image4.setFrameWidth(3)
image4.setImageReframing(4)
image4.setImageSize((250, 250))

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()