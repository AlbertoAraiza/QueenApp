from flask import Flask
from routes.clients import clients
from routes.api import api
from routes.tickets import tickets
from models.client import Client
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from utils.config import secret_key, database_uri, jwt_secret, track_modifications
app = Flask(__name__)

app.secret_key = secret_key
app.config["SQLALCHEMY_DATABASE_URI"]= database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = track_modifications
app.config["JWT_SECRET_KEY"] = jwt_secret

tempdb = SQLAlchemy(app)
Migrate(app, tempdb)
jwt = JWTManager(app, True)

app.register_blueprint(clients)
app.register_blueprint(api, url_prefix="/api/customers")
app.register_blueprint(tickets, url_prefix="/api/tickets")

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(client):
    print (f"client {client}")
    return client.id

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Client.query.filter_by(id=identity).one_or_none()