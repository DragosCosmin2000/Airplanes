import pygame
from network import Network
from player import Player
# pygame initialization
pygame.init()



import socket
from _thread import *
import sys
import pickle

# keep track of players
players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]

def threaded_client(conn, player):
    print("Thread started")
    # "confirmation token", send pos of current player
    conn.send(pickle.dumps(players[player]))

    reply = ""
    while True:
        try:
            # receive some data, 2048 is the dimension of data
            data = pickle.loads(conn.recv(2048))

            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            # send data
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

def run_server():
    # get local ip
    server = "192.168.0.102"
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

    # keep track of current player to know what to send and who's gonna receive that
    current_player = 0

    # looking for connections
    while True:
        # wait to get a connection
        conn = 0
        addr = 0
        if current_player != 3:
            conn, addr = s.accept()
        else:
            print("stop")
            break

        print("Connected to:", addr)

        # start connected client
        start_new_thread(threaded_client, (conn, current_player))

        # increase number of players
        current_player += 1

# clock, framerate = 60 fps
clock = pygame.time.Clock()

def redrawWindow(surface, player, player2):
    surface.fill((255, 255, 255))

    # stuff
    player.draw(surface)
    player2.draw(surface)

    # update window
    pygame.display.update()

def main():
    global clock

    # create window
    # surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    surface = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Airplanes")

    n = Network()
    start_new_thread(run_server, ())
    import time
    time.sleep(5)
    print("I slept")
    # create player
    p = n.get_p()
    print(p)
    # main loop
    run = False
    FPS = 60
    while run:
        clock.tick(FPS)

        # update opponent and send me to him
        p2 = n.send(p)

        # quit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # check for movements
        p.move()

        redrawWindow(surface, p, p2)

if __name__ == "__main__":
    main()

    pygame.quit()