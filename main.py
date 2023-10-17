from mlib import *

TAILLE = [300, 400]

fenetre = pygame.display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], printFps=True)

bouton1 = MButton("Leclerc", 25, 25, 125, 25, mapp)
bouton2 = MButton("Leopard 2A6", 25, 175, 125, 25, mapp)
bouton3 = MButton("Challenger 2", 150, 25, 125, 25, mapp)
bouton4 = MButton("M1A2 Abrams", 150, 175, 125, 25, mapp)

bouton1.setFrameWidth(0)
bouton2.setFrameWidth(0)
bouton3.setFrameWidth(0)
bouton4.setFrameWidth(0)

char = MCheckBox(mapp)
char.addButton("Leclerc", bouton1)
char.addButton("Leopard 2A6", bouton2)
char.addButton("Challenger 2", bouton3)
char.addButton("M1A2 Abrams", bouton4)
char.setChangeFrameWidthOnChoice(True)
char.setFrameWidthOnChoice(2)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()