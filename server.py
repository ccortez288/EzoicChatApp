#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

"""
This function accepts incoming connection then prompts for a name. 
It also launches another thread for asynch processsing. THe other thread
handles client connections. 
"""
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Please type your name and press enter", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

"""
This function handles client connections on a separate thread to allow for multiple sessions to connect to chat
at the same time. It accepts a users name and sets that as the ID for their messages. 
This is also where messages get sent from. WHen a user passes in a message from the GUI, 
this function calls the share_msg function which goes through all the active client sessions
and sends the message from the websocket. 
"""
def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! Type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s joined the chat!" % name
    share_msg(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            share_msg(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            share_msg(bytes("%s left the chat." % name, "utf8"))
            break

"""
This function receives the message and name of person sending it form the respective client, 
then sends that message out to all clients and displays it on their GUI
"""
def share_msg(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
