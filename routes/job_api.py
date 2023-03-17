from flask import Blueprint, jsonify, request, json
from models.role_names import RoleNames

from models.client import Client
from models.Job import Job, job_schema

from flask_jwt_extended import create_access_token, jwt_required, current_user
from datetime import datetime, timedelta
from utils.db import db

from utils.send_notifications import sendNotification
from utils.functions import *

job_api = Blueprint("job_api", __name__)
@job_api.route('/JobList', methods=['GET'])
@jwt_required()
def JobList():
    phoneNumber = request.args.get("phone_number", "", str)
    client = dbQuery(phoneNumber, findClientByPhoneNumber)
    if client and client.jobs:
        data = job_schema.dump(client.jobs)
    else:
        data = []
    return data

@job_api.route("/add", methods=["POST"])
@jwt_required()
def addJob():
    phoneNumber = request.json.get("phone_number", None)
    description = request.json.get("description", None)
    print(request.json.get("id", None))
    print(phoneNumber)
    currentClient = dbQuery(phoneNumber, findClientByPhoneNumber)
    print(currentClient)
    if not currentClient:
        return 'bad request!', 400
    if currentClient.fcm_token:
        sendNotification(currentClient.fcm_token, "Nuevo encargo", f"{description} en proceso")
    newJob = Job(
        final_price = request.json.get("final_price", None),
        payment = request.json.get("payment", None),
        description = request.json.get("description", None),
        status = "Pendiente",#request.json.get("status", None),
        deliver_date = request.json.get("deliver_date", None),
        qr_code = request.json.get("qr_code", None),
        customer_id = currentClient.id
    )
    updateObject(newJob)
    return jsonify({"msg": "Success"})

@job_api.route("/completed", methods=["POST"])
@jwt_required()
def readyJob():
    jobId = request.json.get("id", None)
    oldJob = dbQuery(jobId, findJobById)
    if (oldJob is None):
        return jsonify({"msg": "invalid job", "code" : 0})
    else:
        if oldJob.customer.fcm_token: sendNotification(
            oldJob.customer.fcm_token,
            "Trabajo completado",
            f"{oldJob.description} esta listo para entregarse.")
        oldJob.status = "Listo"
        updateObject(oldJob)
        return jsonify({"msg": "job updated", "code" : 1})

@job_api.route("/delivered", methods=["POST"])
@jwt_required()
def completeJob():
    jobId = request.json.get("id", None)
    oldJob = dbQuery(jobId, findJobById)
    if (oldJob is None):
        return jsonify({"msg": "invalid job", "code" : 0})
    else:
        oldJob.status = "Completado"
        updateObject(oldJob)
        return jsonify({"msg": "job updated", "code" : 1})

@job_api.route("/update_payment", methods=["POST"])
@jwt_required()
def updatePayment():
    jobId = request.json.get("id", None)
    payment = request.json.get("payment", None)
    oldJob = dbQuery(jobId, findJobById)
    if (oldJob is None):
        return jsonify({"msg": "invalid job", "code": 0})
    else:
        oldJob.payment += payment
        updateObject(oldJob)
        return jsonify({"msg": "job updated", "code": 1})
