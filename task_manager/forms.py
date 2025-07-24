from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Optional

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    due_date = DateTimeField('Due Date (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[Optional()])
    is_done = BooleanField('Done')
    submit = SubmitField('Save')
