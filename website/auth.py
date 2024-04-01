from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db #means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password X_X', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 4 chars.', category='error')
        elif len(fname) < 2:
            flash('First name must be greater than 1 chars.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash("Password must be atleast 7 chars.", category='error')
        else:
            #add user to the database
            new_user = User(email=email, first_name=fname, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)