from utils.db import db, ma

class Client(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email  = db.Column(db.String(50))
    phone_number = db.Column(db.String(10))
    device_hash = db.Column(db.String(50))
    role_name = db.Column(db.String(50))

    def __init__(self, first_name, last_name, email, phone_number, device_hash, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
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
    email = ma.auto_field()
    phone_number = ma.auto_field()
    role_name = ma.auto_field()

client_schema = ClientSchema(many = True)