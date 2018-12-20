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
client.conn()

if args.shell:
    choix = "1"
elif args.informations:
    choix = "2"
else:
    choix = client.main_menu()


client.send(choix)
if choix == "1":
    while True:
        print(client.receive(), end="")
        cmd = input()
        client.send(cmd)
        if cmd == "quit":
            client.quit()
        else:
            print(client.receive(), end="")

elif choix == "2":
    if args.informations == "computername":
        choix2 = "1"
    else:
        choix2 = client.display_choice()

    client.choice_information(choix2)
