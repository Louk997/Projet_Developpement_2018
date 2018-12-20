from Class_Projet import *


client = Client()
client.start()
choix = client.bind()


if choix == "1":
    client.receive()
    while True:
        cmd = input()
        client.send(cmd)
        if cmd == "quit":
            client.quit()
        else:
            client.receive()
elif choix == "2":
    client.choice_information()
