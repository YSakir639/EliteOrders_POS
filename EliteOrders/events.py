# Import the SocketIO class from the flask_socketio module
from flask_socketio import SocketIO
# import models (databases) from .models
from .models import Item,Orderitem,Order,User
# import db from __init__.py
from flask import flash,redirect,url_for
from . import db
# from engineio import async_threading
import datetime
from sqlalchemy import and_


# Create a SocketIO instance
socketio = SocketIO()

# Function to generate a new order number based on the current date
def generate_order_number():
    # Get the current date
    today = datetime.date.today()
    # Count the number of orders for the current date
    order_count_today = Order.query.filter_by(date=today).count()
    # Generate the order number by incrementing the count by 1
    order_number = order_count_today + 1
    return order_number


# Define a SocketIO event handler for 'delete-item'
@socketio.on('delete-item')
def delete_item(id):
    # Retrieve the Item with the specified ID from Item 
    item = Item.query.get_or_404(int(id["id"]))
    # Mark the item as deleted
    item.is_deleted = True
    # commit to the database
    db.session.commit()
  
# Event handler for receiving 'order' events from the client via Socket.IO
@socketio.on('order')
def get_order(data):
    # Extract data from the message received from the client
    notes = data[list(data.keys())[0]] 
    items = data[list(data.keys())[1]]
    discount = data[list(data.keys())[2]]
    total = data[list(data.keys())[3]]
    payment_method = data[list(data.keys())[4]]
    
    order_no = generate_order_number()

    # If there are items in the order, add them to the database
    if len(items)>0 :     
        # Create a new Order object with the extracted data to store it into "Order" table
        order = Order(order_no=order_no,date=datetime.datetime.now().date(),time=datetime.datetime.now().time().strftime("%H:%M:%S"),notes=notes,discount=discount,total=total,payment_method=payment_method)
        # Add the order to the database session and commit the transaction
        db.session.add(order)
        db.session.commit()
        for item in items:
            orderitem = Orderitem(item_id=item,item_qty=items[item][1],order=order)
            db.session.add(orderitem)
            db.session.commit()
        # Emit a message to notify the KDS system to reload
        socketio.emit("kds-data","reload")


    
   


# Define a function to handle order completion events
@socketio.on('order-complete')
def order_complete(data):
    # Extract order number from the received data
    order_no = data[list(data.keys())[0]]
    # Get today's date
    today = datetime.date.today()
    # Query the database to find the order with the given order number and current date
    order = Order.query.filter(and_(Order.order_no == order_no, Order.date == today)).first()
    # Update the status of the order to "Complete"
    order.status = "Complete"
    # Commit the changes to the database
    db.session.commit()


# Socket event handler for deleting a user
@socketio.on('delete-user')
def delete_user(id):
    # Extract the user ID from the received data
    user_id = int(id["id"])
    # Query the database for the user with the given ID
    user = User.query.get_or_404(user_id)
    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

