from Class_Projet import Client


client = Client()
client.start()
choix = client.bind()


if choix == "1":
    while True:
        client.receive()
        cmd = input()
        client.send(cmd)
        if cmd == "quit":
            client.quit()
        else:
            client.receive()
elif choix == "2":
    client.choice_information()
