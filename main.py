from mlib import *
import pygame

TAILLE = (700, 394)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre, TAILLE[0], TAILLE[1])
widget = MWidget(0, 0, 100, 100, mapp)

while True:
    mapp.frame()

    pygame.display.flip()