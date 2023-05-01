from config import db

class User(db.Model):
    __tablename__ = 'user'
    phoneNo = db.Column(db.String(200), primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    #mentions the tables that are trying to point to user
    orderDetails = db.relationship("OrderDetails", backref="user")