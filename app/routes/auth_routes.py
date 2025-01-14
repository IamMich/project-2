from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models import User
from app.forms.auth_form import LoginForm, RegisterForm  # Assuming you have forms defined

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Login Route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Add password hashing in production
            login_user(user)
            return redirect(url_for('event_routes.home'))
    return render_template('login.html', form=form)

# Register Route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('event_routes.home'))
    return render_template('register.html', form=form)

# Logout Route
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('event_routes.home'))
