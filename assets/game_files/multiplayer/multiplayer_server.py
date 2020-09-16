import socket
from _thread import *
import pickle
from assets.game_files.game_info import Game

connected = set()
games = {}
id_count = 0
players_number = 0
first_connection_flag = True

def threaded_client(conn, player, gameId):
    global players_number, games, id_count

    # "confirmation token", send pos of current player
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        #print("while loop", player)
        try:
            #print("get in try", player)
            # receive some data, 2048 is the dimension of data
            #data = conn.recv(2048 * 2).decode()
            #print("after getting data", player)
            if gameId in games:
                game = games[gameId]

                # receive some data, 2048 is the dimension of data
                data = conn.recv(2048 * 2).decode()

                # if not data had been received, break
                if not data:
                    print("No data received")
                    break
                else:
                    #print(data, player)
                    # means that the player placed his planes and hit ready
                    if games[gameId].match_deleted:
                        break
                    if data == "get":
                        pass
                    elif data[:5] == "ready":
                        game.ready_to_play[player] = True
                        game.get_planes(player, data[5:])
                    elif data == "unready":
                        game.ready_to_play[player] = False
                        game.reset_planes(player)
                    elif data == "close":
                        print("close request")
                        break
                    elif data == "buzz":
                        print("HU | PL_NO. =", player, "| GAME_ID =", gameId, "--- buzzed")
                    # other stuffs

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                print("no game")
                break
        except:
            print("breakit bro")
            break

    print("Lost connection")
    if not(games[gameId].match_deleted):
        games[gameId].match_deleted = True
    else:
        try:
            del games[gameId]
            print("Closing game", gameId)
        except:
            pass

    try:
        # if it's just player 0 and he closed the game, delete it
        if not(games[gameId].connected()):
            id_count += 1
            del games[gameId]
            print("Closing game", gameId)
    except:
        pass

    players_number -= 1
    conn.close()

def run_server():
    global games, id_count, players_number, first_connection_flag

    # get local ip
    server = socket.gethostbyname(socket.gethostname())
    port = 5555

    # create the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    try:
        s.bind((server, port))
    except socket.error as e:
        print(e)

    # listen for connections
    s.listen()
    print("Waiting for a connection...")

    # looking for connections
    while True:
        # wait to get a connection
        conn, addr = None, None

        if first_connection_flag:
            conn, addr = s.accept()
            first_connection_flag = False
        else:
            if players_number == 0:
                break
            else:
                conn, addr = s.accept()

        print("Connected to:", addr)

        players_number += 1
        id_count += 1

        p = 0
        gameId = (id_count - 1) // 2

        if players_number % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...", gameId)
        else:
            games[gameId].match_found = True
            p = 1

        # start connected client
        start_new_thread(threaded_client, (conn, p, gameId))