# app/routes/event_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Event, Attendee
from app.forms.event_form import EventForm

bp = Blueprint('event_routes', __name__)

# Home Page (List of Events)
@bp.route('/')
def home():
    events = Event.query.all()
    return render_template('home.html', events=events)

# Event Details Page
@bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    attendees = Attendee.query.filter_by(event_id=event_id).all()

    if request.method == 'POST' and current_user.is_authenticated:
        # Register user as attendee
        attendee = Attendee(user_id=current_user.id, event_id=event.id)
        db.session.add(attendee)
        db.session.commit()
        flash('You have registered for the event!', 'success')
        return redirect(url_for('event_routes.event_details', event_id=event.id))

    return render_template('event_details.html', event=event, attendees=attendees)

# Create Event Route
@bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('event_routes.home'))
    return render_template('create_event.html', form=form)
