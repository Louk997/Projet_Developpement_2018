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
    while True:
        choix2 = client.choice_information()
        if choix2 == "1":
            client.send("computer")
        if choix2 == "2":
            client.send("computer")
        if choix2 == "3":
            client.send("computer")
        if choix2 == "4":
            client.send("computer")
        if choix2 == "5":
            client.send("computer")
