from flask import Blueprint, jsonify, request, json
from models.role_names import RoleNames
from models.Job import Job, job_schema
from flask_jwt_extended import create_access_token, jwt_required, current_user
from datetime import datetime, timedelta
from utils.db import db


job_api = Blueprint("job_api", __name__)
@job_api.route('/JobList', methods=['GET'])
@jwt_required()
def clientList():
    phone_number = request.args.get("phone_number", "", str)
    jobs = Job.query.filter_by(phone_number = phone_number).all()
    return job_schema.dump(jobs)

@job_api.route("/add", methods=["POST"])
@jwt_required()
def addCustomer():
    print(request.json.get("id", None))
    newJob = Job(
        id = request.json.get("id", None),
        client_name = request.json.get("client_name", None),
        phone_number = request.json.get("phone_number", None),
        final_price = request.json.get("final_price", None),
        payment = request.json.get("payment", None),
        description = request.json.get("description", None),
        status = request.json.get("status", None),
        deliver_date = request.json.get("deliver_date", None)
    )
    db.session.add(newJob)
    db.session.commit()
    return jsonify({"msg": "Success"})