from flask import Flask, render_template, flash, request, url_for, redirect
from forms import RegistrationForm, LoginForm, PaymentForm, AddToCart, cartForm, User
from addToCartForm import checkIfAddedToCart, getTest, getTestCart, checkIfAddedToCartItem
import sys
import random
from flask_login import login_user, logout_user, LoginManager, current_user
from flaskext.mysql import MySQL


app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'd986e15d678b0a18d2ea47ccfc47e1ad'

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'db990715'
mysql.init_app(app)

con = mysql.connect()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User()




@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form, id, description, imageLink = getTest(30)  # get test data
    checkIfAddedToCart(form, id)  # if the form was send and is correct

    price = []

    for i in range(len(form)):
        form[i].howManyToCart.id = 'counter-display-' + str(
            id[i])  # IMPORTANT!!!! The + and - buttons won't work if this isn't here
        price.append(random.randint(1,9999))

    return render_template('home.html', title="home", form=form, id=id, description=description, imageLink=imageLink, price=price)


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

    form, id, description, imageLink, startValue = getTestCart(3)
    price = []

    for i in range(len(form)):
        form[i].howManyToCart.id = 'counter-display-' + str(id[i])
        form[i].addToCart.id = 'remove-button-' + str(id[i])
        form[i].howManyToCart.data = startValue[i]
        price.append(random.randint(1, 9999))

    return render_template('varukorg.html', title="varukorg", form=form, id=id, description=description,
                           imageLink=imageLink, price=price)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login_user(User())
    if form.validate_on_submit():
        cur = con.cursor()
        cur.execute("INSERT INTO Customer (Customer_ID, First_name, Last_name, Username, Email, Password) VALUES (%s, %s, %s, %s, %s, %s);", (random.randint(1,99999), 'Johan', 'Olsson', 'johols', 'ojaolo-8@gmail.com', '123'))
        con.commit()
        cur.close()

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
def comment():
    return render_template('commentSection.html', title='comment')


@app.route('/item-<int:id>', methods=['GET', 'POST'])
def item(id):
    form, idTest, description, imageLink = getTest(1)  # get test data
    id = [id]
    checkIfAddedToCartItem(form[0], id[0])  # if the form was send and is correct

    form[0].howManyToCart.id = 'counter-display-' + str(
        id[0])  # IMPORTANT!!!! The + and - buttons won't work if this isn't here
    price = []
    price.append(random.randint(1, 9999))

    return render_template('item.html', title='item', form=form, id=id, description=description, imageLink=imageLink, price=price)



@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        print('TEST', file=sys.stderr)

        print(current_user.get_id(), file=sys.stderr)
        print(current_user.getIsAdmin())

        logout_user()

    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    return render_template('profile.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
