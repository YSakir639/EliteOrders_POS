# import create_app function from the Eliteorders folder
from EliteOrders import create_app
# from event.py import socketio instance
from EliteOrders.events import socketio
# assign a variable to store create_app
# Import the SocketIO class from the flask_socketio module
from flask_socketio import SocketIO
from engineio.async_drivers import threading
app = create_app()

# Initialize the SocketIO instance with the Flask application

socketio.init_app(app,async_mode="threading")

# check weather the app is running from the main file 
if __name__=="__main__":
   socketio.run(app,host="127.0.0.1",port=80,debug=True)
   # app.run(host="0.0.0.0",port=80)
    


    