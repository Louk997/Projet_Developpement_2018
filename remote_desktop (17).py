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
    choice = "1"
elif args.informations:
    choice = "2"
else:
    choice = client.main_menu()

while choice != "0" and choice is not None:
    client.send(choice)
    if choice == "1":
        while choice != "4":
            print(client.receive(), end="")
            cmd = input()
            client.send(cmd)
            if cmd == "quit":
                client.quit()
            elif cmd == "menu":
                choice = "4"
            else:
                print(client.receive(), end="")

    elif choice == "2":
        if args.informations == "computername":
            choice2 = "1"
        else:
            choice2 = client.display_choice()

        client.choice_information(choice2)

    choice = client.main_menu()