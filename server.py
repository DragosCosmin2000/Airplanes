import socket
from _thread import *
import sys
from player import Player
import pickle

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

# keep track of players
players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]

def threaded_client(conn, player):
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

# keep track of current player to know what to send and who's gonna receive that
current_player = 0

# looking for connections
while True:
    # wait to get a connection
    conn, addr = s.accept()
    print("Connected to:", addr)

    # start connected client
    start_new_thread(threaded_client, (conn, current_player))

    # increase number of players
    current_player += 1