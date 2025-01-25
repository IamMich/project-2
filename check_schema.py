from app import create_app, db
from sqlalchemy import text

app = create_app()

def check_event_table():
    with app.app_context():
        with db.engine.connect() as connection:
            result = connection.execute(text("PRAGMA table_info(event);"))
            for row in result:
                print(row)

if __name__ == "__main__":
    with app.app_context():
        check_event_table()
