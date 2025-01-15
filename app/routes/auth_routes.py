# app/routes/auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.forms.auth_form import LoginForm, RegisterForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

# User loader for flask-login
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login Route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login Successful', 'success')
            return redirect(url_for('event_routes.home'))
        else:
            flash('Login Unsuccessful. Check username and password.', 'danger')
    return render_template('login.html', form=form)

# Register Route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('auth.register'))

        # Create the new user
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)  # Log the user in
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('event_routes.home'))
    return render_template('register.html', form=form)

# Logout Route
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out successfully', 'info')
    return redirect(url_for('event_routes.home'))
