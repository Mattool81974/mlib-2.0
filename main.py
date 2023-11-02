from mlib import *
from random import randint

TAILLE = [300, 400]

fenetre = pygame.display.set_mode(TAILLE)
mapp = MApp(fenetre, "Test", TAILLE[0], TAILLE[1], printFps=True)

vert = MFrame(30, 175, 240, 120, mapp)
vert.setBackgroundColor((0, 255, 0))
vert.setVisible(False)

bouton1 = MButton("Start", 30, 25, 120, 25, mapp)
bouton2 = MButton("Stop", 85, 50, 120, 25, mapp)
bouton3 = MButton("Reset", 150, 25, 120, 25, mapp)

chrono = MChrono(MChrono.FORMAT_HH_MM_CS, 30, 100, 240, 50, mapp)
chrono.setAntiAnaliasing(True)
chrono.setFontSize(27)
chrono.setTextHorizontalAlignment(1)
chrono.setTextVerticalAlignment(1)

chrono.setUnitSeparation(":")

t = 5 + randint(0, 10)
t0 = 0
tb = True

while True:
    mapp.frameEvent()

    t0 += mapp.getDeltaTime()

    if t0 > t and tb:
        chrono.start()
        vert.setVisible(True)
        tb = False

    if bouton1.isGettingLeftClicked(): chrono.start()

    if bouton2.isGettingLeftClicked(): chrono.stop()

    if bouton3.isGettingLeftClicked(): chrono.reset()

    mapp.frameGraphics()
    pygame.display.flip()