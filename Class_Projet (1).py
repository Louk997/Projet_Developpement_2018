import socket
import os
import sys

"""
Classe contenant les fonctions communes entre client et serveur
"""


class Machine:
    def __init__(self):
        self.server_addr = ("localhost", 60000)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.language = "utf-8"
        self.buffsize = 1024

    def get_my_socket(self):
        return self.my_socket


"""
Classe contenant les fonctions pour le client
"""


class Malware(Machine):
    def __init__(self):
        super().__init__()

    def start(self):
        self.my_socket.connect(self.server_addr)

    def send(self, commande):
        self.my_socket.send(commande.encode(self.language))

    def receive(self):
        return self.my_socket.recv(self.buffsize)

    def quit(self):
        self.my_socket.close()


"""
Classe contenant les fonction pour le malware
"""


class Client(Machine):
    def __init__(self):
        super().__init__()

    def start(self):
        self.my_socket.bind(self.server_addr)
        self.my_socket.listen()

    def send(self, distant_socket, message):
        distant_socket.send(message.encode(self.language))

    def receive(self, distant_socket):
        print(distant_socket.recv(self.buffsize))

    def quit(self, distant_socket):
        distant_socket.close()
        self.my_socket.close()
        sys.exit()
