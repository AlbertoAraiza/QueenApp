from flask import Flask
from routes.clients import clients
from routes.api import api
from routes.tickets import tickets
from routes.job_api import job_api
from models.client import Client
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from utils.config import secret_key, database_uri, jwt_secret, track_modifications, pool_timeout, pool_recycle, pool_pre_ping
import git, os
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)

app.secret_key = secret_key
app.config["SQLALCHEMY_DATABASE_URI"]= database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = track_modifications
app.config['SQLALCHEMY_POOL_TIMEOUT'] = pool_timeout
app.config['SQLALCHEMY_POOL_RECYCLE'] = pool_recycle
app.config['SQLALCHEMY_POOL_PRE_PING'] = pool_pre_ping
app.config["JWT_SECRET_KEY"] = jwt_secret

tempdb = SQLAlchemy(app)
tempma = Marshmallow(app)

Migrate(app, tempdb)
jwt = JWTManager(app, True)
path = os.path.abspath(os.path.dirname(__file__)) + "\\utils\\firebase-adminsdk.json"
print(path)
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)

app.register_blueprint(clients)
app.register_blueprint(api, url_prefix="/api/customers")
app.register_blueprint(tickets, url_prefix="/api/tickets")
app.register_blueprint(job_api, url_prefix="/api/jobs")

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

@app.route("/git_update", methods=["POST"])
def git_update():
    repo = git.Repo("./QueenApp")
    origin = repo.remotes.origin
    repo.create_head('master',origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
    origin.pull()
    return '', 200