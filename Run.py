#from forms import RegistrationForm, LoginForm, PaymentForm, AddToCart, cartForm, User, cartIndividualForm

import os

from datetime import datetime

from Forms import *
from addToCartForm import checkIfAddedToCart, checkIfAddedToCartItem, getTestCart
import sys, random
from flask_login import login_user, logout_user, LoginManager, current_user
from flaskext.mysql import MySQL
from SendToDB import *
from flask import Flask, render_template, flash, request, url_for, redirect, make_response
#from PIL import Image

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'd986e15d678b0a18d2ea47ccfc47e1ad'

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'db990715'
app.config['UPLOAD_FOLDER'] = os.getcwd() + "/static/image"
mysql.init_app(app)


#file = Image.open(os.getcwd() + "/static/image/car.jpg")
#file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp.jpg'))

#con = mysql.connect()

#login_manager = LoginManager()
#login_manager.init_app(app)

USERNAMELOGIN = 0
EMAILLOGIN = 1
ISADMIN ='A'
ISCUSTOMER = 'C'
ORDERNOTSENT = 'pending'
ORDERRESERVED = 'reserved'
signedInUsers = {}
ALLOWED_EXTENSIONS = {'jpg'}


def getIsSignedInAndIsAdmin():
    try:
        if (request.cookies.get('ID')[-1] == str(ISADMIN)) and (signedInUsers.get(request.cookies.get('ID'), False)):
            signedIn = True
            isAdmin = True
        elif (request.cookies.get('ID')[-1] == str(ISCUSTOMER)) and (signedInUsers.get(request.cookies.get('ID'), False)):
            signedIn = True
            isAdmin = False
        else:
            signedIn = False
            isAdmin = False
    except:
        signedIn = False
        isAdmin = False
    return signedIn, isAdmin


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    #form, id, description, imageLink = getTest(30)  # get test data
    #checkIfAddedToCart(form, id)  # if the form was send and is correct

    #price = []

    # for i in range(len(form)):
    #    form[i].howManyToCart.id = 'counter-display-' + str(
    #        id[i])  # IMPORTANT!!!! The + and - buttons won't work if this isn't here
    #    price.append(random.randint(1,9999))
    con = mysql.connect()
    idList, nameList, priceList, descList, prodLeftList, imageLinkList = getProducts(con)
    form = []
    for i in range(len(idList)):
        form.append(AddToCart())
        form[i].howManyToCart.id = 'counter-display-' + str(
            idList[i])  # IMPORTANT!!!! The + and - buttons won't work if this isn't here
        form[i].defineMaxMin(max=int(prodLeftList[i]))

    correctRequest, id, howManyItems = checkIfAddedToCart(form, idList, getIsSignedInAndIsAdmin())
    if(correctRequest):  # if the form was send and is correct
        con = mysql.connect()
        user = signedInUsers.get(request.cookies.get('ID'))
        if(addItemToOrder(con, id, user.getId(), howManyItems)):
            flash('Successfully added ' + str(form[i].howManyToCart.data) + ' of your item to your cart', 'success')
            return redirect(url_for('home'))
        else:
            flash('Something went wrong', 'danger')

    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('home.html', title="home", form=form, id=idList, name=nameList, price=priceList,
                           description=descList, prodLeft=prodLeftList,
                           imageLink=imageLinkList, signedIn=signedIn, isAdmin=isAdmin)


