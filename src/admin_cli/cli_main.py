from admin_cli.connectors.http_connector import AdminAPI
from admin_cli.commands import user_cmds, announce_cmds

api = AdminAPI()

def main():
    print("🌐 Admin CLI conectada ao servidor Flask!")
    while True:
        cmd = input("> ").strip()
        if cmd == "exit":
            break
        elif cmd.startswith("update_user"):
            user_cmds.update_user(api, cmd)
        elif cmd.startswith("broadcast"):
            announce_cmds.broadcast(api, cmd)
        else:
            print("Comando não reconhecido")

if __name__ == "__main__":
    main()
