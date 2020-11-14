from flask import flash, request, url_for
from forms import AddToCart, cartForm
import sys
import random


def checkIfAddedToCart(form, id):
    for i in range(len(form)):
        if id[i] in request.form:
            print(id[i], file=sys.stderr)
        if ((form[i].validate_on_submit()) and (form[i].addToCart.data == True) and (form[i].howManyToCart.data != 0)
                and (id[i] in request.form)):
            print(form[i].howManyToCart.id, file=sys.stderr)
            flash('Successfully added ' + str(form[i].howManyToCart.data) + ' of your items to your cart with ID ' +
                  str(id[i]), 'success')

        elif (form[i].is_submitted() and (not form[i].validate_on_submit()) and (id[i] in request.form)):
            flash('Couldn\'t add your items to your cart. Did you know you can only add 1 to 100 items not more '
                  'or less with ID ' + str(id[i]), 'danger')


def getTest(length):
    url = url_for('static', filename='image/car.jpg')
    string = "etworkeffects platforms proactive exploit, aggregate partnerships synergies " \
             "embedded optimize unleash synergize markets. Networks mindshare robust"
    form = []
    id = []
    description = []
    imageLink = []
    for i in range(length):
        form.append(AddToCart())
        id.append(str(i + 1))
        description.append(string)
        imageLink.append(url)
    return form, id, description, imageLink


def getTestCart(length):
    url = url_for('static', filename='image/car.jpg')
    string = "etworkeffects platforms proactive exploit, aggregate partnerships synergies " \
             "embedded optimize unleash synergize markets. Networks mindshare robust"
    form = []
    id = []
    description = []
    imageLink = []
    startValue = []

    for i in range(length):
        form.append(cartForm())
        id.append(str(i + 1))
        description.append(string)
        imageLink.append(url)
        startValue.append(random.randint(0, 100))

    return form, id, description, imageLink, startValue
