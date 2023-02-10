from utils.db import db, ma
from models.Job import Job

class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    fcm_token = db.Column(db.String(300))
    phone_number = db.Column(db.String(10))
    device_hash = db.Column(db.String(50))
    role_name = db.Column(db.String(50))
    jobs = db.relationship('Job', backref='customer',lazy = True)

    def __init__(self, first_name, last_name, fcm_token, phone_number, device_hash, role):
        self.first_name = first_name
        self.last_name = last_name
        self.fcm_token = fcm_token
        self.phone_number = phone_number
        self.device_hash = device_hash
        self.role_name = role.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ClientSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Client
    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    fcm_token = ma.auto_field()
    phone_number = ma.auto_field()
    role_name = ma.auto_field()

client_schema = ClientSchema(many = True)