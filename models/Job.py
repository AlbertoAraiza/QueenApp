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
    id = db.Column(db.Integer, primary_key = True)
    final_price = db.Column(db.Float())
    payment = db.Column(db.Float())
    description  = db.Column(db.String(150))
    status = db.Column(db.String(10))
    deliver_date = db.Column(db.String(50))
    qr_code = db.Column(db.String(50), unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable = False)

    def __init__(self, final_price, payment, description, status, deliver_date, qr_code, customer_id):
        self.final_price = final_price
        self.payment = payment
        self.description = description
        self.status = status
        self.deliver_date = deliver_date
        self.qr_code = qr_code
        self.customer_id = customer_id
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class JobSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Job
    id = ma.auto_field()
    final_price = ma.auto_field()
    payment = ma.auto_field()
    description = ma.auto_field()
    status = ma.auto_field()
    deliver_date = ma.auto_field()
    qr_code = ma.auto_field()
    customer_id = ma.auto_field()

job_schema = JobSchema(many = True)