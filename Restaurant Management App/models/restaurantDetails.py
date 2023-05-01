from config import db

class RestaurantDetails(db.Model):
    __tablename__ = 'restaurantDetails'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(200), db.ForeignKey("restaurantName.restaurant_name"))
    item_type = db.Column(db.String(200), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    item_price = db.Column(db.String(200),nullable=False)
    rating = db.Column(db.Float, nullable=False)
    reviewer_count = db.Column(db.Integer, nullable=False)
