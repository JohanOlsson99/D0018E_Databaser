from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'd986e15d678b0a18d2ea47ccfc47e1ad'

@app.route("/")
@app.route("/home")

def homello():
    #dropdown_list = ['Air', 'Land', 'Sea']
    return render_template('itemBlock.html', title="home")
    #return render_template('home.html', title="home")#,dropdown_list=dropdown_list)

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

if __name__ == '__main__':
    app.run(debug=True)