# run.py
from app import create_app, db
from app.models import User, Event, Attendee

app = create_app()

def create_tables():
    with app.app_context():
        db.create_all()  # Ensure tables are created within the app context

if __name__ == "__main__":
    create_tables()  # Create tables before running the app
    app.run(debug=True)
