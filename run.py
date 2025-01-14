# run.py
from app import create_app, db
from app.models.models import Event, Attendee, User

app = create_app()

def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()  # Create all tables within the app context

if __name__ == "__main__":
    print("App initialized")
    create_tables()  # Ensure tables are created before running the app
    app.run(debug=True)
