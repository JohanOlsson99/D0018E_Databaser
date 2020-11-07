from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange

class AddToCart(FlaskForm):
    howManyToCart = IntegerField('amount',
                                 validators=[NumberRange(min=1, max=100)])
    addToCart = SubmitField('Add to cart')

