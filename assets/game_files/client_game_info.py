import pygame
from math import ceil
class Airplane(object):
    def __init__(self, surface, segment_dimension, init_pos, id):
        self.surface = surface
        self.segment_dimension = segment_dimension
        '''
            _     _
         _ | | _ | |
        |_     _   | <- a segment
           |_|   |_|
        
        '''

        self.direction = "l"
        self.image = pygame.image.load("assets\\game_images\\airplane_l.png")
        self.dimensions = (4 * self.segment_dimension, 3 * self.segment_dimension)
        self.image = pygame.transform.scale(self.image, (ceil(self.dimensions[0]), ceil(self.dimensions[1])))
        self.init_pos = init_pos
        self.current_pos = init_pos

        self.rotate_icon = pygame.image.load("assets\\game_images\\icons\\rotate_icon.png")
        self.rotate_icon = pygame.transform.scale(self.rotate_icon, (ceil(self.segment_dimension), ceil(self.segment_dimension)))

        self.moving = False
        self.rotating = False

        self.id = id

        self.string_data = ""

    def display(self):
        #if self.current_pos == self.init_pos:
        self.surface.blit(self.image, (self.current_pos[0] - self.dimensions[0] // 2, self.current_pos[1] - self.dimensions[1] // 2))
        #else:
        #self.surface.blit(self.image, self.current_pos)

        pos = pygame.mouse.get_pos()
        # display rotate icon
        if self.current_pos == self.init_pos:
            if self.init_pos[0] - self.segment_dimension // 2 <= pos[0] <= self.init_pos[0] + self.segment_dimension // 2 and self.init_pos[1] - self.segment_dimension // 2 <= pos[1] <= self.init_pos[1] + self.segment_dimension // 2:
                self.surface.blit(self.rotate_icon, (self.current_pos[0] - self.segment_dimension // 2, self.current_pos[1] - self.segment_dimension // 2))

    def rotate(self):
        if self.direction == "l":
            self.image = pygame.image.load("assets\\game_images\\airplane_d.png")
            self.direction = "d"
            self.dimensions = (self.dimensions[1], self.dimensions[0])
        elif self.direction == "d":
            self.image = pygame.image.load("assets\\game_images\\airplane_r.png")
            self.direction = "r"
            self.dimensions = (self.dimensions[1], self.dimensions[0])
        elif self.direction == "r":
            self.image = pygame.image.load("assets\\game_images\\airplane_u.png")
            self.direction = "u"
            self.dimensions = (self.dimensions[1], self.dimensions[0])
        else:
            self.image = pygame.image.load("assets\\game_images\\airplane_l.png")
            self.direction = "l"
            self.dimensions = (self.dimensions[1], self.dimensions[0])

        self.image = pygame.transform.scale(self.image, (ceil(self.dimensions[0]), ceil(self.dimensions[1])))

    def check_for_moving(self):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        # if mouse over an airplane
        if self.current_pos[0] - self.dimensions[0] // 2 <= mouse_pos[0] <= self.current_pos[0] + self.dimensions[0] // 2 and \
            self.current_pos[1] - self.dimensions[1] // 2 <= mouse_pos[1] <= self.current_pos[1] + self.dimensions[1] // 2:
            if mouse_pressed:
                self.moving = True
            else:
                self.moving = False
            if self.current_pos == self.init_pos:
                if self.init_pos[0] - self.segment_dimension // 2 <= mouse_pos[0] <= self.init_pos[0] + self.segment_dimension // 2 and self.init_pos[1] - self.segment_dimension // 2 <= mouse_pos[1] <= self.init_pos[1] + self.segment_dimension // 2:
                    self.moving = False

        if self.moving:
           self.current_pos = mouse_pos

    def validate_pos(self, x, y, size, table):
        coords = (self.current_pos[0] - self.dimensions[0] // 2 + self.segment_dimension // 2, self.current_pos[1] - self.dimensions[1] // 2 + self.segment_dimension // 2)
        indexes = ((coords[0] - x) // self.segment_dimension, (coords[1] - y) // self.segment_dimension)
        indexes = (ceil(indexes[0]), ceil(indexes[1]))
        # check the place to not be ocuppied
        if self.direction == "l":
            new_index = (indexes[0], indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1])
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 2)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 2, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 3, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 3, indexes[1])
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 3, indexes[1] + 2)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)
        elif self.direction == "d":
            new_index = (indexes[0], indexes[1])
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1])
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 2, indexes[1])
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0], indexes[1] + 2)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 2)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 2, indexes[1] + 2)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 3)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)
        elif self.direction == "r":
            new_index = (indexes[0], indexes[1])
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0], indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0], indexes[1] + 2)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 2, indexes[1])
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 2, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 2, indexes[1] + 2)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 3, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)
        elif self.direction == "u":
            new_index = (indexes[0] + 1, indexes[1])
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0], indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 2, indexes[1] + 1)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 2)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0], indexes[1] + 3)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 1, indexes[1] + 3)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

            new_index = (indexes[0] + 2, indexes[1] + 3)
            if new_index[0] > 9 or new_index[1] > 9:
                return (-1, -1)
            else:
                if table[new_index[1]][new_index[0]] != 0 and table[new_index[1]][new_index[0]] != self.id:
                    return (-1, -1)

        if x <= coords[0] <= x + size and y <= coords[1] <= y + size:
            pass
        else:
            return (-1, -1)

        return indexes

