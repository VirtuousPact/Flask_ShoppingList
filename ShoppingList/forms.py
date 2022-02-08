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

class ItemForm(FlaskForm):
    name = StringField(
        'Name',
        [DataRequired(message="Your item must have a name")]
    )
    store_name = StringField(
        'Store Name'
    )
    quantity = IntegerField(
        'Quantity',
        [
            DataRequired(),
            NumberRange(min=1,
            message=('Your quantity should be at least 1.'))
        ]
    )
    submit = SubmitField('Add Item')