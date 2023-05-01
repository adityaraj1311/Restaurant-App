from config import db

class OrderDetails(db.Model):
    __tablename__ = 'orderDetails'
    id = db.Column(db.Integer, primary_key=True)
    phoneNo = db.Column(db.String(200), db.ForeignKey("user.phoneNo"))#NOTE phoneNo is a foreign key pointing to user table
    date = db.Column(db.String(200), nullable=False)
    restaurant_name = db.Column(db.String(200), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    item_price = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(200), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
