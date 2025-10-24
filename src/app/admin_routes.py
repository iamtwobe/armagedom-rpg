from flask import request, jsonify, abort, render_template
from src.app import users_database, admin_bp
from .models import User


API_KEY = "beewee"

def require_auth():
    if request.headers.get("X-API-Key") != API_KEY:
        abort(403)

@admin_bp.route("/update_user", methods=["POST"])
def update_user():
    require_auth()
    data = request.json
    user = users_database.session.get(User, data["id"])
    user.name = data["name"]
    users_database.session.commit()
    return jsonify({"status": "ok", "message": "Usuário atualizado"})

@admin_bp.route("/test", methods=["GET"])
def test():
    return render_template('index.html')