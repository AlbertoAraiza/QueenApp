from flask import Blueprint, jsonify, request
from models.role_names import RoleNames
from models.client import Client
from flask_jwt_extended import create_access_token, jwt_required, current_user
from datetime import datetime, timedelta
from utils.db import db


api = Blueprint("api", __name__)
@api.route('/clientList')
def clientList():
    return jsonify({"hola": "mundo", "adios":"amor"})

@api.route("/")
@jwt_required()
def testAddress():
    return jsonify(
        id = current_user.id,
        first_name = current_user.first_name,
        last_name = current_user.last_name,
    )

@api.route("/update", methods=["POST"])
def passwordUpdate():
    phoneNumber = request.json.get("phone_number", None)
    deviceId = request.json.get("device_id", None)
    client = Client.query.filter_by(phone_number = phoneNumber).one_or_none()
    print(f"phone_number: {phoneNumber}, device_id: {deviceId}")
    print(f"client: {client}")

    if client is None:
        return "Error: No client", 400
    client.device_hash = deviceId
    db.session.commit()
    return "password updated"

@api.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    client = Client.query.filter_by(phone_number = username).one_or_none()
    print(f"client: {client}")
    if client is None:
        return jsonify({"msg": "Número de teléfono inválido", "code": "1"})
    if client and client.device_hash == password:
        now = datetime.now()
        exp = now + datetime.timedelta(1)
        access_token = create_access_token(identity=client, expires_delta = exp, code = 0)
        return jsonify(access_token=access_token, expires = exp)
    else: return jsonify({"msg": "Identificador incorrecto", "code":"2"})