class Client_Game_Info(object):
    def __init__(self, surface, screen_size, x, y, FPS, font_size):
        self.surface = surface

        self.screen_size = screen_size

        # timer position
        self.coords = (x, y)

        self.font = pygame.font.Font('assets\\game_fonts\\Rubik-Regular.ttf', font_size)
        self.font2 = pygame.font.Font('assets\\game_fonts\\Rubik-Regular.ttf', font_size // 2)

        self.client_ready = False

        # amount of time for placing the planes
        self.fps = FPS

        self.timer_progression = 60 * self.fps

        # for right bar
        self.left_margin = 0

        # if both players are ready or timer is over
        self.both_ready = False

        # for transition animation
        self.can_start = False

        pos1 = (0.53 * self.screen_size[0] + 2 * 0.041 * self.screen_size[0], 0.06 * self.screen_size[0] + 2 * 0.041 * self.screen_size[0])
        pos2 = (0.53 * self.screen_size[0] + 8 * 0.041 * self.screen_size[0], 0.06 * self.screen_size[0] + 2 * 0.041 * self.screen_size[0])
        pos3 = (0.53 * self.screen_size[0] + 4 * 0.041 * self.screen_size[0], 0.06 * self.screen_size[0] + 8 * 0.041 * self.screen_size[0])
        # ariplanes
        self.airplanes = [
            Airplane(self.surface, 0.041 * self.screen_size[0], pos1, 1),
            Airplane(self.surface, 0.041 * self.screen_size[0], pos2, 2),
            Airplane(self.surface, 0.041 * self.screen_size[0], pos3, 3)
        ]

        self.table = []
        for i in range(10):
            new_row = []
            for j in range(10):
                new_row.append(0)
            self.table.append(new_row)

    def reset_data(self):
        self.both_ready = False
        self.timer_progression = 60 * self.fps
        self.client_ready = False
        self.can_start = False
        self.table = []
        for i in range(10):
            new_row = []
            for j in range(10):
                new_row.append(0)
            self.table.append(new_row)

        pos1 = (0.53 * self.screen_size[0] + 2 * 0.041 * self.screen_size[0], 0.06 * self.screen_size[0] + 2 * 0.041 * self.screen_size[0])
        pos2 = (0.53 * self.screen_size[0] + 8 * 0.041 * self.screen_size[0], 0.06 * self.screen_size[0] + 2 * 0.041 * self.screen_size[0])
        pos3 = (0.53 * self.screen_size[0] + 4 * 0.041 * self.screen_size[0], 0.06 * self.screen_size[0] + 8 * 0.041 * self.screen_size[0])
        self.airplanes = [
            Airplane(self.surface, 0.041 * self.screen_size[0], pos1, 1),
            Airplane(self.surface, 0.041 * self.screen_size[0], pos2, 2),
            Airplane(self.surface, 0.041 * self.screen_size[0], pos3, 3)
        ]

    def run_timer(self):
        if self.timer_progression != 0:
            self.timer_progression -= 1

        self.display_timer()

    def display_timer(self):
        color = (255, 255, 255)
        text = str(self.timer_progression // self.fps)

        # timer text becomes red and replace 9 with 09, 8 with 08 and so on
        if self.timer_progression < 10 * self.fps: # 10 = 60 / 6 - means 10 seconds
            color = (255, 0, 0)
            text = "0" + text

        text = "TIMER: " + text

        # display timer
        text = self.font.render(text, True, color, (135, 206, 235))
        text_rect = text.get_rect()
        text_rect.center = (self.coords[0] + text.get_size()[0] // 2 + text.get_size()[0] // 20, self.coords[1] - text.get_size()[1] // 2 - text.get_size()[1] // 20)

        self.surface.blit(text, text_rect)

        if self.left_margin == 0:
            self.left_margin = self.coords[0] + text.get_size()[0] + text.get_size()[0] // 10

        # display right bar
        start_pos = (self.left_margin, self.coords[1] - text.get_size()[1])
        end_pos = (self.left_margin, self.coords[1] - text.get_size()[1] // 10)
        pygame.draw.line(self.surface, color, start_pos, end_pos, 3)

    def display_opponent_status(self, flag):
        color = (255, 255, 255)
        text = "Your opponent is not ready!"
        if flag:
            color = (255, 0, 0)
            text = "Your opponent is ready! Hurry up!"

        text = self.font2.render(text, True, color, (135, 206, 235))
        text_rect = text.get_rect()
        text_rect.center = (self.left_margin + text.get_size()[0] // 2 + text.get_size()[0] // 20, self.coords[1] - text.get_size()[1] - text.get_size()[1] // 20)

        self.surface.blit(text, text_rect)