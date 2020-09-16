from assets.game_files.multiplayer.multiplayer_network import Network
from assets.game_files.multiplayer.multiplayer_server import run_server
from assets.game_files.game_info import Game
from assets.game_files.game_widgets import Icon_Button, Button, Image_Button
from assets.game_files.client_game_info import Client_Game_Info
from _thread import *
import pygame
from math import ceil

class Multiplayer(object):
    def __init__(self, surface, screen_size, FPS):
        self.surface = surface

        self.screen_size = screen_size

        # sections:
            # "MultiplayerMenu" - where you can choose localhost match or random match
            # "LocalhostMenu" - localhost match menu
            # "LocalhostMatch" - localhost match
            # "RandomMenu" - random match menu
        self.current_section = "MultiplayerMenu"

        # if it is already connected, don't try to connect again
        self.connected = False

        # network
        self.network = None

        # player_number (0/1)
        self.player_number = None

        # icon buttons
        size = self.screen_size[0] // 35
        self.exit_button = Icon_Button(self.surface, "assets\\game_images\\icons\\close_icon.png", self.screen_size[0] - 3 * size // 2, size // 2, size, size)

        space = self.screen_size[0] // 35
        size = self.screen_size[0] // 25

        self.back_to_localhost_menu_button = Icon_Button(self.surface, "assets\\game_images\\icons\\back_icon.png", self.screen_size[0] - size - space // 2, self.screen_size[1] - size - space // 2, size, size)

        # buttons

        # temporary ready button
        self.ready_button = Button(self.surface, "NOT READY!", 600, self.screen_size[1] - 100, 200, 100, (255, 0, 0), (0, 255, 0), 30)

        # temporary buzz button
        self.buzz_button = Button(self.surface, "BUZZ", 0, 0, 200, 100, (255, 255, 0), (0, 255, 255), 30)

        # CLIENT DATA
        self.client_game_info = Client_Game_Info(self.surface, screen_size, 0, self.screen_size[1], FPS, self.screen_size[1] // 15)

        self.fps = FPS

            #### BACKGROUND
        self.background_image = pygame.image.load("assets\\game_images\\background.jpg")
        # add 20 px to screen size to make sure that it blits over the enitre window(didn't remain 1 pixel uncovered)
        # I'll blit it at position (0 - 20 / 2, 0 - 20 / 2)
        self.background_image = pygame.transform.scale(self.background_image, (screen_size[0] + 20, screen_size[1] + 20))

            #### MULTIPLAYER MENU BUTTONS
        ### Localhost button
        # The image is 236 x 59, it's not 16:9 so I need to take care of how I resize it
        button_width = self.screen_size[0] // 8  # <- here I resize the button width

        # here I calculate with how much the button_width is bigger to know with how much to increase/decrease the height, just some simple math
        button_height = 59 + ceil(((button_width - 236) / 236) * 59)

        self.localhost_button = Image_Button(self.surface, "assets\\game_images\\texts\\local1.png", self.screen_size[0] // 2, 3 * self.screen_size[1] // 8, button_width, button_height)

        ### Public button
        # the size of the image is 253 x 59
        # Because no all the texts have the same length, I can't make "abc" the same size with "abcdefghij", so I will resize it after the % of how much bigger is the first text
        button_width2 = 253 + ceil(((button_width - 236) / 236) * 253)  # <- here I resize the button width

        # here I calculate with how much the button_width is bigger to know with how much to increase/decrease the height, just some simple math
        button_height2 = 59 + ceil(((button_width - 236) / 236) * 59)

        self.public_button = Image_Button(self.surface, "assets\\game_images\\texts\\public1_unavailable.png", self.screen_size[0] // 2, 5 * self.screen_size[1] // 8, button_width2, button_height2)

        ### Back to main menu icon button
        space = self.screen_size[0] // 35
        size = self.screen_size[0] // 25

        self.back_to_main_menu_button = Icon_Button(self.surface, "assets\\game_images\\icons\\back_icon.png", self.screen_size[0] - size - space // 2, self.screen_size[1] - size - space // 2, size, size)

            #### MULTIPLAYER LOCALHOST MENU BUTTONS
        ### Find match button
        # The image is 1280 x 720
        button_width3 = self.screen_size[0] // 4  # <- here I resize the button width

        # here I calculate with how much the button_width is bigger to know with how much to increase/decrease the height, just some simple math
        button_height3 = 720 + ceil(((button_width3 - 1280) / 1280) * 720)
        self.find_match_button = Icon_Button(self.surface, "assets\\game_images\\icons\\find_match.png", self.screen_size[0] // 2 - button_width3 // 2, self.screen_size[1] // 2 - button_height3 // 2, button_width3, button_height3)

        ### Back to multiplayer menu icon button
        space = self.screen_size[0] // 35
        size = self.screen_size[0] // 25
        self.back_to_multiplayer_menu_button = Icon_Button(self.surface, "assets\\game_images\\icons\\back_icon.png", self.screen_size[0] - size - space // 2, self.screen_size[1] - size - space // 2, size, size)

    def display_content(self):
        if self.current_section == "MultiplayerMenu":
            self.multiplayer_menu()
        elif self.current_section == "LocalhostMenu":
            self.localhost_menu()
        elif self.current_section == "PreparingSection":
            self.preparing_section()
        elif self.current_section == "LocalhostMatch":
            self.localhost_match()

    def multiplayer_menu(self):
        # Display the background image
        self.surface.blit(self.background_image, (-10, -10))

            #### BUTTONS DISPLAY
        # display "go to localhost section" button
        self.localhost_button.display()

        # display "go to public section" button
        self.public_button.display()

        # display back to main menu icon button
        self.back_to_main_menu_button.display()

    def localhost_menu(self):
        # Display the background image
        self.surface.blit(self.background_image, (-10, -10))

        # insert maybe an animation

            #### BUTTONS DISPLAY
        # display "back to multiplayer menu section" icon button
        self.back_to_multiplayer_menu_button.display()

        # display find match button
        self.find_match_button.display()

        # find match button clicked
        if self.find_match_button.status == True:
            # unset button
            self.find_match_button.status = False

            # change image button
            if self.find_match_button.change_image_flag == 0:
                self.find_match_button.icon_image = pygame.image.load("assets\\game_images\\icons\\searching.png")
            else:
                self.find_match_button.icon_image = pygame.image.load("assets\\game_images\\icons\\find_match.png")

            self.find_match_button.change_image_flag = abs(self.find_match_button.change_image_flag - 1)
            self.find_match_button.icon_image = pygame.transform.scale(self.find_match_button.icon_image, (self.find_match_button.rect[2], self.find_match_button.rect[3]))

            # connect/disconnect
            if self.connected:
                # disconnect
                self.connected = False
            else:
                # connect to find a match
                self.connect_to_play()

        # if connected, wait until an opponent appears
        if self.connected:
            try:
                # get the current game
                game = self.network.send("get")

                # opponent found
                if game.connected():
                    print("Match started...")
                    # go to match
                    self.current_section = "PreparingSection"
            except:
                print("Couldn't get the game, connection lost!")
                self.connected = False
                self.player_number = None
        elif self.player_number != None:
            # match finder cancelled
            try:
                self.player_number = None
                print("You're closing the game")
                self.network.send("close")
            # here, except is inevitable because when I send close to the server, it close the game first, then send a response,
                # so it's already close and it is not gonna send a response, sooo.. error -> except
            except:
                print("Server doesnt exist! (CLOSE TRY)")

    def connect_to_play(self):
        '''
        Short description:

        try:
            connect to an existing server
        except:
            try:
                create a server
                try:
                    connect to created server
                except:
                    can't connect
            except:
                cant't connect
        '''

        # if is not connected, try to connect
        if not(self.connected):
            # if the server isn't running, self.player_number will be None
            self.network = Network()
            self.player_number = self.network.get_p()

            # get player number
            try:
                self.player_number = int(self.player_number)
            except:
                pass

            # If no server is running, let's run one
            if self.player_number == None: # It means that the player couldn't connect to a server(probably it doesn't exist)
                #!!! Show smth to the player who created the server that will let him know that he is the host
                print("Creating the server..")

                # start a new thread and run the server
                start_new_thread(run_server, ())

                # and try to connect again
                self.network = Network()
                self.player_number = self.network.get_p()

                # get player number
                try:
                    self.player_number = int(self.player_number)
                except:
                    pass

            # if player successfully connected to the server, change the flag to True
            if self.player_number != None:
                self.connected = True

    def preparing_section(self):
        # change searching button from previous section
        self.find_match_button.text = "FIND MATCH"

        self.surface.fill((135, 206, 235))

        game = None
        # what to send to the server
        if self.client_game_info.timer_progression > 0:
            if self.client_game_info.client_ready:
                # change button text
                self.ready_button.text = "READY!"
                try:
                    data = self.client_game_info.airplanes[0].string_data
                    data += self.client_game_info.airplanes[1].string_data
                    data += self.client_game_info.airplanes[2].string_data
                    if len(data) != 9:
                        data = "71d84l83r"
                    game = self.network.send("ready" + data)
                except:
                    print("Couldn't get the game! (READY TRY)")
                    # show message and give option to go back
                    self.current_section = "LocalhostMenu"
                    self.connected = False
                    self.client_game_info.reset_data()
            else:
                # change button text
                self.ready_button.text = "NOT READY!"
                try:
                    game = self.network.send("unready")
                except:
                    print("Couldn't get the game! (GET TRY)")
                    # show message and give option to go back
                    self.current_section = "LocalhostMenu"
                    self.connected = False
                    self.client_game_info.reset_data()
        else:
            # change button text
            self.ready_button.text = "READY!"
            try:
                data = self.client_game_info.airplanes[0].string_data
                data += self.client_game_info.airplanes[1].string_data
                data += self.client_game_info.airplanes[2].string_data
                if len(data) != 9:
                    data = "71d84l83r"
                game = self.network.send("ready" + data)
            except:
                print("Couldn't get the game! (READY TRY)")
                # show message and give option to go back
                self.current_section = "LocalhostMenu"
                self.connected = False
                self.client_game_info.reset_data()

        self.client_game_info.run_timer()

        # DISPLAY THINGS

        # display game table
        self.display_table_grid(self.screen_size[0] // 20, self.screen_size[0] // 20, 0.41 * self.screen_size[0], self.client_game_info.table) # 0.425 = 42.5% of screen_size[0]
        # self.display_table_grid(0.53 * self.screen_size[0], self.screen_size[0] // 20, 0.41 * self.screen_size[0], self.client_game_info.table)

        # display opponent's status
        try:
            self.client_game_info.display_opponent_status(game.ready_to_play[abs(self.player_number - 1)])
        except:
            print("Couldn't get the game! (GET PLAYER STATUS)")
            # show message and give option to go back
            self.current_section = "LocalhostMenu"
            self.connected = False
            self.client_game_info.reset_data()

        # for transition, see game_control_panel.py
        try:
            if game.ready_to_play[0] and game.ready_to_play[1]:
                self.client_game_info.both_ready = True
        except:
            print("Couldn't get the game! (GET PLAYERS STATUS)")
            # show message and give option to go back
            self.current_section = "LocalhostMenu"
            self.connected = False
            self.client_game_info.reset_data()

        # display exit button
        self.exit_button.display()
        # exit button functionality
        if self.exit_button.status:
            exit()

        # display back to localhost menu button, the functionality code is in game_control_panel.py, in display_content()
        self.back_to_localhost_menu_button.display()

        self.ready_button.display()

        for i in range(3):
            self.client_game_info.airplanes[i].display()
            if self.client_game_info.client_ready == False:
                if not(self.client_game_info.airplanes[i].rotating):
                    # to move just one plane
                    flag = True
                    for j in range(3):
                        if j != i and self.client_game_info.airplanes[j].moving == True:
                            flag = False
                    if flag == True:
                        self.client_game_info.airplanes[i].check_for_moving()
                else:
                    self.client_game_info.airplanes[i].rotating = False

                if not(self.client_game_info.airplanes[i].moving):
                    pos_flag = self.client_game_info.airplanes[i].validate_pos(self.screen_size[0] // 20, self.screen_size[0] // 20, 0.41 * self.screen_size[0], self.client_game_info.table)
                    if pos_flag == (-1, -1):
                        self.client_game_info.airplanes[i].current_pos = self.client_game_info.airplanes[i].init_pos
                        self.client_game_info.airplanes[i].string_data = ""
                    else:
                        #print(pos_flag)
                        # correct positioning
                        self.client_game_info.airplanes[i].current_pos = (ceil(self.screen_size[0] / 20 + pos_flag[0] * self.client_game_info.airplanes[i].segment_dimension + self.client_game_info.airplanes[i].dimensions[0] / 2), ceil(self.screen_size[0] / 20 + pos_flag[1] * self.client_game_info.airplanes[i].segment_dimension + self.client_game_info.airplanes[i].dimensions[1] / 2))

                        # edit table
                        # delete old pos
                        for i1 in range(10):
                            for j1 in range(10):
                                if self.client_game_info.table[i1][j1] == i + 1:
                                    self.client_game_info.table[i1][j1] = 0
                        # add the new pos
                        if self.client_game_info.airplanes[i].direction == "l":
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0]] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1]][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1] + 2][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 2] = i + 1
                            self.client_game_info.table[pos_flag[1]][pos_flag[0] + 3] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 3] = i + 1
                            self.client_game_info.table[pos_flag[1] + 2][pos_flag[0] + 3] = i + 1
                            # edit string data
                            self.client_game_info.airplanes[i].string_data = str(pos_flag[1] + 1) + str(pos_flag[0]) + "l"
                        elif self.client_game_info.airplanes[i].direction == "d":
                            self.client_game_info.table[pos_flag[1]][pos_flag[0]] = i + 1
                            self.client_game_info.table[pos_flag[1]][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1]][pos_flag[0] + 2] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1] + 2][pos_flag[0]] = i + 1
                            self.client_game_info.table[pos_flag[1] + 2][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1] + 2][pos_flag[0] + 2] = i + 1
                            self.client_game_info.table[pos_flag[1] + 3][pos_flag[0] + 1] = i + 1
                            # edit string data
                            self.client_game_info.airplanes[i].string_data = str(pos_flag[1] + 3) + str(pos_flag[0] + 1) + "d"
                        elif self.client_game_info.airplanes[i].direction == "r":
                            self.client_game_info.table[pos_flag[1]][pos_flag[0]] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0]] = i + 1
                            self.client_game_info.table[pos_flag[1] + 2][pos_flag[0]] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1]][pos_flag[0] + 2] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 2] = i + 1
                            self.client_game_info.table[pos_flag[1] + 2][pos_flag[0] + 2] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 3] = i + 1
                            # edit string data
                            self.client_game_info.airplanes[i].string_data = str(pos_flag[1] + 1) + str(pos_flag[0] + 3) + "r"
                        elif self.client_game_info.airplanes[i].direction == "u":
                            self.client_game_info.table[pos_flag[1]][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0]] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1] + 1][pos_flag[0] + 2] = i + 1
                            self.client_game_info.table[pos_flag[1] + 2][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1] + 3][pos_flag[0]] = i + 1
                            self.client_game_info.table[pos_flag[1] + 3][pos_flag[0] + 1] = i + 1
                            self.client_game_info.table[pos_flag[1] + 3][pos_flag[0] + 2] = i + 1
                            # edit string data
                            self.client_game_info.airplanes[i].string_data = str(pos_flag[1]) + str(pos_flag[0] + 1) + "u"

    def display_table_grid(self, x, y, size, table):
        distance = size / 10
        for i in range(11):
            pygame.draw.line(self.surface, (84, 173, 209), (x, y + i * distance), (x + size, y + i * distance), 3)
            pygame.draw.line(self.surface, (84, 173, 209), (x + i * distance, y), (x + i * distance, y + size), 3)

        for i in range(10):
            for j in range(10):
                if table[i][j] != 0:
                    rect = (x + distance * j, y + distance * i, distance, distance)
                    pygame.draw.rect(self.surface, (255, 0, 0), rect)

    def localhost_match(self):
        """if self.player_number == None:
            # display a message about that and change section
            self.current_section = "LocalhostMenu"
        else:
            # got the player, so now, let's play
            try:
                game = self.network.send("ready")
                print(game.ready_to_play)
            except:
                # display a message about that and change section
                self.current_section = "LocalhostMenu"
                print("Couldn't get a game")"""
        # change searching button from previous section
        self.find_match_button.text = "FIND MATCH"

        self.surface.fill((255, 255, 255))

        # display things
        self.buzz_button.display()

        if self.buzz_button.status == True:
            # unset button
            self.buzz_button.status = False

            try:
                game = self.network.send("buzz")
                print("Player", self.player_number, "has the next values:")
                print("Plane1:", game.moves[self.player_number]["plane1"])
                print("Plane2:", game.moves[self.player_number]["plane2"])
                print("Plane3:", game.moves[self.player_number]["plane3"])
            except:
                # show message and give option to go back
                self.current_section = "LocalhostMenu"
                self.connected = False
        else:
            try:
                game = self.network.send("get")
            except:
                pass

            if game == None:
                print("the server doesnt exist anymore")
                # show message and give option to go back
                self.current_section = "LocalhostMenu"
                self.connected = False