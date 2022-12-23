from flask import Blueprint, jsonify, request
from models.ticket import Ticket
from datetime import datetime
from utils.db import db

tickets = Blueprint("tickets", __name__)
@tickets.route('/VerifyAccess', methods=['GET'])
def verifyInAccess():
    jsonCode = request.args.get("code", "", str)
    print(jsonCode)
    ticket = Ticket.query.filter_by(code = jsonCode).one_or_none()
    if ticket:
        return jsonify({"Message": f"Ese boleto ya ingreso a las {ticket.time}"}), 301
    else:
        now = datetime.now()
        stringNow = now.strftime("%d/%m/%Y %H:%M:%S")
        newTicket = Ticket(jsonCode, stringNow)
        db.session.add(newTicket)
        db.session.commit()
        return jsonify({"Message": "Acceso autorizado"})

@tickets.route('/VerifySortieOut', methods=['GET'])
def verifySortieOut():
    jsonCode = request.args.get("code", "", str)
    print(jsonCode)
    ticket = Ticket.query.filter_by(code = jsonCode).one_or_none()
    if ticket:
        if ticket.status == 0:
            ticket.status = 1
            db.session.commit()
            return jsonify({"Message": "Salida autorizada"})
        else:
            return jsonify({"Message": "Salida no autorizada"}), 301
    else:
        return jsonify({"Message": f"Ese codigo no registro acceso"}), 301

@tickets.route('/VerifySortieIn', methods=['GET'])
def verifySortieIn():
    jsonCode = request.args.get("code", "", str)
    print(jsonCode)
    ticket = Ticket.query.filter_by(code = jsonCode).one_or_none()
    if ticket:
        if ticket.status == 1:
            ticket.status = 0
            db.session.commit()
            return jsonify({"Message": "Entrada autorizada"})
        else:
            return jsonify({"Message": "Entrada no autorizada"}), 301
    else:
        return jsonify({"Message": f"Ese codigo no registro acceso"}), 301