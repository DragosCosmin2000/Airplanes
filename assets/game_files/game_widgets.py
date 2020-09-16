import pygame
from math import ceil

class Image_Button(object):
    def __init__(self, surface, image, x, y, width, height):
        self.surface = surface

        self.image = image
        self.button_image = pygame.image.load(image)
        self.button_image = pygame.transform.scale(self.button_image, (width, height))

        self.rect = (x, y, width, height)

        # True - pressed
        # False - not pressed
        self.status = False

    def display(self):
        pos = pygame.mouse.get_pos()

        # highlighting button
        size = (self.rect[2], self.rect[3])
        if self.rect[0] - size[0] // 2 <= pos[0] <= self.rect[0] + size[0] // 2 and self.rect[1] - size[1] // 2 <= pos[1] <= self.rect[1] + size[1] // 2:
            self.button_image = pygame.image.load(self.image)
            size = (1.2 * self.rect[2], 1.2 * self.rect[3])

        self.button_image = pygame.transform.scale(self.button_image, (ceil(size[0]), ceil(size[1])))
        self.surface.blit(self.button_image, (self.rect[0] - size[0] // 2, self.rect[1] - size[1] // 2))

class Button(object):
    def __init__(self, surface, text, x, y, width, height, first_color, second_color, font_size):
        self.surface = surface
        self.text = text
        self.rect = (x, y, width, height)
        self.first_color = first_color
        self.second_color = second_color
        self.font = pygame.font.Font('assets\\game_fonts\\Rubik-Regular.ttf', font_size)
        # True - pressed
        # False - not pressed
        self.status = False

    def display(self):
        pos = pygame.mouse.get_pos()

        # highlighting button
        color_1, color_2 = self.first_color, self.second_color
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2] and self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
            color_1, color_2 = color_2, color_1

        # button outline
        points = [
            (self.rect[0], self.rect[1]),
            (self.rect[0], self.rect[1] + self.rect[3]),
            (self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]),
            (self.rect[0] + self.rect[2], self.rect[1])
        ]
        pygame.draw.lines(self.surface, self.first_color, True, points, 3)

        # button background
        pygame.draw.rect(self.surface, color_2, self.rect)

        # button text
        text = self.font.render(self.text, True, color_1, color_2)
        text_rect = text.get_rect()
        text_rect.center = (self.rect[0] + self.rect[2] // 2, self.rect[1] + self.rect[3] // 2)

        self.surface.blit(text, text_rect)

class Icon_Button(object):
    def __init__(self, surface, image, x, y, width, height):
        self.surface = surface

        self.icon_image = pygame.image.load(image)
        self.icon_image = pygame.transform.scale(self.icon_image, (width, height))

        self.rect = (x, y, width, height)

        # True - pressed
        # False - not pressed
        self.status = False

        # for changing the icon image(in case of)
        self.change_image_flag = 0

    def display(self):
        # display img
        self.surface.blit(self.icon_image, (self.rect[0], self.rect[1]))

        pos = pygame.mouse.get_pos()
        # highlighting button
        if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2] and self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
            # display it again to increase the opacity
            self.surface.blit(self.icon_image, (self.rect[0], self.rect[1]))
