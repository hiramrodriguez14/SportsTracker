from flask import Blueprint, request, jsonify
from app.handler.handler_user import UserHandler

auth_routes = Blueprint("auth_routes", __name__)
handler = UserHandler()

@auth_routes.route("/signup", methods=["POST"])
def signup():
    data = request.json
    result, status = handler.signup(data)
    return jsonify(result), status

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    result, status = handler.login(data)
    return jsonify(result), status
