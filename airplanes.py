from assets.game_files.game_settings.game_settings_class import Game_Settings
from assets.game_files.loading_screen import Loading_Screen
import threading
import pygame

# pygame initialization
pygame.init()

# clock
clock = pygame.time.Clock()

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
    current_settings = Game_Settings()

    # create window
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # surface = pygame.display.set_mode(current_settings.game_resolution)
    pygame.display.set_caption("Airplanes")

    # frames per second
    FPS = 60

    '''import ctypes
    user32 = ctypes.windll.user32
    #user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    print(screensize)'''

    # create loading screen
    # Inside it try to load loading's images for 20 seconds or until they load
    # Just in case, because of some load errors(cause by antiviruse's scaning) that can appear
    # If after 20 seconds still doesn't load, raise to stop the execution
    loading_screen = Loading_Screen(surface, current_settings.game_resolution, 5, FPS, "assets\\game_images\\loading_screen_images\\loading_screen_drawing.png")

    # add an icon

    # create a thread to load game content and run it
    thread1 = Loading_Content()
    thread1.start()

    # loading screen loop
    while loading_screen.loading_flag:
        clock.tick(FPS)

        # quit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loading_screen.loading_flag = False

        # start loading screen
        loading_screen.start_loading(thread1.loading)

        pygame.display.update()

    # create game object
    # game loop

if __name__ == "__main__":
    main()

    pygame.quit()