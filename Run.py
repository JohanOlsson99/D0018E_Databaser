from flask import Flask, render_template, flash, request
from forms import RegistrationForm, LoginForm
from addToCartForm import AddToCart

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'd986e15d678b0a18d2ea47ccfc47e1ad'

@app.route("/")
@app.route("/home")
def home():
    #return render_template('itemBlock.html', title="homenot")
    return render_template('home.html', title="home")


@app.route("/about")
def about():
    return render_template('about.html', title="about")

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="login", form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title="register", form=form)

@app.route("/itemblock", methods=['GET', 'POST'])
def itemBlockAddToCart():
    form = AddToCart()

    if form.validate_on_submit():
        flash('Successfully added ' + str(form.howManyToCart.data) + ' of your items to your cart', 'success')

    elif ((form.addToCart.data == True) and (not form.validate_on_submit())):
        flash('Couldn\'t add your items to your cart. Did you know you can only add 1 to 100 items not more or less', 'danger')
    return render_template('itemBlock.html', title='block', form=form)



if __name__ == '__main__':
    app.run(debug=True)

