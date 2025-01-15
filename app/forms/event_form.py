# app/forms/event_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    date = DateTimeField('Event Date', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
