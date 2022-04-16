from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.message_model import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#home index routing us to the main login page
@app.route('/')
def index():
    return render_template('index.html')

#registration route
@app.route('/register',methods=['POST'])
def register():
    email_data = {'email': request.form['email']}
    user_in_db = User.get_by_email(email_data)
    if user_in_db:
        flash("Email already in use, please enter another.", 'register')
        return redirect('/')
    if not User.validate_register(request.form): #checks that the user is valid, if not redirects back to index page
        return redirect('/')
    data ={ #otherwise we create a dictionary called "data"
        "first_name": request.form['first_name'], #key is "first_name", value is what comes into the form from "first_name", etc...
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']) #key is password, value is the hashed version of the password using Bcrypt
    }
    id = User.save(data) #the save function returns the id of the user, and so we use that to...
    session['user_id'] = id #store it into session
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form) #passing in form data and checking via the "get by email" method if the user exists in the DB

    if not user: #if they do not exist, flash message (treating "user" as a Boolean here)
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']): #de-hashes the pw in the database and checks it with the input, if they don't match, flash message
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id #otherwise, user logs in and ID is stored in session (if this step is not taken, if the user tries to access the /dashboard by typing in the url, they will be redirected back to the login page)
    return redirect('/dashboard') #and dashboard is accessed

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ #have to create an object that represents what is logged in session as the user id
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    messages = Message.get_user_messages(data)
    users = User.get_all()
    return render_template("dashboard.html", user=user,users=users,messages=messages) #then can pass in that information and pull the users information to display on the dashboard

@app.route('/logout')
def logout():
    session.clear() #clears out session upon logging out
    return redirect('/')

