from config import db

class RestaurantName(db.Model):
    __tablename__ = 'restaurantName'
    restaurant_name = db.Column(db.String(200), primary_key=True)

    #mention the table names that you're trying to connect 
    restaurantDetails = db.relationship("RestaurantDetails", backref="restaurantName")