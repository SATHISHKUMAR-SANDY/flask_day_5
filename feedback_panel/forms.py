from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class FeedbackForm(FlaskForm):
    user_name = StringField("Name", validators=[DataRequired(), Length(min=2)])
    rating = IntegerField("Rating (1 to 5)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField("Comment", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Submit")
