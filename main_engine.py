import sys

import pygame_functions as pyf
import pygame
from utilities import functions

pygame.init()
pyf.screenSize(1280, 720)
pastel_blue = (57, 157, 207)
pyf.setBackgroundColour(pastel_blue)
pyf.setWindowTitle('Car Memory Game')
icon_img = pygame.image.load('Pictures/car.png').convert_alpha()
pygame.display.set_icon(icon_img)


start_button = functions.make_button('Pictures/start_button.png', 1, 640, 300)
quit_button = functions.make_button('Pictures/quit_button.png', 1, 640, 420)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pyf.spriteClicked(start_button):
            pyf.hideSprite(start_button)
            pyf.hideSprite(quit_button)
            functions.main_game()
            pyf.setBackgroundColour(pastel_blue)
            pyf.showSprite(start_button)
            pyf.showSprite(quit_button)
            pyf.updateDisplay()

        elif pyf.spriteClicked(quit_button):
            run = False

pygame.quit()
sys.exit()
