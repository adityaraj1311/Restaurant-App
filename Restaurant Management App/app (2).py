from flask import Flask, jsonify, request
from flask_cors import CORS #when cross origin request occur it let u handle manually and errors won't occur i.e Frontend and backend part can have different origins
from os import environ # retuns a dict having users' env var as keys and their values as values
from config import db, SECRET_KEY
from dotenv import load_dotenv #read key-value pair from .env file and set them as environmental varibles
from datetime import date, datetime

from models.restaurantName import RestaurantName
from models.restaurantDetails import RestaurantDetails
from models.user import User
from models.orderDetails import OrderDetails

def create_app(): #within this fn create a Flask class
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)
    print("DB Initialized Successfully")


    with app.app_context():
        # db.drop_all() 
        # whenever you're made changes to the database, uncomment db.drop_all(), run the .py file and then comment it
        # all entries of the table will be deleted #if you have made changes in db then only don't comment db.drop_all() else comment it 

        # global_phone_no = None
        # global_items_in_cart = None

        @app.route("/sign_up", methods=["POST"])
        def sign_up():
            user_details = request.get_json()
            #create an object 
            new_user_details = User(
                phoneNo = user_details["phoneNo"],
                username = user_details["username"],
                email = user_details["email"],
                address = user_details["address"]
            )
            db.session.add(new_user_details)
            db.session.commit()
            return "user successfully added"

        #NOTE 1st fill the table(restaurantName) to which a foreign key(fk of restaurantDetails i.e restaurant_name) is pointing to => bcz then only defn of FK satisfies i.e FK points to pk of an table provided that key should be there in the pointed table(i.e restaurantName)
        @app.route("/add_restaurant_names", methods=["POST"])
        def add_restaurant_names():
            """
                format in which we get restaurant names => i.e should be able to iterate => so list & that list be in a dict to be able to accept as a json
                =>  {
                        "name_list" : ["rest1", "rest2", "rest3", ...]
                    }
            """
            restaurant_names_list = request.get_json()
            name_list = restaurant_names_list["name_list"]
            for name in name_list:
                new_restaurant_name = RestaurantName(
                    restaurant_name = name
                )
                db.session.add(new_restaurant_name)
            db.session.commit()
            return "restaurants added successfully"

        @app.route("/add_items_to_menu", methods=["POST"])
        def add_items_to_menu():
            """NOTE
                we may want to push one item or tuple of the restaurantDetails or push multiple items at a time 
                so format could be 
                {
                    "list" : [
                            {},{},{},.....
                        ]
                }
                so inside a dictionary we've a list within which there are multiple dictionaries => iterate the list => get access to each dictionary and push it
            """
            menu_items = request.get_json()
            item_list = menu_items["list"]
            for item in item_list:
                #now item rep each of the dictionaries
                new_menu_item = RestaurantDetails(
                    restaurant_name = item["restaurant_name"],
                    item_type = item["item_type"],
                    item_name = item["item_name"],
                    item_price = item["item_price"],
                    rating = 0,
                    reviewer_count = 0 #NOTE initially just after adding an item to the menu => the rating and reviewer_count is 0
                )
                db.session.add(new_menu_item)
            db.session.commit()
            return "all the items has successfully been added"

        @app.route("/search_by_restaurant_name", methods=["GET"])
        def search_by_restaurant_names():
            """
                NOTE => user input => take (restaurant name) as a string then using query select all the tuples(NOTE using .all()) from (NOTE restaurantDetails) that has that restaurant_name => it returns a list (NOTE NOTE NOTE => say all the object references for which the condition of query satisfied => that list is iterable => so traverse to all the object references and access all of the attribute value for that object(NOTE using object reference.attribute name) in format => [{},{}]) => bcz we can append to a list
            """
            rest_name = request.args.get('rest_name')
            rest_name_items_list = RestaurantDetails.query.filter_by(restaurant_name = rest_name).all() #NOTE so we get all the object references that satisfied the condition => so put the details for those tuples in a dictionary which should be within a list
            #create an empty list within which the dictionaries should reside
            queried_menu = []
            for item_details in rest_name_items_list:
                queried_menu.append({
                    "restaurant_name" : item_details.restaurant_name,
                    "item_type": item_details.item_type,
                    "item_name": item_details.item_name,
                    "item_price": item_details.item_price,
                    "rating": item_details.rating,
                    "reviewer_count": item_details.reviewer_count
                })
            
            return queried_menu

        @app.route("/search_by_item_type", methods=["GET"])
        def search_by_item_type():
            item_type = request.args.get("item_type")
            rest_name_item_list = RestaurantDetails.query.filter_by(item_type = item_type).all()
            queried_menu = []
            for item_details in rest_name_item_list:
                queried_menu.append({
                    "restaurant_name" : item_details.restaurant_name,
                    "item_type": item_details.item_type,
                    "item_name": item_details.item_name,
                    "item_price": item_details.item_price,
                    "rating": item_details.rating,
                    "reviewer_count": item_details.reviewer_count
                })
            
            return queried_menu
        
        @app.route("/add_items_to_cart", methods=["POST"])
        def add_items_to_cart():
            """
                NOTE => after adding items to cart => user has 2 options => either place_order or cancel_order 
                && in the add_items_to_cart => user will be providing 
                phoneNo via params,
                {
                    "items1" : "quantity", "item2" : "quantity2", ....
                }
                we can store both the things in global variables and then if the user places order => we use them to NOTE 1) update in OrderDetails table
                2) get the totalSum, 3) return the list(dictionary.keys()) so that user can provide ratings for these these items in a format {"item" : rating, ...}
            """ 
            phoneNo = request.args.get("phoneNo")
            cart_items = request.get_json()

            # global_phone_no = phoneNo
            # global_items_in_cart = cart_items

            return "Items has successfully been added to cart, Do you wish to order the items or cancel the order ?"

        @app.route("/place_order", methods=["POST"])
        def place_order():
            # global 
            global_phone_no = request.args.get("phoneNo")
            global_items_in_cart = request.get_json()
            
            item_list = list(global_items_in_cart.keys())
            """
                NOTE => the no of items there are in the global_items_in_cart => only that many OrderDetails Objects we need to create

                After we're done with placing the order and updating in orderDetails and calculating totalSum => reset both the global var to None
            """
            totalOrderSum = 0
            for item in item_list:
                #query to find the restaurant name and the item price
                #NOTE item_price and quantity are Strings in all the tables
                rest_instance = RestaurantDetails.query.filter_by(item_name = item).first()
                item_price = rest_instance.item_price
                quantity = global_items_in_cart[item]
                cur_item_amount = int(item_price)*int(quantity)#NOTE cal cur item amount to add item price to totalSum for each itern
                totalOrderSum = totalOrderSum + cur_item_amount
                new_order_details = OrderDetails(
                    phoneNo = global_phone_no,
                    date = str(date.today()),
                    restaurant_name = rest_instance.restaurant_name,
                    item_name = item,
                    item_price = item_price,
                    quantity = quantity,
                    total_amount = cur_item_amount
                )
                db.session.add(new_order_details)
            db.session.commit()

            #NOTE jsonify is equivalent to sending a json separated by ","
            return jsonify(msg = "Order Succesfully Placed", total_amount_spent = totalOrderSum, put_ratings_for_following_items = item_list)

        @app.route("/cancel_order", methods=["GET"])
        def cancel_order():
            return "Your Order has been Cancelled"

        @app.route("/total_amount_ordered_on_date", methods=["GET"])
        def total_amount_ordered_on_date():
            """
                get the phoneNo from the user and get the date from the user => query it 
            """
            phoneNo = request.args.get("phoneNo")
            date = request.args.get("date")

            orderDetails_instance = OrderDetails.query.filter_by(phoneNo = phoneNo).all()
            #NOTE it retuns a list => containing all the references to the objects => now traverse all those references and for that particular date => sum up the total_amount
            total_amount_on_date = 0
            for orders in orderDetails_instance:
                if orders.date == date:
                    total_amount_on_date = total_amount_on_date + orders.total_amount

            return jsonify(total_amount_ordered_on_provided_date = total_amount_on_date)

        @app.route("/give_rating", methods=["POST"])
        def give_rating():
            """
                user specify the item for which he wants to give the rating => in format =>
                {
                    "item_rating_dictionary" : {item1 : rating, item2 : rating, item3 : rating, ...}
                }
                how should the rating be affected => 
                (rating*reviewer_count + cur_rating)/reviewer_count + 1 is the new rating which is to be updated
            """
            newer_item_rating_json = {}
            item_rating_dictionary = request.get_json()["item_rating_dictionary"]
            #NOTE traverse to all the item names and query their rating and reviewer_count from the restaurantDetails table => and for that instance only we have to update the rating
            item_names = list(item_rating_dictionary.keys())
            for item in item_names:
                #NOTE query the instance => query it via the item_name
                item_instance = RestaurantDetails.query.filter_by(item_name = item).first()

                older_reviewer_count = item_instance.reviewer_count
                older_rating = item_instance.rating
                cur_user_rating = item_rating_dictionary[item]
                new_reviewer_count = older_reviewer_count + 1
                newer_rating = (older_rating*older_reviewer_count + cur_user_rating)/(new_reviewer_count) 

                #NOTE now update the newer_rating and the reviewer count to the queried instance
                item_instance.rating = newer_rating
                item_instance.reviewer_count = new_reviewer_count
                newer_item_rating_json[item] = item_instance.rating

                db.session.commit()
            
            return jsonify(ratings_have_successfully_been_update = newer_item_rating_json)

        @app.route("/user_history", methods=["GET"])
        def user_history():
            """
                take phoneNo from user and query all the tuples => using .all() => returns a list of references => iterative the list of ref. and in a single itern => put all the attributes in a dict. and append to the list from the orderDetails table and put them in a json and return it
            json format => {phoneNo : [
                                        {
                                            date : {}
                                        },
                                        {
                                            date : {}
                                        },
                                        ....
                                    ]
                            }
            """
            phoneNo = request.args.get("phoneNo")
            orderDetails_list = OrderDetails.query.filter_by(phoneNo = phoneNo).all()
            user_history = {}
            # user_history[phoneNo] = "" 
            date_wise_list = []
            for orderDetails in orderDetails_list:
                #orderDetails rep each of orderDetails reference
                #create a dictionary with key as date : {}
                temp_dict = {
                    "restaurant_name" : orderDetails.restaurant_name,
                    "item_name" : orderDetails.item_name,
                    "item_price" : orderDetails.item_price,
                    "quantity" : orderDetails.quantity,
                    "total_amount" : orderDetails.total_amount
                }
                date_dict = {
                    orderDetails.date : temp_dict
                }
                date_wise_list.append(date_dict)
            user_history[phoneNo] = date_wise_list

            return jsonify(user_history_queried_for_phoneNo = phoneNo, user_history_is = user_history)

        @app.route("/contact_us", methods=["GET"])
        def contact_us():
            """
                get contact us details in the format 
                {
                    email : "",
                    phoneNo : "",
                    socials : {
                        "insta" : "",
                        "fb" : "",
                        "linkedin" : ""
                    }
                }
            """
            contact_us_dict = {
                "email" : "petpooja_clone@gmail.com",
                "phoneNo" : "88012133435",
                "socials" : {
                    "insta" : "www.petpooja_clone.instagram.com",
                    "fb" : "www.petpooja_clone.facebook.com",
                    "linkedin" : "www.petpooja_clone.linkedin.com"
                }
            }

            # test

            # I am in dev branch

            # I am in main branch
            
            return jsonify(feel_free_to_contact_us = contact_us_dict)

        @app.route("/about_us", methods=["GET"])
        def about_us():
            about_us_string = "Starting out in 2011, Petpooja_Clone was a food delivery platform for Corporates. Think Zomato or Swiggy, but for bulk corporate orders. With this business model, we achieved a respectable mark in 2 years: serving over 200 corporates by partnering with 300+ restaurants."
            return about_us_string

        db.create_all()
        db.session.commit()
        return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)