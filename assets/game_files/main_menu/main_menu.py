from assets.game_files.game_widgets import Icon_Button, Image_Button
import pygame
from math import ceil

class Main_Menu(object):
    def __init__(self, surface, screen_size):
        self.surface = surface

        self.screen_size = screen_size

            #### BACKGROUND
        self.background_image = pygame.image.load("assets\\game_images\\background.jpg")
        # add 20 px to screen size to make sure that it blits over the enitre window(didn't remain 1 pixel uncovered)
        # I'll blit it at position (0 - 20 / 2, 0 - 20 / 2)
        self.background_image = pygame.transform.scale(self.background_image, (screen_size[0] + 20, screen_size[1] + 20))

            #### GAME's TITLE
        self.title_width_size = self.screen_size[0] // 2
        # Increase the height with a x%, where x is "with how much I increase/decrease the width size", simple math
        self.title_height_size = 205 + ceil(((self.title_width_size - 877) / 877) * 205)
        self.game_title = pygame.image.load("assets\\game_images\\game_title.png")
        self.game_title = pygame.transform.scale(self.game_title, (self.title_width_size, self.title_height_size))

                    #### MENU BUTTONS
        ### Singleplayer button
        # The image is 531 x 61, it's not 16:9 so I need to take care of how I resize it
        button_width = self.screen_size[0] // 4  # <- here I resize the button width

        # here I calculate with how much the button_width is bigger to know with how much to increase/decrease the height, just some simple math
        button_height = 61 + ceil(((button_width - 531) / 531) * 61)

        # I calculate where to place the button from top
        top_margin_for_buttons = self.screen_size[1] // 4 + self.title_height_size // 2 + 1.5 * button_height

        self.singleplayer_section_button = Image_Button(self.surface, "assets\\game_images\\texts\\singleplayer1.png", self.screen_size[0] // 2, top_margin_for_buttons, button_width, button_height)

        ### Multiplayer button
        # the size of the image is 487 x 63
        # Because no all the texts have the same length, I can't make "abc" the same size with "abcdefghij", so I will resize it after the % of how much bigger is the first text
        button_width2 = 487 + ceil(((button_width - 531) / 531) * 487)  # <- here I resize the button width

        # here I calculate with how much the button_width is bigger to know with how much to increase/decrease the height, just some simple math
        button_height2 = 63 + ceil(((button_width - 531) / 531) * 63)

        # I calculate where to place the button from top
        top_margin_for_buttons += 2 * button_height2

        self.multiplayer_section_button = Image_Button(self.surface, "assets\\game_images\\texts\\multiplayer1.png", self.screen_size[0] // 2, top_margin_for_buttons, button_width2, button_height2)

        ### Credits button
        # the size of the image is 305 x 61
        # Because no all the texts have the same length, I can't make "abc" the same size with "abcdefghij", so I will resize it after the % of how much bigger is the first text
        button_width2 = 305 + ceil(((button_width - 531) / 531) * 305)  # <- here I resize the button width

        # here I calculate with how much the button_width is bigger to know with how much to increase/decrease the height, just some simple math
        button_height2 = 61 + ceil(((button_width - 531) / 531) * 61)

        # I calculate where to place the button from top
        top_margin_for_buttons += 2 * button_height2

        self.credits_section_button = Image_Button(self.surface, "assets\\game_images\\texts\\credits1.png", self.screen_size[0] // 2, top_margin_for_buttons, button_width2, button_height2)

        ### Exit icon button
        # Adjust the size here
        size = self.screen_size[0] // 35
        self.exit_button = Icon_Button(self.surface, "assets\\game_images\\icons\\close_icon.png", self.screen_size[0] - 3 * size // 2, size // 2, size, size)

        ### Settings icon button
        # Adjust the size here
        size = self.screen_size[0] // 35
        self.settings_button = Icon_Button(self.surface, "assets\\game_images\\icons\\settings_icon.png", self.screen_size[0] - 3 * size, size // 2, size, size)

    def display_content(self):
        # Display the background image
        self.surface.blit(self.background_image, (-10, -10))

        # Display text title
        self.surface.blit(self.game_title, ((self.screen_size[0] - self.title_width_size) // 2, self.screen_size[1] // 4 - self.title_height_size // 2))

        #### BUTTONS DISPLAY
        # display "go to singleplayer section" button
        self.singleplayer_section_button.display()

        # display "go to multiplayer section" button
        self.multiplayer_section_button.display()

        # display "go to credits section" button
        self.credits_section_button.display()

        # display "go to settings section" icon button
        self.settings_button.display()

        # display exit button
        self.exit_button.display()
        # exit button functionality
        if self.exit_button.status:
            exit()