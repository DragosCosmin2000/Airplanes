import pygame
class Game_Settings(object):
    def __init__(self, real_screen_size):
        # for when the resolution is changed, to reset the game from beginning
        self.change_resolution_flag = False

        # screen mode, one of {"Fullscreen", "Big window", "Small window"}
        self.screen_mode = "Fullscreen"

        # screen size
        # Fullscreen - fullscreen size, if it is 16:9
        # Big Window - 2/3 from the nearest 16:9 dimension obtained from decreasing screen size(a non 16:9 screen)
        # Small window - 1/2 from the nearest 16:9 dimension obtained from decreasing screen size(a non 16:9 screen)
        # a tuple: (width, height), see "self.get_game_screen_settings()" function definition to find how it is calculated
        self.game_resolution = (0, 0)
        #self.screen_size = 0


        # real screen size (in case of using Window Mode)
        # set real screen size
        self.real_screen_size = real_screen_size

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
        try:
            file = open("assets\\game_files\\game_settings\\settings.txt", "r")
            self.get_current_settings(file)
        except:
            print("Cannot open the settings file!")

        # if there's no file from where to get the resolution, get it down here and make the file with calculated settings
        if self.game_resolution == (0, 0):
            self.get_game_screen_settings()
            self.write_current_settings()

    def get_current_settings(self, file):
        self.screen_mode = file.readline()

        # to remove "\n"
        self.screen_mode = self.screen_mode[:(len(self.screen_mode) - 1)]

        game_rez = (file.readline()).split(",")
        self.game_resolution = (int(game_rez[0]), int(game_rez[1]))

        self.full_screen_flag = bool(file.readline())

        self.music_volume = int(file.readline())

        self.sound_volume = int(file.readline())

        self.tutorial_flag = bool(file.readline())

    def write_current_settings(self):
        # write current settings in the file
        file = open("assets\\game_files\\game_settings\\settings.txt", "w")
        file.write(self.screen_mode + "\n")
        file.write(str(self.game_resolution[0]) + "," + str(self.game_resolution[1]) + "\n")
        file.write(str(self.full_screen_flag) + "\n")
        file.write(str(self.music_volume) + "\n")
        file.write(str(self.sound_volume) + "\n")
        file.write(str(self.tutorial_flag))

    def get_game_screen_settings(self):
        # I do that because if it's not an exact devision I can get results like x.9999999999999 and y.0000000000001 and that's not good
        if (self.real_screen_size[1] / 16) - (self.real_screen_size[0] / 16) > 0.1:
            self.screen_mode = "Big Window"

        if self.screen_mode == "Fullscreen":
            self.full_screen_flag = True
        # Just else because it's big window, small window is ignored for the moment
        else:
            self.game_resolution = (7 * self.real_screen_size[0] // 8, 7 * self.real_screen_size[1] // 8)
            #self.game_resolution = (5 * self.real_screen_size[0] // 8, 5 * self.real_screen_size[1] // 8) <----- Small Window Dimension
            self.full_screen_flag = False