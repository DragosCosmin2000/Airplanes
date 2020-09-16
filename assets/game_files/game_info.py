class Game(object):
    def __init__(self, game_id):
        self.game_id = game_id

        # False until two players are connected to the current game
        self.match_found = False

        # Become True after both players pushed ready button
        # Every player have 1 min to place the planes
        self.ready_to_play = [False, False]

        # planes positions and hit flags
        '''
            keys = planes
            values = a tuple of:
                -> coords of the head + direction
                Ex: { "abc" | a = row, b = col, c = direction }
                      0   0
            head -> 0 0 0 0
                      0   0
            Above plane has left direction
                -> flag to know if the plane got hitted on the head
        '''
        the_player = {
            "plane1": ["", False],
            "plane2": ["", False],
            "plane3": ["", False]
        }
        self.moves = [the_player, the_player]

        # player last move
        self.last_move = [None, None]

        # if current player made move
        self.players_went = [False, False]

        # player turn
        self.turn = 0

        # to close the game
        self.match_deleted = False

    def get_player_last_move(self, player_number):
        """
        :param player_number: [0, 1]
        :return: (x, y)
        """
        return self.last_move[player_number]

    def get_planes(self, player_number, planes):
        self.moves[player_number]["plane1"][0] = planes[0:3]
        self.moves[player_number]["plane2"][0] = planes[3:6]
        self.moves[player_number]["plane3"][0] = planes[6:9]

    def reset_planes(self, player_number):
        the_player = {
            "plane1": ["", False],
            "plane2": ["", False],
            "plane3": ["", False]
        }
        if player_number == 0:
            self.moves = [the_player, self.moves[1]]
        else:
            self.moves = [self.moves[0], the_player]

    def play(self, player_number, move):
        # edit moves
        self.last_move[player_number] = move
        self.players_went[player_number] = True

        return self.check_if_hit(player_number, move)

    def check_if_hit(self, player_number, move):
        for i in range(1, 4):
            plane_coords = (
                #                   opponent            plane_number tuple_obj string_index
                int(self.moves[abs(player_number - 1)]["plane" + str(i)][0][0]),
                int(self.moves[abs(player_number - 1)]["plane" + str(i)][0][1])
            )
            plane_direction = self.moves[abs(player_number - 1)]["plane" + str(i)][0][2]
            if move[0] == plane_coords[0] and move[1] == plane_coords[1]:
                self.moves[player_number]["plane" + str(i)][1] = True
                return 1 # for head hit

            # left direction
            if plane_direction == "l":
                if (move[0] == plane_coords[0] and move[1] == plane_coords[1] + 1) or \
                    (move[0] == plane_coords[0] - 1 and move[1] == plane_coords[1] + 1) or \
                    (move[0] == plane_coords[0] + 1 and move[1] == plane_coords[1] + 1) or \
                    (move[0] == plane_coords[0] and move[1] == plane_coords[1] + 2) or \
                    (move[0] == plane_coords[0] and move[1] == plane_coords[1] + 3) or \
                    (move[0] == plane_coords[0] - 1 and move[1] == plane_coords[1] + 3) or \
                    (move[0] == plane_coords[0] + 1 and move[1] == plane_coords[1] + 3):
                    return 0 # hit, but not the head

            # right direction
            if plane_direction == "r":
                if (move[0] == plane_coords[0] and move[1] == plane_coords[1] - 1) or \
                    (move[0] == plane_coords[0] - 1 and move[1] == plane_coords[1] - 1) or \
                    (move[0] == plane_coords[0] + 1 and move[1] == plane_coords[1] - 1) or \
                    (move[0] == plane_coords[0] and move[1] == plane_coords[1] - 2) or \
                    (move[0] == plane_coords[0] and move[1] == plane_coords[1] - 3) or \
                    (move[0] == plane_coords[0] - 1 and move[1] == plane_coords[1] - 3) or \
                    (move[0] == plane_coords[0] + 1 and move[1] == plane_coords[1] - 3):
                    return 0  # hit, but not the head

            # up direction
            if plane_direction == "u":
                if (move[0] == plane_coords[0] + 1 and move[1] == plane_coords[1]) or \
                    (move[0] == plane_coords[0] + 1 and move[1] == plane_coords[1] - 1) or \
                    (move[0] == plane_coords[0] + 1 and move[1] == plane_coords[1] + 1) or \
                    (move[0] == plane_coords[0] + 2 and move[1] == plane_coords[1]) or \
                    (move[0] == plane_coords[0] + 3 and move[1] == plane_coords[1]) or \
                    (move[0] == plane_coords[0] + 3 and move[1] == plane_coords[1] - 1) or \
                    (move[0] == plane_coords[0] + 3 and move[1] == plane_coords[1] + 1):
                    return 0  # hit, but not the head

            # down direction
            if plane_direction == "d":
                if (move[0] == plane_coords[0] - 1 and move[1] == plane_coords[1]) or \
                    (move[0] == plane_coords[0] - 1 and move[1] == plane_coords[1] - 1) or \
                    (move[0] == plane_coords[0] - 1 and move[1] == plane_coords[1] + 1) or \
                    (move[0] == plane_coords[0] - 2 and move[1] == plane_coords[1]) or \
                    (move[0] == plane_coords[0] - 3 and move[1] == plane_coords[1]) or \
                    (move[0] == plane_coords[0] - 3 and move[1] == plane_coords[1] - 1) or \
                    (move[0] == plane_coords[0] - 3 and move[1] == plane_coords[1] + 1):
                    return 0  # hit, but not the head

        return -1 # no hit

    def connected(self):
        return self.match_found

    def ready_to_start(self):
        return (self.ready_to_play[0] and self.ready_to_play[1])

    def get_winner(self):
        # player 1 won
        if self.moves[0]["plane1"][1] == self.moves[0]["plane2"][1] and self.moves[0]["plane2"][1] == self.moves[0]["plane3"][1] and self.moves[0]["plane3"][1] == True:
            return 1

        # player 0 won
        if self.moves[1]["plane1"][1] == self.moves[1]["plane2"][1] and self.moves[1]["plane2"][1] == self.moves[1]["plane3"][1] and self.moves[1]["plane3"][1] == True:
            return 0

        # still playing
        return -1

    def rematch(self):
        self.ready_to_play = [False, False]

        the_player = {
            "plane1": ["", False],
            "plane2": ["", False],
            "plane3": ["", False]
        }
        self.moves = [the_player, the_player]

        self.last_move = [None, None]

        self.players_went = [False, False]

        self.turn = 0
