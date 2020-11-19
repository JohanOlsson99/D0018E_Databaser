from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flask_login import UserMixin



class RegistrationForm(FlaskForm):
    username = StringField('Användarnamn',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Lösenord', validators=[DataRequired()])

    submit = SubmitField('Registrera dig')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Lösenord', validators=[DataRequired()])
    remember = BooleanField('Kom ihåg mig')
    submit = SubmitField('Logga in')


class PaymentForm(FlaskForm):
    name = StringField('Fullständigt namn*', validators=[DataRequired()])

    cardnumber = StringField('Kort', validators=[DataRequired()])

    adress = StringField('Adress', validators=[DataRequired()])

    Postnummer = StringField('Postnummer*', validators=[DataRequired()])

    Stad = StringField('Stad', validators=[DataRequired()])

    Land = StringField('Land', validators=[DataRequired()])

    submit = SubmitField('Skicka bestälning')


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