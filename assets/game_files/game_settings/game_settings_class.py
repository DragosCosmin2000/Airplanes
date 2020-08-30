class Game_Settings(object):
    def __init__(self):
        # for when the resolution is changed, to reset the game from beginning
        self.change_resolution_flag = False

        # a tuple: (width, height), see "self.get_game_screen_settings()" function definition to find how it is calculated
        self.game_resolution = 0

        # screen mode, one of {"Fullscreen", "Big window", "Small window"}
        self.screen_mode = "Fullscreen"

        # screen size
        # Fullscreen - fullscreen size, if it is 16:9
        # Big Window - 2/3 from the nearest 16:9 dimension obtained from decreasing screen size(a non 16:9 screen)
        # Small window - 1/2 from the nearest 16:9 dimension obtained from decreasing screen size(a non 16:9 screen)
        self.screen_size = 0

        # full screen mode flag, check if it can be full screen or not
        # True - it can be (means that the screen is 16:9)
        # False - opposite
        self.full_screen_flag = True

        # game volume
        self.music_volume = 50
        self.sound_volume = 50

        # flag for tutorial from singleplayer vsCPU mode
        self.tutorial_flag = True

        # -------------------------
        # Here will come a try and except for game settings file to get last settings

        # if there's no file from where to get the resolution, get it down here and make the file with calculated settings
        if self.game_resolution == 0:
            self.get_game_screen_settings()

    def get_game_screen_settings(self):
        self.game_resolution = (1024, 576) # (1536, 864)