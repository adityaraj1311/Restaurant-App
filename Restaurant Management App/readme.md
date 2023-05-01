# note => first we need to add the restaurant 
in below format
{
    "name_list" : ["rest1", "rest2", "rest3", ...]
}

# then add items to the menu bcz (restaurantName table is parent and restaurantDetails is child)
/add_items_to_menu
{
    "list" : [
        {
        "restaurant_name" : "abc",
        "item_type" : "starters",
        "item_name" : "veg cutlet",
        "item_price" : "200"
        },
        {
            "restaurant_name" : "def",
            "item_type" : "drinks",
            "item_name" : "diet coke",
            "item_price" : "150" 
        },
        {
            "restaurant_name" : "ghi",
            "item_type" : "ice cream",
            "item_name" : "chocolate",
            "item_price" : "100"
        }
    ]
}

# to fill restaurantDetails => for each tuple we need to provide to provide {dictionaries} and to iterate all the dictionaries => put dictionaries in a list => and iterate over each item you get access to each item and then create a new object and put it all their details acc to that iteration in that object