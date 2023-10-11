from mlib import *

TAILLE = [300, 400]

fenetre = pygame.display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], printFps=True)

barre1 = MSlider(MSlider.ORIENTATION_TOP_TO_BOTTOM, 0, 100, 25, 25, 25, 250, mapp)
barre2 = MSlider(MSlider.ORIENTATION_BOTTOM_TO_TOP, 0, 100, barre1.getX() + barre1.getWidth() + 25, 25, 25, 250, mapp)
barre3 = MSlider(MSlider.ORIENTATION_LEFT_TO_RIGHT, 0, 100, 25, 300, 250, 25, mapp)
barre4 = MSlider(MSlider.ORIENTATION_RIGHT_TO_LEFT, 0, 100, 25, 350, 250, 25, mapp)

while True:
    mapp.frameEvent()

    mapp.frameGraphics()
    pygame.display.flip()