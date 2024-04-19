from . import db # import db from __init__.py file
from flask_login import UserMixin #import flask_login for managing different User Access 
from decimal import Decimal
# Each Class defines a table 

# User class inheriting from db.Model and UserMixin 
class User(db.Model,UserMixin):
    # columns for the User table
    id=db.Column("id",db.Integer,primary_key=True)
    email = db.Column("email",db.String(150),unique=True)
    password = db.Column("password",db.String(150))
    firstName = db.Column("firstname",db.String(30))
    lastName=db.Column("lastname",db.String(30))
    phonenumber=db.Column("phonenumber",db.String(15),unique=False)
    role=db.Column("role",db.String(10))

class Item(db.Model):
    # columns for the Item table
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250),unique=True)
    img = db.Column(db.Text,nullable=False)
    price = db.Column(db.Numeric(10, 2),nullable=False)
    cost = db.Column(db.Numeric(10, 2),nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    # Define relationship with Orderitem table
    orderitem = db.relationship("Orderitem",backref="item")

class Order(db.Model):
    # columns for the Order table
    id=db.Column(db.Integer,primary_key=True)
    order_no = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.String)
    notes = db.Column(db.String,nullable=True)
    payment_method = db.Column(db.String(20), nullable=False)
    discount = db.Column(db.Numeric(10, 2),nullable=False)
    total = db.Column(db.Numeric(10, 2),nullable=False)
    status = db.Column(db.String,nullable=False,default="incomplete")
    # Defines relationship with Orderitem table
    orderitem = db.relationship("Orderitem",backref="order")

class Orderitem(db.Model):
    # columns for the Orderitem table
    id=db.Column(db.Integer,primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey("item.id"))
    item_qty =db.Column(db.Integer)
    order_id = db.Column(db.Integer,db.ForeignKey("order.id"))