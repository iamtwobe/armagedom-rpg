

def update_user(api, cmd):
    # ex: "update_user 3 Lian"
    _, user_id, name = cmd.split(maxsplit=2)
    resp = api.send("update_user", {"id": int(user_id), "name": name})
    print("→", resp)