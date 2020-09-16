from assets.game_files.game_settings.game_settings_class import Game_Settings
from assets.game_files.loading_screen import Loading_Screen
from assets.game_files.game_control_panel import Game_Control_Panel
from assets.game_files.transitions import Section_Transition
import threading
import pygame

# pygame initialization
pygame.init()

# clock
clock = pygame.time.Clock()

# screen tretching prevention (1)
import os, sys
if os.name != "nt" or sys.getwindowsversion()[0] < 6:
    raise NotImplementedError('this script requires Windows Vista or newer')

try:
    import ctypes
except ImportError:
    print('install ctypes from http://sourceforge.net/projects/ctypes/files/ctypes')
    raise
user32 = ctypes.windll.user32

# loading content thread, run while loading screen shows
class Loading_Content(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # flag to know when the thread ends
        self.loading = True

        # save images in below vars, you can pass an storage object for content

    def run(self):
        # load all the images
        print("Images loaded!")

        # unblock loading screen, after images load
        self.loading = False

def main():
    # get current settings
    current_settings = Game_Settings((user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)))

    # create window
    if current_settings.screen_mode == "Fullscreen":
        # screen tretching prevention (2)
        user32.SetProcessDPIAware()

        surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        current_settings.game_resolution = pygame.display.get_surface().get_size()
        current_settings.write_current_settings()
    else:
        surface = pygame.display.set_mode(current_settings.game_resolution)

    pygame.display.set_caption("Airplanes")

    # frames per second
    FPS = 60

    # create loading screen
    # Inside it try to load loading's images for 20 seconds or until they load
    # Just in case, because of some load errors(cause by antiviruse's scaning) that can appear
    # If after 20 seconds still doesn't load, raise to stop the execution
    loading_screen = Loading_Screen(surface, current_settings.game_resolution, 5, FPS, "assets\\game_images\\loading_screen_images\\loading_screen_drawing_with_text.png")

    # add an icon

    # create a thread to load game content and run it
    thread1 = Loading_Content()
    thread1.start()

    # loading screen loop
    while False:#loading_screen.loading_flag:
        clock.tick(FPS)

        # quit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loading_screen.loading_flag = False

        # start loading screen
        loading_screen.start_loading(thread1.loading)

        pygame.display.update()

    # remember to delete loading class, don't need it anymore

    # create game control panel
    game_control_panel = Game_Control_Panel(surface, current_settings, FPS)

    # create screen transition
    change_section_transition = Section_Transition(surface, current_settings.game_resolution, (255, 255, 255), FPS, 0.1)

    # game loop
    run = True
    while run:
        clock.tick(FPS)

        # events check
        for event in pygame.event.get():
            # quit check
            if event.type == pygame.QUIT:
                run = False

            # for change screen transition
            if not (change_section_transition.running):
                # set the flag to false after the transition ends
                game_control_panel.section_transition_flag = False

                # button click effect
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()


                        ##### MAIN MENU BUTTONS
                    ### Singleplayer button event
                    if game_control_panel.current_section == "MainMenu":
                        button = game_control_panel.main_menu_section.singleplayer_section_button
                        # button rect
                        rect = button.rect
                        if rect[0] - rect[2] // 2 <= pos[0] <= rect[0] + rect[2] // 2 and rect[1] - rect[3] // 2 <= pos[1] <= rect[1] + rect[3] // 2:
                            button.status = True
                            change_section_transition.running = True

                    ### Multiplayer button event
                    if game_control_panel.current_section == "MainMenu":
                        button = game_control_panel.main_menu_section.multiplayer_section_button
                        # button rect
                        rect = button.rect
                        if rect[0] - rect[2] // 2 <= pos[0] <= rect[0] + rect[2] // 2 and rect[1] - rect[3] // 2 <= pos[1] <= rect[1] + rect[3] // 2:
                            button.status = True
                            change_section_transition.running = True

                    ### Credits button event
                    if game_control_panel.current_section == "MainMenu":
                        button = game_control_panel.main_menu_section.credits_section_button
                        # button rect
                        rect = button.rect
                        if rect[0] - rect[2] // 2 <= pos[0] <= rect[0] + rect[2] // 2 and rect[1] - rect[3] // 2 <= pos[1] <= rect[1] + rect[3] // 2:
                            button.status = True
                            change_section_transition.running = True

                    ### Close icon button
                    # button rect
                    if game_control_panel.current_section == "MainMenu":
                        button = game_control_panel.main_menu_section.exit_button
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True

                    ### Settings icon button
                    # button rect
                    if game_control_panel.current_section == "MainMenu":
                        button = game_control_panel.main_menu_section.settings_button
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True
                            change_section_transition.running = True

                        ##### MULTIPLAYER MENU BUTTONS
                    ### Localhost button event
                    if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "MultiplayerMenu":
                        button = game_control_panel.multiplayer_section.localhost_button
                        # button rect
                        rect = button.rect
                        if rect[0] - rect[2] // 2 <= pos[0] <= rect[0] + rect[2] // 2 and rect[1] - rect[3] // 2 <= pos[1] <= rect[1] + rect[3] // 2:
                            button.status = True
                            change_section_transition.running = True

                    ### Back to main menu icon button
                    if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "MultiplayerMenu":
                        button = game_control_panel.multiplayer_section.back_to_main_menu_button
                        # button rect
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True
                            change_section_transition.running = True

                    ### Find match button
                    if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "LocalhostMenu":
                        button = game_control_panel.multiplayer_section.find_match_button
                        # button rect
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True

                    ### Back to multiplayer menu icon button
                    if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "LocalhostMenu":
                        button = game_control_panel.multiplayer_section.back_to_multiplayer_menu_button
                        # button rect
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True
                            change_section_transition.running = True

                    # ----------------- temporary

                    # BUZZ BUTTON
                    # button rect
                    if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "LocalhostMatch":
                        button = game_control_panel.multiplayer_section.buzz_button
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True

                    # CLOSE ICON BUTTON - Multiplayer
                    # button rect
                    if game_control_panel.current_section == "Multiplayer":
                        button = game_control_panel.multiplayer_section.exit_button
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True

                    # BACK ICON BUTTON - Multiplayer
                    # button rect
                    """if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "LocalhostMenu":
                        button = game_control_panel.multiplayer_section.back_button
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True
                            change_section_transition.running = True"""

                    # BACK ICON BUTTON - from preparing section to localhost menu
                    # button rect
                    if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "PreparingSection":
                        button = game_control_panel.multiplayer_section.back_to_localhost_menu_button
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True
                            change_section_transition.running = True

                    # READY BUTTON - go and play
                    # button rect
                    if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "PreparingSection":
                        button = game_control_panel.multiplayer_section.ready_button
                        rect = button.rect
                        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                            button.status = True

                    # ROTATE BUTTON - preparing section
                    if game_control_panel.current_section == "Multiplayer" and game_control_panel.multiplayer_section.current_section == "PreparingSection":
                        for i in range(3):
                            init_pos = game_control_panel.multiplayer_section.client_game_info.airplanes[i].init_pos
                            current_pos = game_control_panel.multiplayer_section.client_game_info.airplanes[i].current_pos
                            segment = game_control_panel.multiplayer_section.client_game_info.airplanes[i].segment_dimension
                            if current_pos == init_pos:
                                rect = (init_pos[0] - segment // 2, init_pos[1] - segment // 2, segment, segment)
                                if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
                                    game_control_panel.multiplayer_section.client_game_info.airplanes[i].rotate()
                                    game_control_panel.multiplayer_section.client_game_info.airplanes[i].rotating = True

        # if both are ready start transition
        if game_control_panel.multiplayer_section.client_game_info.both_ready or game_control_panel.multiplayer_section.client_game_info.timer_progression == 0:
            change_section_transition.running = True

        game_control_panel.display_content()
        if game_control_panel.current_section == "Exit":
            run = False

        # run transition, see transition.py to see how it works
        if change_section_transition.running:
            change_section_transition.run()
            # after fade in(when the screen is completly cover with the rect) change the window content,
                # for that set a flag to true, to know when to change the content
            if change_section_transition.fade_in_flag == False:
                game_control_panel.section_transition_flag = True

        pygame.display.update()

if __name__ == "__main__":
    main()

    pygame.quit()