from flask import Flask, render_template, flash, request, url_for, redirect
from forms import RegistrationForm, LoginForm, PaymentForm
from addToCartForm import AddToCart 

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'd986e15d678b0a18d2ea47ccfc47e1ad'

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = AddToCart()
    checkIfAddedToCart(form)
    return render_template('home.html', title="home", form=form)

def checkIfAddedToCart(form):
    if form.validate_on_submit():
        flash('Successfully added ' + str(form.howManyToCart.data) + ' of your items to your cart', 'success')

    elif ((form.addToCart.data == True) and (not form.validate_on_submit())):
        flash('Couldn\'t add your items to your cart. Did you know you can only add 1 to 100 items not more or less',
              'danger')


@app.route("/varukorg")
def kundkorg():
    return render_template('varukorg.html', title="varukorg")

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="login", form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/betalning", methods=['GET','POST'])
def betalning():
    form = PaymentForm()
    return render_template('betalning.html', title='betalning', form=form)



#@app.route("/itemblock", methods=['GET', 'POST'])
#def itemBlockAddToCart():
#    form = AddToCart()
#
#    if form.validate_on_submit():
#        flash('Successfully added ' + str(form.howManyToCart.data) + ' of your items to your cart', 'success')
#
#    elif ((form.addToCart.data == True) and (not form.validate_on_submit())):
#        flash('Couldn\'t add your items to your cart. Did you know you can only add 1 to 100 items not more or less', 'danger')
#    return render_template('itemBlock.html', title='block', form=form)



if __name__ == '__main__':
    app.run(debug=True)

