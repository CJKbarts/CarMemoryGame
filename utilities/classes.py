import pygame
from pygame import mixer
from math import ceil


class Difficulty:
    def __init__(self):
        self.difficulty_level = 1
        self.number_of_turns = 3
        self.unlocked_level = 1

    def unlock_level(self):
        self.unlocked_level += 1

    def choose_difficulty(self, new_difficulty):
        self.difficulty_level = int(new_difficulty)
        if self.difficulty_level > 1:
            self.number_of_turns = 2 * self.difficulty_level

        else:
            self.number_of_turns = 3


class Button:
    def __init__(self, x, y, image):
        self.width = image.get_width()
        self.height = image.get_height()
        self.xpos = x - ceil(self.width/2)
        self.ypos = y - ceil(self.height/2)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.xpos, self.ypos)
        self.clicked = False
        self.needed = True

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def click(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.needed:
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action

    def used(self):
        self.needed = False

