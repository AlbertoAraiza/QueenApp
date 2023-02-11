from flask import Blueprint, jsonify, request, json
from models.role_names import RoleNames
from models.client import Client, client_schema
from flask_jwt_extended import create_access_token, jwt_required, current_user
from datetime import datetime, timedelta
from utils.db import db
from utils.send_notifications import sendNotification

api = Blueprint("api", __name__)
@api.route('/clientList')
def clientList():
    return jsonify({"hola": "mundo", "adios":"amor"})

@api.route('/validatePhoneNumber')
def validatePhoneNumber():
    phoneNumber = request.args.get("phone_number", "", str)
    db.session()
    client = Client.query.filter_by(phone_number = phoneNumber).one_or_none()
    if client:
        db.session.close()
        return jsonify({"valid": True})
    else:
        db.session.close()
        return jsonify({"valid": False})

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
    fcmToken = request.json.get("fcm_token", None)
    db.session()
    client = Client.query.filter_by(phone_number = phoneNumber).one_or_none()
    print(f"phone_number: {phoneNumber}, device_id: {deviceId}")
    print(f"client: {client}")

    if client is None:
        db.session.close()
        return "Error: No client", 400
    client.device_hash = deviceId
    client.fcm_token = fcmToken
    db.session.commit()
    db.session.close()
    return "password updated"

@api.route("/login", methods=["POST"])
def login():
    print("Login")
    db.session()
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    print("params getted")
    query = Client.query.filter_by(phone_number = username)
    print(f"query: {query}")
    client = query.one_or_none()
    print(f"client: {client}")
    db.session.commit()
    if client is None:
        db.session.close()
        return jsonify({"msg": "Número de teléfono inválido", "code": "1"})
    if client and client.device_hash == password:
        #if client.fcm_token:
            #sendNotification(client.fcm_token, "Nuevo inicio de sesion", "Se ha registrado un nuevo inicio de sesion")
        now = datetime.now()
        exp = now + timedelta(1)
        print(exp)
        access_token = create_access_token(identity=client, expires_delta = timedelta(1))
        print("returning")
        db.session.close()
        return jsonify(access_token=access_token, expires = exp.strftime("%H:%M:%S %d-%m-%Y"))
    else:
        print("returning")
        db.session.close()
        return jsonify({"msg": "Identificador incorrecto", "code":"2"})


@api.route("/add", methods=["POST"])
@jwt_required()
def addCustomer():
    db.session()
    newClient = Client(
        first_name=request.json.get("first_name", None),
        last_name=request.json.get("last_name", None),
        fcm_token = "",
        phone_number=request.json.get("phone_number", None),
        device_hash="",
        role = RoleNames.CUSTOMER)
    db.session.add(newClient)
    db.session.commit()
    db.session.close()
    return jsonify({"msg": "Success"})

@api.route("/user_role_name", methods=["GET"])
@jwt_required()
def listOrders():
    print("HOLA MUNDO")
    return jsonify({"role_name": current_user.role_name})

@api.route("/list", methods=["GET"])
@jwt_required()
def customersList():
    db.session()
    clients = Client.query.all()
    db.session().close()
    return client_schema.dump(clients)

@api.route("/addAdmin", methods=["POST"])
def addAdmin():
    phoneNumber = request.json.get("phone_number", None)
    db.session()
    newClient = Client.query.filter_by(phone_number=phoneNumber).one_or_none()
    if newClient is None:
        newClient = Client(
            first_name = request.json.get("first_name", None),
            last_name = request.json.get("last_name", None),
            fcm_token = request.json.get("fcm_token", None),
            phone_number = request.json.get("phone_number", None),
            device_hash = request.json.get("device_hash", None),
            role = RoleNames.ADMIN)
        db.session.add(newClient)
    else:
        newClient.role_name = RoleNames.ADMIN.name
    db.session.commit()
    db.session.close()
    return jsonify({"msg": "Success"})