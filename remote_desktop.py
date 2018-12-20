from Class_Projet import Client
import argparse
import time

client = Client()
parser = argparse.ArgumentParser(prog="Remote Desktop",
                                 description="Optional settings for a quick use of the program",
                                 prefix_chars="/-",
                                 add_help=False,
                                 conflict_handler="resolve")

parser.add_argument("/h", "--help", action="help", help="<<Show all the existing options>>")
parser.add_argument("/s", "--shell", action="store_true", help="<<Access directly to the remote shell>>")
parser.add_argument("/m", "--infomenu", action="store_true", help="<<Access directly to the information menu>>")
parser.add_argument("/i", "--informations", choices=["computername", "network", "currentuser", "allusers"],
                    help="<<Directly get informations>>")
parser.add_argument("/b", "/buffsize", type=int, choices=[1024, 2048, 4096, 8192, 16384], default=4096,
                    help="<<Choose an optional buffsize (default = 4096),>>")

args = parser.parse_args()


client.start()
client.conn()

if args.shell:
    choice = "1"
elif args.informations or args.infomenu:
    choice = "2"
else:
    choice = client.main_menu()

client.send(choice)
time.sleep(2)
while choice != "0" and choice is not None:
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
            client.info_arg("computer")
        if args.informations == "network":
            client.info_arg("network")
        if args.informations == "currentuser":
            client.info_arg("current")
        if args.informations == "allusers":
            client.info_arg("users")
        else:
            choice2 = client.display_choice()

        client.choice_information(choice2)

    choice = client.main_menu()
    client.send(choice)

client.quit()
