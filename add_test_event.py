from app import create_app, db
from app.models import Event

app = create_app()

with app.app_context():
    from datetime import datetime

    event_date = datetime.strptime('2025-01-22', '%Y-%m-%d').date()
    new_event = Event(name='Test Event', description='This is a test event.', date=event_date, venue_id=1, creator_id=1)  # Default creator_id
    db.session.add(new_event)
    db.session.commit()
    print("Test event created successfully.")
