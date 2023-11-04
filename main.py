from mlib import *

TAILLE = [500, 500]

window = pygame.display.set_mode(TAILLE)
mapp = MApp(window, "Test", TAILLE[0], TAILLE[1], printFps = True)

bouton1 = MButton("Leclerc", 0, 0, 200, 50, mapp)
bouton2 = MButton("M1A2 Abrams", 0, 50, 200, 50, mapp)
mcb = MCheckBox(mapp)

mcb.addButton("Leclerc", bouton1)
mcb.addButton("M1A2 Abrams", bouton2)

while True:
    mapp.frameEvent()

    t = mcb.isChoiceGettingChanged()
    if t[0]:
        print("Changemenent de nom, \"" + t[2] + "\" devient \"" + t[1] + "\"")

    mapp.frameGraphics()
    pygame.display.flip()