@app.route("/cart", methods=['GET', 'POST'])
def cart():
    customer = signedInUsers.get(request.cookies.get('ID'), False)
    if customer is not False:
        customerId = customer.getId()
    else:
        flash('You need to sign in before checking your cart', 'danger')
        return redirect(url_for('home'))
    con = mysql.connect()
    #form, idList, descList, imageLinkList, itemsInCart, nameList, prodLeftList, priceList = getTestCart(3)
    #trueFalse, productId, descList, imageLinkList, itemsInCart, nameList, prodLeftList, priceList = getProductsInCart(con, customerId)
    trueFalse, productId, descList, imageLinkList, itemsInCart, nameList, prodLeftList, priceList = getProductsInCartNew(
        con, customerId)

    #form = cartForm(productId, itemsInCart, prodLeftList)
    totalCost = 0
    form = []
    if trueFalse:
        for i in range(len(productId)):
            form.append(cartIndividualForm())
            #form[i].howManyToCart.id = 'counter-display-' + str(productId[i])
            #form[i].addToCart.id = 'remove-button-' + str(productId[i])
            form[i].defineStartUpValues(productId[i], itemsInCart[i])
            #form[i].howManyToCart.data = itemsInCart[i]
            #print(itemsInCart[i])
            form[i].defineMaxMin(max=(int(prodLeftList[i]) + int(itemsInCart[i])))
            totalCost += (itemsInCart[i] * priceList[i])
    if not trueFalse:
        flash('You have nothing in your cart right now, you can add items from home', 'danger')

    if request.method == 'POST':
        if checkCartForm(form, productId, customerId, con):
            return redirect(url_for('cart'))
        elif request.form.get('payment') == 'payment':
            checkIfReservedSuccessfull = setReservedOrder(con, customerId)
            if checkIfReservedSuccessfull:
                flash('Successfully ordered your products', 'success')
                return redirect(url_for('cart'))
            else:
                flash('Couldn\'t order your products', 'danger')


    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('varukorg.html', title="Cart", form=form, id=productId, name=nameList, price=priceList,
                           description=descList, prodLeft=prodLeftList,
                           imageLink=imageLinkList, signedIn=signedIn, totalCost=totalCost, isAdmin=isAdmin, itemsInCart=itemsInCart)

def checkCartForm(form, productId, customerId, con):
    print('Check')
    for i in range(len(form)):
        if ((form[i].validate_on_submit()) and (form[i].addToCart.data == True)
                and (str(productId[i]) in request.form)):
            print('cartForm correct with data', form[i].howManyToCart.data, 'and ID', productId[i])
            if updateOrder(con, form[i].howManyToCart.data, int(productId[i]), int(customerId)):
                return True
            return False
    return False



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        con = mysql.connect()
        if adminUsernameAndPasswordCorrect(form, con):
            temp = getAdmin(form, con, USERNAMELOGIN)
            print("IS ADMIN", file=sys.stderr)
            return setCookieAndReturnAddress(temp, ISADMIN)
        elif adminEmailAndPasswordCorrect(form, con):
            temp = getAdmin(form, con, EMAILLOGIN)
            print("IS ADMIN", file=sys.stderr)
            return setCookieAndReturnAddress(temp, ISADMIN)
        elif customerUsernameAndPasswordCorrect(form, con):
            temp = getUser(form, con, USERNAMELOGIN)
            print("IS CUSTOMER", file=sys.stderr)
            return setCookieAndReturnAddress(temp, ISCUSTOMER)
        elif customerEmailAndPasswordCorrect(form, con):
            temp = getUser(form, con, EMAILLOGIN)
            print("IS CUSTOMER", file=sys.stderr)
            return setCookieAndReturnAddress(temp, ISCUSTOMER)
        else:
            flash('Wrong sign in credits', 'danger')

    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('login.html', title="login", form=form, signedIn=signedIn, isAdmin=isAdmin)

def setCookieAndReturnAddress(temp, adminOrCustomer):
    value = str(str(temp.getId()) + str(adminOrCustomer))
    signedInUsers[value] = temp
    res = make_response(redirect(url_for('home')))
    res.set_cookie('ID', value=value, max_age=60 * 60 * 24)
    flash('logged in', 'success')
    return res


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.phone.data is not None:
            if int(form.phone.data) > 2147483648:
                flash(f'Wrong phonenumber type', 'danger')

        con = mysql.connect()
        if not customerAlreadyInDB(form, con):
            if addCustomerInDB(form, con):
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('login'))
            else:
                flash(f'Something went wrong with your registration', 'danger')
        else:
            flash(f'User already exists', 'danger')

    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('register.html', title='Register', form=form, signedIn=signedIn, isAdmin=isAdmin)


@app.route("/betalning", methods=['GET', 'POST'])
def betalning():
    form = PaymentForm()
    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('betalning.html', title='betalning', form=form, signedIn=signedIn, isAdmin=isAdmin)


@app.route("/com")
def comment():
    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('commentSection.html', title='comment', signedIn=signedIn, isAdmin=isAdmin)


