from flask import Flask, render_template
app = Flask(__name__)



@app.route("/")
@app.route("/home")

def homello():
    #dropdown_list = ['Air', 'Land', 'Sea']

    return render_template('home.html')#,dropdown_list=dropdown_list)

@app.route("/about")
def about():
    return render_template('about.html', title="about")

@app.route("/login")
def login():
    return render_template('login.html', title="login")

@app.route("/register")
def register():
    return render_template('register.html', title="register")

if __name__ == '__main__':
    app.run(debug=True)