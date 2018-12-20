from Class_Projet import *

"""def menu():"""


client = Client()
client.start()
s = client.get_my_socket()
distant_socket, addr = s.accept()
print("Connection accepted for :", addr)
hostname = client.get_hostname(distant_socket)

"""menu()"""

while True:
    cmd = input(str(addr[0])+"@"+str(hostname)+">")
    if cmd == "quit":
        client.send(distant_socket, cmd)
        client.quit(distant_socket)
    else:
        print("Me : " + cmd)
        client.send(distant_socket, cmd)
        client.receive(distant_socket)
