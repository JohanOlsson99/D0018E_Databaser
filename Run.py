from flask import Flask, render_template, flash, request, url_for, redirect
from forms import RegistrationForm, LoginForm, PaymentForm, AddToCart
from addToCartForm import checkIfAddedToCart, getTest

import sys

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'd986e15d678b0a18d2ea47ccfc47e1ad'


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form, id, description, imageLink = getTest(30)  # get test data
    checkIfAddedToCart(form, id)  # if the form was send and is correct

    for i in range(len(form)):
        form[i].howManyToCart.id = 'counter-display-' + str(
            id[i])  # IMPORTANT!!!! The + and - buttons won't work if this isn't here

    return render_template('home.html', title="home", form=form, id=id, description=description, imageLink=imageLink)


@app.route("/varukorg")
def kundkorg():
    return render_template('varukorg.html', title="varukorg")


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="login", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/betalning", methods=['GET', 'POST'])
def betalning():
    form = PaymentForm()
    return render_template('betalning.html', title='betalning', form=form)


@app.route("/com")
def commentSection():
    return render_template('commentSection.html', title='comment')


if __name__ == '__main__':
    app.run(debug=True)
