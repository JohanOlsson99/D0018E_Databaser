from flask import flash, request, url_for
from forms import AddToCart, cartForm
import sys
import random




def checkIfAddedToCart(form, id, isSignedIn):
    for i in range(len(form)):
        id[i] = str(id[i])
        #if str(id[i]) in request.form:
            #print(id[i], file=sys.stderr)
        if ((form[i].validate_on_submit()) and (form[i].addToCart.data == True) and (form[i].howManyToCart.data != 0)
                and (id[i] in request.form)):
            #print(form[i].howManyToCart.id, file=sys.stderr)
            if (not isSignedIn[0]):
                flash('You need to login to add items to your cart', 'danger')
            elif (isSignedIn[1]):
                flash('You can\'t be admin when adding items to your cart', 'danger')
            else:
                #flash('Successfully added ' + str(form[i].howManyToCart.data) + ' of your item to your cart', 'success')
                return True, id[i], str(form[i].howManyToCart.data)

        elif (form[i].is_submitted() and (not form[i].validate_on_submit()) and (id[i] in request.form)):
            flash('There aren\'t that many items left', 'danger')
    return False, None, None


def checkIfAddedToCartItem(form, id):
    id = str(id)
    if id in request.form:
        print(id, file=sys.stderr)
    if ((form.validate_on_submit()) and (form.addToCart.data == True) and (form.howManyToCart.data != 0)
            and (id in request.form)):
        print(form.howManyToCart.id, file=sys.stderr)
        flash('Successfully added ' + str(form.howManyToCart.data) + ' of your items to your cart with ID ' +
              str(id), 'success')

    elif (form.is_submitted() and (not form.validate_on_submit()) and (id in request.form)):
        flash('There aren\'t that many items left', 'danger')

def getTest(length):
    url = url_for('static', filename='image/0.jpg')
    string = "etworkeffects platforms proactive exploit, aggregate partnerships synergies " \
             "embedded optimize unleash synergize markets. Networks mindshare robust"
    form = []
    id = []
    description = []
    imageLink = []
    prodLeftList = []
    nameList = []
    priceList = []
    for i in range(length):
        form.append(AddToCart())
        id.append(str(i + 1))
        description.append(string)
        imageLink.append(url)
        prodLeftList.append(random.randint(1,100))
        nameList.append('Mercedes')
        priceList.append(random.randint(0, 9999))
    return form, id, description, imageLink, prodLeftList, nameList, priceList


def getTestCart(length):
    url = url_for('static', filename='image/0.jpg')
    string = "etworkeffects platforms proactive exploit, aggregate partnerships synergies " \
             "embedded optimize unleash synergize markets. Networks mindshare robust"
    form = []
    id = []
    description = []
    imageLink = []
    itemsInCart = []
    nameList = []
    prodLeftList = []
    priceList = []

    for i in range(length):
        form.append(cartForm())
        id.append(str(i))
        description.append(string)
        imageLink.append(url)
        itemsInCart.append(random.randint(0, 100))
        nameList.append('Mercedes')
        prodLeftList.append(random.randint(0,100))
        priceList.append(random.randint(0, 999))

    return form, id, description, imageLink, itemsInCart, nameList, prodLeftList, priceList