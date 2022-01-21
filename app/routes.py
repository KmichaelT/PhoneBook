from app import phonebook, db
from flask import render_template, redirect, url_for,flash
from flask_login import login_user, logout_user, login_required
from app.forms import RegisterForm, LoginForm, ContactForm
from app.models import Contacts, User

@phonebook.route('/')
def index():
    contacts=Contacts.query.all()
    return render_template('index.html' , people=contacts)

@phonebook.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get the data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if either the username or email is already in db
        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
        # if it is, return back to register
        if user_exists:
            return redirect(url_for('register'))
        # Create a new user instance using form data
        User(username=username,email=email, password=password)

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@phonebook.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        # Grab the data from the form
        username = form.username.data
        password = form.password.data
       
        # Query user table for user with username
        user = User.query.filter_by(username=username).first()
        
        # if the user does not exist or the user has an incorrect password
        if not user or not user.check_password(password):
            # redirect to login page
            print('That username and password is incorrect')
            return redirect(url_for('login'))
        
        # if user does exist and correct password, log user in
        login_user(user)
        print('User has been logged in')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@phonebook.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@phonebook.route('/add_contact', methods=["GET","POST"])

def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Get the data from the form
        name = form.name.data
        address = form.address.data
        phone = form.phone.data
        
        contact=Contacts(name=name, address=address, phone=phone)
        contact.add()
        flash('new contact added!')

        return redirect(url_for('index'))

    return render_template('add_contact.html', form=form)