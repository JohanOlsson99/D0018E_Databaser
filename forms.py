from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_login import UserMixin



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember')
    submit = SubmitField('Login')


class PaymentForm(FlaskForm):
    name = StringField('Full Name*', validators=[DataRequired()])

    cardnumber = StringField('Card', validators=[DataRequired()])

    adress = StringField('Adress', validators=[DataRequired()])

    Postnummer = StringField('Postal Number*', validators=[DataRequired()])

    Stad = StringField('City', validators=[DataRequired()])

    Land = StringField('Country', validators=[DataRequired()])

    submit = SubmitField('Send Order')


class AddToCart(FlaskForm):
    howManyToCart = IntegerField('amount', validators=[NumberRange(min=1, max=100)])
    addToCart = SubmitField('Add to cart')


class cartForm(FlaskForm):
    howManyToCart = IntegerField('amount', validators=[NumberRange(min=1, max=100)])
    addToCart = SubmitField('Remove')


class User(UserMixin):
    id = 1
    username = "Johan"
    email = "Johan@gmail.com"
    password = '123'
    isAdmin = True

    def getIsAdmin(self):
        return self.isAdmin