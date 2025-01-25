import csv
from io import StringIO
from flask import Blueprint, make_response, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Event, Attendee, Venue  # Import the Venue model
from app.forms.event_form import EventForm
from app.forms.venue_form import VenueForm  # Importing VenueForm
from datetime import datetime

bp = Blueprint('event_routes', __name__)

# Venue Management Routes

# Create Venue Route
@bp.route('/create-venue', methods=['GET', 'POST'])
@login_required
def create_venue():
    form = VenueForm()  # Assuming a VenueForm exists
    if form.validate_on_submit():
        new_venue = Venue(
            name=form.name.data,
            location=form.location.data,
            capacity=form.capacity.data
        )
        db.session.add(new_venue)
        db.session.commit()
        flash('Venue created successfully!', 'success')
        return redirect(url_for('event_routes.home'))
    return render_template('create_venue.html', form=form)

# View Venues Route
@bp.route('/venues', methods=['GET'])
def view_venues():
    venues = Venue.query.all()  # Fetch all venues from the database
    return render_template('view_venues.html', venues=venues)

# View Events Route
@bp.route('/events', methods=['GET'])
def view_events():
    events = Event.query.all()  # Fetch all events from the database
    return render_template('view_events.html', events=events)  # Render the view_events template

# Home Page (List of Events)
@bp.route('/')
def home():
    events = Event.query.all()  # Fetch all events from the database
    return render_template('home.html', events=events)

# Dashboard Route
@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    events = Event.query.filter_by(creator_id=current_user.id).all()  # Fetch events created by the current user
    return render_template('dashboard_updated.html', events=events)  # Render the updated dashboard template with events

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
    form = EventForm()  # Assuming an EventForm exists
    if form.validate_on_submit():
        # Check for event date availability
        existing_event = Event.query.filter_by(date=form.date.data).first()
        if existing_event:
            flash('This date is already booked for another event. Please choose a different date.', 'danger')
            return render_template('create_event.html', form=form)

        # Check for venue availability
        venue_id = form.venue_id.data  # Assuming the form has a venue_id field
        venue_events = Event.query.filter_by(venue_id=venue_id, date=form.date.data).first()
        if venue_events:
            flash('The selected venue is not available on this date. Please choose a different venue or date.', 'danger')
            return render_template('create_event.html', form=form)

        new_event = Event(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data,
            venue_id=venue_id
        )
    if form.validate_on_submit():
        new_event = Event(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data
        )
        db.session.add(new_event)
        try:
            db.session.commit()
            flash('Event created successfully!', 'success')  # Success message
            return redirect(url_for('event_routes.home'))  # Redirect to home after creation
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while creating the event. Please try again.", "danger")
    
    return render_template('create_event.html', form=form)

@bp.route('/confirm-event', methods=['POST'])
@login_required
def confirm_event():
    # Fetch event details from the form
    event_data = request.form.to_dict()
    event_name = event_data.get('name')
    event_description = event_data.get('description')
    event_date = event_data.get('date')

    # Convert the date string to a Python date object (handle date conversion)
    try:
        event_date_obj = datetime.strptime(event_date, '%Y-%m-%d').date()
    except ValueError:
        flash("Invalid date format. Please select a valid date.", "danger")
        return redirect(url_for('event_routes.create_event'))

    # Pass event data to the confirmation page
    return render_template('confirm_event.html', event_details={
        'name': event_name,
        'description': event_description,
        'date': event_date_obj
    })

@bp.route('/submit-event', methods=['POST'])
@login_required
def submit_event():
    event_data = request.form.to_dict()

    # Convert the date string to a Python date object
    event_name = event_data['name']
    event_description = event_data['description']
    event_date_str = event_data['date']
    try:
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
    except ValueError:
        flash("Invalid date format. Please select a valid date.", "danger")
        return redirect(url_for('event_routes.create_event'))

    # Create the event and add it to the database
    new_event = Event(
        name=event_name,
        description=event_description,
        date=event_date
    )
    db.session.add(new_event)
    try:
        db.session.commit()
        flash('Your event has been submitted for our internal review. We will get back to you once we approve the event.', 'success')
        return redirect(url_for('event_routes.home'))  # Redirect to home after submission
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while submitting your event. Please try again.", "danger")
        return redirect(url_for('event_routes.create_event'))

# Export events as CSV
@bp.route('/export-events', methods=['GET'])
def export_events():
    events = Event.query.all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Event Name', 'Description', 'Date'])
    for event in events:
        cw.writerow([event.name, event.description, event.date])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=events.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# Import events from CSV
@bp.route('/import-events', methods=['POST'])
def import_events():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] != 'Event Name':  # Skip header row
                event = Event(
                    name=row[0],
                    description=row[1],
                    date=datetime.strptime(row[2], '%Y-%m-%d').date()  # Ensure date is correctly formatted
                )
                db.session.add(event)
        db.session.commit()
        flash('Events imported successfully!', 'success')
        return redirect(url_for('event_routes.home'))
    else:
        flash('Invalid file format. Please upload a CSV file.', 'danger')
        return redirect(url_for('event_routes.home'))

# Import Events Route
@bp.route('/import-event', methods=['POST'])
@login_required
def import_event():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0] != 'Event Name':  # Skip header row
                event = Event(
                    name=row[0],
                    description=row[1],
                    date=datetime.strptime(row[2], '%Y-%m-%d').date()  # Ensure date is correctly formatted
                )
                db.session.add(event)
        db.session.commit()
        flash('Events imported successfully!', 'success')
        return redirect(url_for('event_routes.home'))
    else:
        flash('Invalid file format. Please upload a CSV file.', 'danger')
        return redirect(url_for('event_routes.home'))

# Search for events by name
@bp.route('/search', methods=['GET'])
def search_events():
    search_query = request.args.get('query', '')  # Get the search query from the URL
    events = Event.query.filter(Event.name.like(f'%{search_query}%')).all()  # Search events by name
    return render_template('search_results.html', events=events)  # Render results page with events
