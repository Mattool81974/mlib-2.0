from mlib import *

TAILLE = [300, 400]

fenetre = pygame.display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], printFps=True)

barre1 = MBar(MBar.ORIENTATION_TOP_TO_BOTTOM, 25, 25, 25, 250, mapp)
barre2 = MBar(MBar.ORIENTATION_BOTTOM_TO_TOP, barre1.getX() + barre1.getWidth() + 25, 25, 25, 250, mapp)
barre3 = MBar(MBar.ORIENTATION_LEFT_TO_RIGHT, 25, 300, 250, 25, mapp)
barre4 = MBar(MBar.ORIENTATION_RIGHT_TO_LEFT, 25, 350, 250, 25, mapp)

slider = MSlider(1, 0, 100, barre2.getX() + barre2.getWidth() + 25, 25, 25, 250, mapp)

valeur = MText("0", slider.getX() + slider.getWidth() + 25, 25, 100, 250, mapp)
valeur.setAntiAnaliasing(True)
valeur.setFontSize(23)
valeur.setTextHorizontalAlignment(1)
valeur.setTextVerticalAlignment(1)

while True:
    mapp.frameEvent()

    valeur.setText(str(slider.getValue()))
    barre1.setValue(slider.getValue())
    barre2.setValue(slider.getValue())
    barre3.setValue(slider.getValue())
    barre4.setValue(slider.getValue())

    mapp.frameGraphics()
    pygame.display.flip()