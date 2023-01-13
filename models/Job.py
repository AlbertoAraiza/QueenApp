#
# @PrimaryKey @ColumnInfo(name = "ID") var id :String = Uuid.randomUUID().toString(),
    #@ColumnInfo(name = "CLIENT_NAME") var clientName :String = "",
    #@ColumnInfo(name = "PHONE_NUMBER") var phoneNumber :String = "",
    #@ColumnInfo(name = "FINAL_PRICE") var finalPrice :Float = 0f,
    #@ColumnInfo(name = "PAYMENT") var payment :Float = 0f,
    #@ColumnInfo(name = "DECRIPTION") var description :String = "",
    #@ColumnInfo(name = "STATUS") var status :String = "",
    #@ColumnInfo(name = "DELIVER_DATE") var deliverDate : String = ""

from utils.db import db, ma

class Job(db.Model):
    id = db.Column(db.String(50), primary_key = True)
    client_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(10))
    final_price = db.Column(db.Float())
    payment = db.Column(db.Float())
    description  = db.Column(db.String(150))
    status = db.Column(db.String(10))
    deliver_date = db.Column(db.String(50))

    def __init__(self, id, client_name, phone_number, final_price, payment, description, status, deliver_date):
        self.id = id
        self.client_name = client_name
        self.phone_number = phone_number
        self.final_price = final_price
        self.payment = payment
        self.description = description
        self.status = status
        self.deliver_date = deliver_date

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class JobSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Job
    id = ma.auto_field()
    client_name = ma.auto_field()
    phone_number = ma.auto_field()
    final_price = ma.auto_field()
    payment = ma.auto_field()
    description = ma.auto_field()
    status = ma.auto_field()
    deliver_date = ma.auto_field()

job_schema = JobSchema(many = True)