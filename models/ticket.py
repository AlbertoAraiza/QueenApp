from utils.db import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(100))
    time = db.Column(db.String(100))
    status = db.Column(db.Integer)

    def __init__(self, code, time):
        self.code = code
        self.time = time
        self.status = 0

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}