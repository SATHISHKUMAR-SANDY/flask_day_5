from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

class UpdateStatusForm(FlaskForm):
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Canceled', 'Canceled')], validators=[DataRequired()])
    submit = SubmitField('Update Status')