@app.route('/item-<int:id>', methods=['GET', 'POST'])
def item(id):
    con = mysql.connect()
    bool, data = getProductFromId(con, id)
    if bool:
        id = data[0]
        name = data[1]
        price = data[2]
        desc = data[3]
        prodLeft = data[4]
        rating = data[5]
        howManyRated = data[6]
        imageLink = url_for('static', filename=('image/' + str(id) + '.jpg'))
    else:
        return redirect(url_for('error.html'))

    form = AddToCart()

    #form.defineHowManyToCartId(id)
    form.defineMaxMin(max=int(prodLeft))
    form.howManyToCart.id = 'counter-display-' + str(id)  # IMPORTANT!!!! The + and - buttons won't work if this isn't here
    #checkIfAddedToCartItem(form, id)  # if the form was send and is correct

    #form.howManyToCart.id = 'counter-display-' + str(id)  # IMPORTANT!!!! The + and - buttons won't work if this isn't here
    #price = []
    #price.append(random.randint(1, 9999))

    correctRequest, howManyItems = checkIfAddedToCartItem(form, id, getIsSignedInAndIsAdmin())
    if (correctRequest):  # if the form was send and is correct
        con = mysql.connect()
        user = signedInUsers.get(request.cookies.get('ID'))
        if (addItemToOrder(con, id, user.getId(), howManyItems)):
            flash('Successfully added ' + str(form.howManyToCart.data) + ' of your item to your cart', 'success')
            return redirect(url_for('item', id=id))
        else:
            flash('Something went wrong', 'danger')



    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('item.html', title='item', form=form, id=id, name=name, price=price,
                           description=desc, prodLeft=prodLeft,
                           imageLink=imageLink, signedIn=signedIn, isAdmin=isAdmin)



@app.route('/logout')
def logout():
    try:
        if signedInUsers.get(request.cookies.get('ID'), False):
            id = request.cookies.get('ID')
            signedInUsers.pop(id)
            res = make_response(redirect(url_for('home')))
            res.set_cookie('ID', id, max_age=0)
            flash(f'logged out', 'success')
            return res
    except:
        pass
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    user = signedInUsers.get(request.cookies.get('ID'), False)
    if user is  False:
        flash('Not Logged in!', 'danger')
        return redirect(url_for('home'))
    firstName = str(user.getFirstname())
    surName = str(user.getLastname())
    username = str(user.getUsername())
    email = str(user.getEmail())

    if user.getPhone() is None:
        phone = ''
    else:
        phone = str(user.getPhone())
    birthday = user.getBirthday()
    try:
        birthdayDay = str(birthday.day)
        birthdayMonth = str(birthday.month)
        birthdayYear = str(birthday.year)
    except:
        birthdayDay = '-'
        birthdayMonth = '-'
        birthdayYear = '-'
    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('profile.html', title='profile', form=form, firstName=firstName, surName=surName, 
                            username=username, email=email, phone=phone, birthdayDay=birthdayDay, birthdayMonth=birthdayMonth, 
                            birthdayYear=birthdayYear, signedIn=signedIn, isAdmin=isAdmin)

@app.route('/admin', methods=['GET', 'POST'])
def adminPage():
    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    if isAdmin:
        form = addProductsForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                if 'file' not in request.files:
                    flash('No selected file', 'danger')
                    return render_template('adminPage.html', title='admin', form=form, signedIn=signedIn, isAdmin=isAdmin)
                file = request.files['file']
                if file.filename == '':
                    flash('No selected file', 'danger')
                    return render_template('adminPage.html', title='admin', form=form, signedIn=signedIn, isAdmin=isAdmin)
                con = mysql.connect()
                if len(form.productDescription.data) > 255:
                    flash('To long description', 'danger')
                    return render_template('adminPage.html', title='admin', form=form, signedIn=signedIn, isAdmin=isAdmin)
                id = addNewProductAndGetNewId(con, form)
                if file and allowed_file(file.filename):
                    filename = str(id) + ".jpg"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('successfully added your item', 'success')
                    return redirect(url_for('home'))
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp.jpg'))
            #if img.lower().endswith('.jpg'):
            #    print('True')
            #print(request.files['file'])

        return render_template('adminPage.html', title='admin', form=form, signedIn=signedIn, isAdmin=isAdmin)
    else:
        flash('You are not an admin, therefore you do not have access to admin page', 'danger')
        return redirect(url_for('home'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
