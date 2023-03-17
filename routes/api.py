from flask import Blueprint, jsonify, request, json
from models.role_names import RoleNames
from models.client import Client, client_schema
from flask_jwt_extended import create_access_token, jwt_required, current_user
from datetime import datetime, timedelta
from utils.db import db
from utils.send_notifications import sendNotification
from utils.functions import *

api = Blueprint("api", __name__)
@api.route('/clientList')
def clientList():
    return jsonify({"hola": "mundo", "adios":"amor"})

@api.route('/validatePhoneNumber')
def validatePhoneNumber():
    phoneNumber = request.args.get("phone_number", "", str)
    client = dbQuery(phoneNumber, findClientByPhoneNumber)
    if client:
        return jsonify({"valid": True})
    else:
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
    client = dbQuery(phoneNumber, findClientByPhoneNumber)
    if client:
        client.device_hash = deviceId
        client.fcm_token = fcmToken
        updateObject(client)
        return "password updated"
    else: return "Error: No client", 400

@api.route("/update_data", methods=["POST"])
def updateData():
    response = "bad request", 404
    customerId = request.json.get("customer_id", None)
    phoneNumber = request.json.get("phone_number", "")
    firstName = request.json.get("first_name","")
    lastName = request.json.get("last_name","")
    print(f"customerId: {customerId}")
    print(f"phoneNumber: {phoneNumber}")
    print(f"firstName: {firstName}")
    print(f"lastName: {lastName}")

    client = dbQuery(phoneNumber, findClientByPhoneNumber)
    print(f"client: {client}")
    if client and client.id != customerId: response = "0"
    else:
        if customerId:
            client = dbQuery(customerId, findClientById)
            print(f"client: {client}")
            if client:
                client.first_name = firstName
                client.last_name = lastName
                client.phone_number = phoneNumber
                updateObject(client)
                response = "1"
    return response

@api.route("/login", methods=["POST"])
def login():
    response = "bad request", 404
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    client = dbQuery(username, findClientByPhoneNumber)
    print(client.device_hash)
    if client is None:
        response = jsonify({"msg": "Número de teléfono inválido", "code": "1"})
    if client and client.device_hash == password:
        now = datetime.now()
        exp = now + timedelta(1)
        print(exp)
        access_token = create_access_token(identity=client, expires_delta = timedelta(1))
        print("returning")
        response = jsonify(access_token=access_token, expires = exp.strftime("%H:%M:%S %d-%m-%Y"))
    else:
        print("returning")
        response = jsonify({"msg": "Identificador incorrecto", "code":"2"})
    return response


@api.route("/add", methods=["POST"])
@jwt_required()
def addCustomer():
    response = "bad request", 401
    phoneNumber=request.json.get("phone_number", None),
    client = dbQuery(phoneNumber, findClientByPhoneNumber)
    if client: response = "0"
    else :
        newClient = Client(
            first_name=request.json.get("first_name", None),
            last_name=request.json.get("last_name", None),
            phone_number= phoneNumber,
            fcm_token = "",
            device_hash="",
            role = RoleNames.CUSTOMER)
        updateObject(newClient)
        response = "1"
    return response

@api.route("/user_role_name", methods=["GET"])
@jwt_required()
def listOrders():
    return jsonify({"role_name": current_user.role_name})

@api.route("/list", methods=["GET"])
@jwt_required()
def customersList():
    response = "bad request", 404
    phoneNumber = request.args.get("phone_number", "", str)
    clients = dbQuery(phoneNumber, findClients)
    response = client_schema.dump(clients)
    return response

@api.route("/addAdmin", methods=["POST"])
def addAdmin():
    phoneNumber = request.json.get("phone_number", None)
    newClient = dbQuery(phoneNumber, findClientByPhoneNumber)
    #newClient = Client.query.filter_by(phone_number=phoneNumber).one_or_none()
    if newClient: newClient.role_name = RoleNames.ADMIN.name
    else:
        newClient = Client(
            first_name = request.json.get("first_name", None),
            last_name = request.json.get("last_name", None),
            fcm_token = request.json.get("fcm_token", None),
            phone_number = request.json.get("phone_number", None),
            device_hash = request.json.get("device_hash", None),
            role = RoleNames.ADMIN)
    updateObject(newClient)
    return jsonify({"msg": "Success"})