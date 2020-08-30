from assets.game_files.game_settings.game_settings_class import Game_Settings
from assets.game_files.loading_screen import Loading_Screen
import threading
import pygame

# pygame initialization
pygame.init()

# clock
clock = pygame.time.Clock()

# loading thread
class Loading_Thread(threading.Thread):
    def __init__(self, loading_screen):
        threading.Thread.__init__(self)
        self.loading_screen = loading_screen
        self.running = True

    def run(self):
        #print("bine bossule")
        #self.loading_screen.start_loading(clock)
        clock2 = pygame.time.Clock()
        run1 = True
        place = (0, 0)
        while run1:
            clock2.tick(self.loading_screen.fps)

            # quit check
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run1 = False
                    self.running = False

            self.loading_screen.surface.fill((0, 0, 0))
            self.loading_screen.surface.blit(self.loading_screen.cloud_image, place)

            if place[0] == 0:
                place = (100, 100)
            else:
                place = (0, 0)

            pygame.display.update()

def main():
    # get current settings
    current_settings = Game_Settings()

    # create window
    # surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.set_mode(current_settings.game_resolution)
    pygame.display.set_caption("Airplanes")

    # frames per second
    FPS = 60

    '''import ctypes
    user32 = ctypes.windll.user32
    #user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    print(screensize)'''

    # create loading screen
    # inside it try to load loading's images for 20 seconds or until they load
    # just in case, because of some load errors(cause by antiviruse's scaning) that can appear
    # if after 20 seconds still doesn't load, raise to stop the execution
    loading_screen = Loading_Screen(surface, current_settings.game_resolution, 8, FPS, "assets\game_images\loading_screen_images\loading_screen_drawing.png")

    # add an icon

    # create a thread to load game content
    thread1 = Loading_Thread(loading_screen)
    thread1.start()

    # load all game images and wait for loading screen thread to finish
    # create game object
    # ---------------------------
    print("Loading images...")

    # wait for loading to finish
    while True:
        if thread1.running == False:
            break
        import time
        print("yeaa")
        time.sleep(1)

    run = True
    while run:
        clock.tick(FPS)

        # quit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        surface.fill((0, 255, 0))

        #loading_screen.start_loading()
        pygame.display.update()

if __name__ == "__main__":
    main()

    pygame.quit()