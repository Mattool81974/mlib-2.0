from mlib import *
import pygame

TAILLE = (700, 394)

fenetre = display.set_mode(TAILLE)
mapp = MApp(fenetre)

while True:
    mapp.frame()

    pygame.display.flip()

pygame.quit()