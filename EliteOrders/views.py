from flask import Blueprint,render_template,redirect,url_for,request,send_from_directory,flash

# Import the secure_filename function from the werkzeug.utils module
from werkzeug.utils import secure_filename
# Import the RequestEntityTooLarge exception from the werkzeug.exceptions module
from werkzeug.exceptions import RequestEntityTooLarge
import os
from decimal import Decimal
# import models from .models
from .models import Item,Orderitem,Order
# import db from __init__.py
from . import db

import datetime

from sqlalchemy import and_,func,desc,asc

# Import specific functions and objects from the flask_login module
from flask_login import login_user,login_required,current_user


# Create a new Blueprint named views
# This Blueprint will be used to organize routes for web urls
views = Blueprint("views",__name__)

# Define a route for the root URL ("/") to redirect users to the login page
@views.route("/")
def index():
    return redirect(url_for("auth.login"))

# Define a route for "/Menu" with GET and POST methods
@views.route("/Menu",methods=["GET","POST"])
@login_required
def menu():
    # Check if the user is not a chef
    if current_user.role != "Chef":
        # Redirect the user to the login page
        return redirect(url_for("auth.login"))

    # Check if the request method is POST
    if request.method == 'POST':    
        try:
            # Check if form data is present in the request
            if request.form:
                # Extract form data
                item_name = request.form.get("item-name")  # Capitalize the first letter in the item name

                if len(item_name.split(" "))>1:
                    temp=""
                    for i in item_name.split(" "):
                        try:
                            temp = temp+i[0][0].upper()+i[1:]+" "
                        except IndexError:
                            pass
                    item_name = temp
                else:
                    item_name = item_name[0].upper() +" "+item_name[1:] 

              
                item_img = request.files['item_img']
                item_cost = request.form.get("item-cost")
                item_price = request.form.get("item-price")

                item = Item.query.filter(Item.name==item_name).first()
               
                if item:
                    if item.is_deleted==False:
                        flash("Error: Item name already exists. Please choose a different name.")
                        return redirect(url_for("views.menu"))
                    elif item.is_deleted==True:
                        db.session.delete(item)
                        db.session.commit()
                    
                
                if item_cost == item_price:
                    flash("Error: Item cost cannot be equal to the item price. Please adjust the values accordingly.")
                    return redirect(url_for("views.menu"))
                
                elif Decimal(item_cost)>Decimal(item_price):
                    flash("Error: Item price should be greater than the item cost. Please adjust the values accordingly.")
                    return redirect(url_for("views.menu"))
    
                # Check if all required form fields are not empty
                elif item_name and item_cost and item_price and item_img:
                    # Create a new Item object with the extracted form data
                    item = Item(name=item_name, img=secure_filename(item_img.filename), cost=item_cost, price=item_price)
                    # Add the new item to the database session
                    db.session.add(item)
                    # Commit the changes to the database
                    db.session.commit()
                else:
                    flash("Error: Please fill in all the required fields.")
                    return redirect(url_for("views.menu"))

                # Check if item_img is not empty
                if item_img:
                    # Save the uploaded image to the Media directory
                    # secure the filename to prevent errors 
                    item_img.save(os.path.join("EliteOrders/Media", secure_filename(item_img.filename)))
                    # Redirect to the "/Menu" route
                    return redirect("/Menu")
                else:
                    flash("Please select an image for the item.")
                    redirect(url_for("views.menu"))
         # Handle the exception if the request entity is too large (if the img file is too large)      
        except RequestEntityTooLarge :
            flash("Error: Image file size exceeds limit. Please upload a smaller file.")
    # Query the Item table to retrieve all items where is_deleted is False
    item = Item.query.filter(Item.is_deleted == False).order_by(asc(Item.name)).all()

    # Render the "menu.html" template and passing items to the templates (this will be rendered by jinja)
    return render_template("menu.html",items=item)


# Define a route to serve images with a specific filename
@login_required
@views.route("/serve-image/<filename>")
def serve_image(filename):    
    # Return the requested image from the Media directory
    return send_from_directory("C:\\ELiteOrders POS\\EliteOrders\\Media",filename)


# Define a route for the 'Counter' page
@views.route("/Counter")
@login_required
def counter():
    # Check if the user's role is not "Counter Staff"
    if current_user.role != "Counter Staff":
        # Redirect the user to the login page
        return redirect(url_for("auth.login"))
    # Query items that are not deleted from the database
    item = Item.query.filter(Item.is_deleted == False).order_by(asc(Item.name)).all()
    # Render the counter.html template with the queried items
    return render_template("counter.html", items=item)





