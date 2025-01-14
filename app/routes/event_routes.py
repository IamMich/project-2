from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app import db  # Import db after app is initialized
from app.models import Event, Attendee
from app.forms.event_form import EventForm

bp = Blueprint('event_routes', __name__)

@bp.route('/')
def home():
    events = Event.query.all()
    return render_template('home.html', events=events)

@bp.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    attendees = Attendee.query.filter_by(event_id=event_id).all()
    return render_template('event_details.html', event=event, attendees=attendees)

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
        return redirect(url_for('event_routes.home'))
    return render_template('create_event.html', form=form)
