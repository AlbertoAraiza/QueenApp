from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.client import Client
from models.role_names import RoleNames
from utils.db import db

clients = Blueprint("clients", __name__)

@clients.route("/")
def index():
    clients = Client.query.all()
    return "Adios mundo"
    #return render_template("index.html", clients = clients)

@clients.route("/new",methods = ['POST'])
def add():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']
    device_id = request.form['device_id']
    newClient = Client(first_name, last_name, "jose@vargas.com",phone_number, device_id, RoleNames.ADMIN)
    db.session.add(newClient)
    db.session.commit()
    flash("Cliente agregado satisfactoriamente")
    return redirect(url_for('clients.index'))

@clients.route("/update/<id>", methods=["POST", "GET"])
def update(id):
    client = Client.query.get(id)
    if(request.method == "POST"):
        client.first_name = request.form["first_name"]
        client.last_name = request.form["last_name"]
        db.session.commit()
        flash("Cliente actualizado satisfactoriamente")
        return redirect(url_for('clients.index'))
    else:
        return render_template("update_client.html", client = client)

@clients.route("/delete/<id>")
def delete(id):
    client = Client.query.get(id)
    db.session.delete(client)
    db.session.commit()
    flash("Cliente eliminado correctamente")
    return redirect(url_for('clients.index'))