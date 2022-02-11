from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class ListForm(FlaskForm):
    name = StringField(
        'Name',
        [
            DataRequired(message="Your list must have a name"),
        ]
    )
    submit = SubmitField('Add List')