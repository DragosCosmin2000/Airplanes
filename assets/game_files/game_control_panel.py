from assets.game_files.multiplayer.multiplayer_section import Multiplayer
from assets.game_files.main_menu.main_menu import Main_Menu
import pygame

class Game_Control_Panel(object):
    def __init__(self, surface, game_settings, FPS):
        self.surface = surface

        # current section
        self.current_section = "MainMenu"

        # sections
        self.multiplayer_section = Multiplayer(self.surface, game_settings.game_resolution, FPS)
        self.main_menu_section = Main_Menu(self.surface, game_settings.game_resolution)

        # section transition flag
        # True - change section
        # False - wait
        self.section_transition_flag = False

    def display_content(self):
        if self.current_section == "Multiplayer":
            self.multiplayer_section.display_content()
        elif self.current_section == "MainMenu":
            self.main_menu_section.display_content()

        # buttons press checks
        # change the window content when the fade in ends(when fade in ends self.section_transition_flag turn to True)

            ##### MAIN MENU BUTTONS
        # "go to singleplayer section" button
        if self.main_menu_section.singleplayer_section_button.status and self.section_transition_flag:
            self.main_menu_section.singleplayer_section_button.status = False
            self.current_section = "Multiplayer" # need to do singleplayer section

        # "go to multiplayer section" button
        if self.main_menu_section.multiplayer_section_button.status and self.section_transition_flag:
            self.main_menu_section.multiplayer_section_button.status = False
            self.current_section = "Multiplayer"

        # "go to credits section" button
        if self.main_menu_section.credits_section_button.status and self.section_transition_flag:
            self.main_menu_section.credits_section_button.status = False
            self.current_section = "Multiplayer"

        # "go to settings section" button
        if self.main_menu_section.settings_button.status and self.section_transition_flag:
            self.main_menu_section.settings_button.status = False
            self.current_section = "Multiplayer"

            ##### MULTIPLAYER MENU BUTTONS
        # "go to localhost section" button
        if self.multiplayer_section.localhost_button.status and self.section_transition_flag:
            self.multiplayer_section.localhost_button.status = False
            self.multiplayer_section.current_section = "LocalhostMenu"

        # "go from multiplayer menu to main menu" icon button
        if self.multiplayer_section.back_to_main_menu_button.status and self.section_transition_flag:
            self.multiplayer_section.back_to_main_menu_button.status = False
            self.current_section = "MainMenu"

        # find match button - don't need to be here because it doesn't need a transition

        # "go from localhost menu section to multiplayer menu" icon button
        if self.multiplayer_section.back_to_multiplayer_menu_button.status and self.section_transition_flag:
            self.multiplayer_section.back_to_multiplayer_menu_button.status = False
            self.multiplayer_section.current_section = "MultiplayerMenu"

            # change img button too
            self.multiplayer_section.find_match_button.icon_image = pygame.image.load("assets\\game_images\\icons\\find_match.png")
            self.multiplayer_section.find_match_button.change_image_flag = 0
            self.multiplayer_section.find_match_button.icon_image = pygame.transform.scale(self.multiplayer_section.find_match_button.icon_image, (self.multiplayer_section.find_match_button.rect[2], self.multiplayer_section.find_match_button.rect[3]))

            # disconnect too
            self.multiplayer_section.connected = False
            # match finder cancelled
            try:
                self.multiplayer_section.player_number = None
                self.multiplayer_section.network.send("close")
            except:
                print("Server doesnt exist! (CLOSE TRY)")

        # -------------- temporary

        # go back to localhost menu from preparing section
        if self.multiplayer_section.back_to_localhost_menu_button.status and self.section_transition_flag:
            self.multiplayer_section.back_to_localhost_menu_button.status = False
            self.multiplayer_section.current_section = "LocalhostMenu"
            self.multiplayer_section.connected = False
            self.multiplayer_section.client_game_info.reset_data()

        # ready, now play
        if self.multiplayer_section.ready_button.status:
            self.multiplayer_section.ready_button.status = False
            self.multiplayer_section.client_game_info.client_ready = bool(abs(self.multiplayer_section.client_game_info.client_ready - 1))

        if self.section_transition_flag and (self.multiplayer_section.client_game_info.both_ready or self.multiplayer_section.client_game_info.timer_progression == 0):
            self.multiplayer_section.current_section = "LocalhostMatch"
            self.multiplayer_section.client_game_info.timer_progression = self.multiplayer_section.fps * 60
            self.multiplayer_section.client_game_info.both_ready = False
            self.multiplayer_section.client_game_info.client_ready = False