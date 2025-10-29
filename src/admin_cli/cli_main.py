from admin_cli.connectors import AdminAPI
from admin_cli.commands import user_cmds, announce_cmds


def main(api):
    print("Admin CLI conectada ao servidor.")
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
    api = AdminAPI()

    main(api)
