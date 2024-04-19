from flask import Blueprint,request,render_template,redirect,url_for,flash
from . import db
from .models import User

#modules to hash the passwords
from werkzeug.security import generate_password_hash,check_password_hash 

# Import specific functions and objects from the flask_login module
from flask_login import login_user,login_required,current_user,logout_user

# Create a new Blueprint named auth
auth = Blueprint("auth",__name__)

# Define a route for creating user accounts
@auth.route("/Accounts",methods=["GET","POST"])
# Ensure that the user is logged in 
@login_required
def accounts():
# Owner-> SuperSecurePassword
    # Check if the user is not an owner
    if current_user.role != "Owner":
        # Redirect the user to the login page
        return redirect(url_for("auth.login"))
    # Check if the request method is POST
    if request.method == 'POST':  
        # Retrieve form data
        email=request.form.get("email")
        password=request.form.get("password")
        # Hash the password
        hashed_password = generate_password_hash(password)
        confirmpassword=request.form.get("confirmpassword")
        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        phonenumber=request.form.get("phonenumber")
        role=request.form.get("role")

        # Check if the password length is less than 8 characters
        if len(password)<8:
            # Flash a message if the password is too short
            flash("Sorry, the password should be at least 8 characters long. Please choose a longer password.")
            # Redirect to the accounts route
            return redirect(url_for("auth.accounts"))
        # Check if an account with the provided email already exists
        elif User.query.filter_by(email=email).first():
            # Flash a message if an account with the email already exists
            flash("Sorry, an account with that email address already exists. Please log in or use a different email address to register.")
            return redirect(url_for("auth.accounts"))
        # Check if password matches the confirm password
        elif password==confirmpassword:
            # Create a new user with the data
            new_user = User(email=email,password=hashed_password,firstName=fname,lastName=lname,phonenumber=phonenumber,role=role)
            # Add the new user to the database

            db.session.add(new_user)
            db.session.commit()

        else:
            flash("Sorry, the password and confirm password fields do not match. Please ensure they are identical before proceeding.")        

            
    # Retrieve users with a role other than "Owner"
    users = User.query.filter(User.role!="Owner").all()
    # Render the "accounts.html" template
    return render_template("accounts.html",users=users)


# Route for handling login requests
@auth.route("/login",methods=["GET","POST"])
def login():
     # Check if the request method is POST 
    if request.method == 'POST':    
        # Retrieve email and password from the form
        email=request.form.get("email")
        password= request.form.get("password")
        
        # Query the database for a user with the provided email
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Sorry, we couldn't find an account with that email. Please double-check your email")
            return redirect(url_for("auth.login"))
        
         # Check if a user with the provided email exists and the password matches
        if user and check_password_hash(user.password,password):
            # log in the user
            login_user(user,remember=False)
             # Redirect the user based on their role
            if user.role == "Owner":
                return redirect(url_for("views.analytics"))
            if user.role=="Chef":
                return redirect(url_for("views.kds"))
            elif user.role=="Counter Staff":
                return redirect(url_for("views.counter"))
        else:
            flash("Sorry, your password was incorrect. Please double-check your password.")
            
    # Render the login page template
    return render_template("login.html")

# Define a route for the "/logout" 
@auth.route("/logout")  
# Ensure that the user is logged in before proceeding with the logout operation
@login_required
def logout():
    # Log out the current user
    logout_user()
    # Redirect the user to the login page after logout
    return redirect(url_for("auth.login"))


