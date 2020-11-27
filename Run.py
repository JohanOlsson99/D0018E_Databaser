
from forms import RegistrationForm, LoginForm, PaymentForm, AddToCart, cartForm, User
from addToCartForm import *
import sys, random
from flask_login import login_user, logout_user, LoginManager, current_user
from flaskext.mysql import MySQL
from SendToDB import *
from flask import Flask, render_template, flash, request, url_for, redirect, make_response


app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'd986e15d678b0a18d2ea47ccfc47e1ad'

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'db990715'
mysql.init_app(app)


#con = mysql.connect()

#login_manager = LoginManager()
#login_manager.init_app(app)

USERNAMELOGIN = 0
EMAILLOGIN = 1
ISADMIN = 0
ISCUSTOMER = 1
signedInUsers = {}

#signedInUsers[0] = (User([0, 'johan', 'olsson', 'johols', 'a@gmail.com', '0000000000', '2020-01-01', True]))


def getIsSignedInAndIsAdmin():
    try:
        if (request.cookies.get('ID')[-1] == str(ISADMIN)) and (signedInUsers.get(request.cookies.get('ID')[0:-1])):
            signedIn = True
            isAdmin = True
        elif (request.cookies.get('ID')[-1] == str(ISCUSTOMER)) and (signedInUsers.get(request.cookies.get('ID')[0:-1])):
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
    checkIfAddedToCart(form, idList)  # if the form was send and is correct

    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('home.html', title="home", form=form, id=idList, name=nameList, price=priceList,
                           description=descList, prodLeft=prodLeftList,
                           imageLink=imageLinkList, signedIn=signedIn, isAdmin=isAdmin)


@app.route("/varukorg", methods=['GET', 'POST'])
def kundkorg():
    """form = [cartForm(), cartForm()]
    id = ['1', '2']
    form[0].howManyToCart.id = 'counter-display-' + str(id[0])
    form[1].howManyToCart.id = 'counter-display-' + str(id[1])
    description = ["etworkeffects platforms proactive exploit, aggregate partnerships synergies embedded optimize unleash synergize markets. Networks mindshare robust", "Test"]
    imageLink = [url_for('static', filename='image/car.jpg'), url_for('static', filename='image/car.jpg')]
    form[0].addToCart.id = 'remove-button-' + str(id[0])
    form[1].addToCart.id = 'remove-button-' + str(id[1])"""

    form, idList, descList, imageLinkList, itemsInCart, nameList, prodLeftList, priceList = getTestCart(3)


    for i in range(len(form)):
        form[i].howManyToCart.id = 'counter-display-' + str(idList[i])
        form[i].addToCart.id = 'remove-button-' + str(idList[i])
        form[i].howManyToCart.data = itemsInCart[i]

    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('varukorg.html', title="varukorg", form=form, id=idList, name=nameList, price=priceList,
                           description=descList, prodLeft=prodLeftList,
                           imageLink=imageLinkList, signedIn=signedIn, isAdmin=isAdmin)


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
    signedInUsers[str(temp.getId())] = temp
    res = make_response(redirect(url_for('home')))

    res.set_cookie('ID', value=str(str(temp.getId()) + str(adminOrCustomer)), max_age=60 * 60 * 24)
    flash('logged in', 'success')
    return res


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.phone.data is not None:
            if int(form.phone.data ) > 2147483648:
                flash(f'Wrong phonenumber type', 'danger')
        else:
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
    form, idList, descList, imageLinkList, prodLeftList, nameList, priceList  = getTest(1)  # get test data
    id = [id]
    checkIfAddedToCartItem(form[0], id[0])  # if the form was send and is correct

    form[0].howManyToCart.id = 'counter-display-' + str(
        id[0])  # IMPORTANT!!!! The + and - buttons won't work if this isn't here
    price = []
    price.append(random.randint(1, 9999))

    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('item.html', title='item', form=form, id=idList, name=nameList, price=priceList,
                           description=descList, prodLeft=prodLeftList,
                           imageLink=imageLinkList, signedIn=signedIn, isAdmin=isAdmin)



@app.route('/logout')
def logout():
    try:
        if signedInUsers.get(request.cookies.get('ID')[0:-1]):
            id = request.cookies.get('ID')
            signedInUsers.pop(id[0:-1])
            res = make_response(redirect(url_for('home')))
            res.set_cookie('ID', id, max_age=0)
            flash(f'logged out', 'success')
            return res
    except:
        pass
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    signedIn, isAdmin = getIsSignedInAndIsAdmin()
    return render_template('profile.html', title='profile', signedIn=signedIn, isAdmin=isAdmin)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
