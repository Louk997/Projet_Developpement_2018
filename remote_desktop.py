from Class_Projet import *

client = Client()
client.start()
client.bind()

while True:
    cmd = input()
    if cmd == "quit()":
        client.send(cmd)
        client.quit()
    else:
        print("Me : " + cmd)
        client.send(cmd)
        client.receive()