# Route for the "/KDS" endpoint
@views.route("/KDS")
@login_required
def kds():
    # Check if the user is not a chef
    if current_user.role != "Chef":
        # Redirect the user to the login page
        return redirect(url_for("auth.login"))
    
    # Query incomplete orders for today's date
    orders = Order.query.filter(and_(Order.date == datetime.datetime.now().date(), Order.status == "incomplete")).all()
    # Initialize an empty list to store items for each order
    items = []
    # Loop through each order
    for order in orders:

        item_names = item_names = Item.query.with_entities(Item.name).join(Orderitem).join(Order).filter(and_(Orderitem.order_id == order.id, Order.status == "incomplete")).all()
        

        item_qty = Orderitem.query.with_entities(Orderitem.item_qty).join(Order).filter(and_(Orderitem.order_id == order.id, Order.status == "incomplete")).all()
        
        # Extract item names and quantities from the query results
        names = [item_name for item_name, in item_names]
        qty = [qty for qty, in item_qty]

        # Create a list of lists for items with names and quantities
        item = [list(row) for row in zip(names, qty)]
        items.append(item)

    # Combine orders and items into a single iterable using the zip function
        # this will help to iterate through orders and items[item names, item qtys] simultaneously
    data = zip(orders, items)

    # Render the template "kds.html" with the combined data
    return render_template("kds.html", data=data)

# Define a route for the "/Invoice" page
@views.route("/Invoice") 
@login_required
def invoice():
    # Check if the user is not an owner
    if current_user.role != "Owner":
        # Redirect the user to the login page
        return redirect(url_for("auth.login"))

     # Retrieve all orders from the database
    # orders = Order.query.all()
    orders = Order.query.order_by(desc(Order.date)).order_by(desc(Order.order_no)).all() 
 
    orderitems=[] # List to store order items
    items=[] # List to store items

    # Loop through each order
    for order in orders:
         # query order items associated with the current order
        orderitems_model = Orderitem.query.join(Order).filter(Orderitem.order_id==order.id).all()
        orderitems.append(orderitems_model) # Add order items to the list
         # query items associated with the current order
        items_model = Item.query.join(Orderitem).filter(Orderitem.order_id == order.id).all()
        items.append(items_model) # Add items to the list
    # Combine orders, order items, and items into a single iterable (this will help to iterate through all the lists simultaneously)
    data = zip(orders,orderitems,items)
    # Render the template "invoice.html" with the data
    return render_template("invoice.html",data=data)

# Define a route for the "/Analytics" page
@views.route("/Analytics")  
@login_required
def analytics():
    # Check if the user is not an owner
    if current_user.role != "Owner":
        # Redirect the user to the login page
        return redirect(url_for("auth.login"))    
    # Query all items 
    items = Item.query.filter(Item.is_deleted==False).all()
    # Get all the names of the Items
    item_names = [item.name for item in items]

    # Calculate total sales for each item
    item_sales = []
    for item in items:
        sales = sum(orderitem.item_qty for orderitem in item.orderitem)
        item_sales.append(sales)
    
    # Retrieve dates of all thye orders from the databse
    dates = Order.query.with_entities(Order.date).distinct().all()
    dates_list = [str(date[0]) for date in dates]

    # Calculate the number of customers per day
    # store each of them in a list
    customers = [Order.query.filter(Order.date == date[0]).count() for date in dates]

    # # Count total number of items
    # total_items = Item.query.filter(Item.is_deleted!=True).count()

    # Count number of sales for today
    today = datetime.datetime.now().date()
    number_of_sales = Order.query.filter(Order.date==today).count()

    # Calculate the total cash payments received today
    total_cash_payments_today = db.session.query(db.func.sum(Order.total)) \
    .filter(db.and_(
        Order.payment_method == 'cash',
        db.func.date(Order.date) == today
    )).scalar() or 0

    # print(total_cash_payments_today)
    
    # Calculate the total card payments received today
    total_card_payments_today = db.session.query(db.func.sum(Order.total)) \
    .filter(db.and_(
        Order.payment_method == 'card',
        db.func.date(Order.date) == today
    )).scalar() or 0

    # Calculate total discount amount
    total_discount_amount = db.session.query(func.sum(Order.total * (Order.discount / 100))).scalar()

    # Query to retrieve the 'total' amount of all orders placed today
    todays_orders= Order.query.with_entities(Order.total).filter(Order.date ==today).all()
    # Calculate the gross revenue from today's orders
    gross = sum(order.total for order in todays_orders)

    # Calculate the total cost of all items sold today
    total_cost_today = db.session.query(
    db.func.sum(Orderitem.item_qty * Item.cost)) \
    .select_from(Order) \
    .join(Orderitem, Order.id == Orderitem.order_id) \
    .join(Item, Orderitem.item_id == Item.id) \
    .filter(db.func.date(Order.date) == today).scalar() 

    net_profit_today = gross - total_cost_today


    # Create a list of figures
    # this will be passed to frontend
    # also formatting the amounts to 2dps
    figures =[number_of_sales,format(total_cash_payments_today,".2f"),format(total_card_payments_today,".2f"),format(total_discount_amount,".2f"),gross,net_profit_today]

    # Render the template "analytics.html" with all the necessary data 
    return render_template("analytics.html", item_names=item_names, item_sales=item_sales, dates=dates_list, customers=customers,figures=figures)



