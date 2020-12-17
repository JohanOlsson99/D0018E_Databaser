from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField, \
    validators, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from wtforms.widgets import TextArea
from flask_login import UserMixin
from wtforms.widgets import TextArea


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    firstName = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    surName = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
    phone = IntegerField('Phone Number', validators=[validators.optional()])
    birthdayDay = SelectField(
        'Day',
        choices=[('-', '-'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'),
                 (9, '09'), (10, '10'),
                 (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'),
                 (19, '19'), (20, '20'), (21, '21'),
                 (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'),
                 (30, '30'), (31, '31')]
    )
    birthdayMonth = SelectField(
        'Month',
        choices=[('-', '-'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'),
                 (9, '09'), (10, '10'),
                 (11, '11'), (12, '12')]
    )
    birthdayYear = SelectField(
        'Year',
        choices=[('-', '-'), (2020, '2020'), (2019, '2019'), (2018, '2018'), (2017, '2017'), (2016, '2016'),
                 (2015, '2015'),
                 (2014, '2014'), (2013, '2013'), (2012, '2012'), (2011, '2011'), (2010, '2010'), (2009, '2009'),
                 (2008, '2008'),
                 (2007, '2007'), (2006, '2006'), (2005, '2005'), (2004, '2004'), (2003, '2003'), (2002, '2002'),
                 (2001, '2001'),
                 (2000, '2000'), (1999, '1999'), (1998, '1998'), (1997, '1997'), (1996, '1996'), (1995, '1995'),
                 (1994, '1994'),
                 (1993, '1993'), (1992, '1992'), (1991, '1991'), (1990, '1990'), (1989, '1989'), (1988, '1988'),
                 (1987, '1987'),
                 (1986, '1986'), (1985, '1985'), (1984, '1984'), (1983, '1983'), (1982, '1982'), (1981, '1981'),
                 (1980, '1980'),
                 (1979, '1979'), (1978, '1978'), (1977, '1977'), (1976, '1976'), (1975, '1975'), (1974, '1974'),
                 (1973, '1973'),
                 (1972, '1972'), (1971, '1971'), (1970, '1970'), (1969, '1969'), (1968, '1968'), (1967, '1967'),
                 (1966, '1966'),
                 (1965, '1965'), (1964, '1964'), (1963, '1963'), (1962, '1962'), (1961, '1961'), (1960, '1960'),
                 (1959, '1959'),
                 (1958, '1958'), (1957, '1957'), (1956, '1956'), (1955, '1955'), (1954, '1954'), (1953, '1953'),
                 (1952, '1952'),
                 (1951, '1951'), (1950, '1950'), (1949, '1949'), (1948, '1948'), (1947, '1947'), (1946, '1946'),
                 (1945, '1945'),
                 (1944, '1944'), (1943, '1943'), (1942, '1942'), (1941, '1941'), (1940, '1940'), (1939, '1939'),
                 (1938, '1938'),
                 (1937, '1937'), (1936, '1936'), (1935, '1935'), (1934, '1934'), (1933, '1933'), (1932, '1932'),
                 (1931, '1931'),
                 (1930, '1930'), (1929, '1929'), (1928, '1928'), (1927, '1927'), (1926, '1926'), (1925, '1925'),
                 (1924, '1924'),
                 (1923, '1923'), (1922, '1922'), (1921, '1921'), (1920, '1920'), (1919, '1919'), (1918, '1918'),
                 (1917, '1917'),
                 (1916, '1916'), (1915, '1915'), (1914, '1914'), (1913, '1913'), (1912, '1912'), (1911, '1911'),
                 (1910, '1910'),
                 (1909, '1909'), (1908, '1908'), (1907, '1907'), (1906, '1906'), (1905, '1905'), (1904, '1904'),
                 (1903, '1903'),
                 (1902, '1902'), (1901, '1901'), (1900, '1900')]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email or username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=20)])
    firstName = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    surName = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[validators.optional()])
    birthdayDay = SelectField(
        'Day',
        choices=[('-', '-'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'),
                 (9, '09'), (10, '10'),
                 (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'),
                 (19, '19'), (20, '20'), (21, '21'),
                 (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'),
                 (30, '30'), (31, '31')]
    )
    birthdayMonth = SelectField(
        'Month',
        choices=[('-', '-'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'),
                 (9, '09'), (10, '10'),
                 (11, '11'), (12, '12')]
    )
    birthdayYear = SelectField(
        'Year',
        choices=[('-', '-'), (2020, '2020'), (2019, '2019'), (2018, '2018'), (2017, '2017'), (2016, '2016'),
                 (2015, '2015'),
                 (2014, '2014'), (2013, '2013'), (2012, '2012'), (2011, '2011'), (2010, '2010'), (2009, '2009'),
                 (2008, '2008'),
                 (2007, '2007'), (2006, '2006'), (2005, '2005'), (2004, '2004'), (2003, '2003'), (2002, '2002'),
                 (2001, '2001'),
                 (2000, '2000'), (1999, '1999'), (1998, '1998'), (1997, '1997'), (1996, '1996'), (1995, '1995'),
                 (1994, '1994'),
                 (1993, '1993'), (1992, '1992'), (1991, '1991'), (1990, '1990'), (1989, '1989'), (1988, '1988'),
                 (1987, '1987'),
                 (1986, '1986'), (1985, '1985'), (1984, '1984'), (1983, '1983'), (1982, '1982'), (1981, '1981'),
                 (1980, '1980'),
                 (1979, '1979'), (1978, '1978'), (1977, '1977'), (1976, '1976'), (1975, '1975'), (1974, '1974'),
                 (1973, '1973'),
                 (1972, '1972'), (1971, '1971'), (1970, '1970'), (1969, '1969'), (1968, '1968'), (1967, '1967'),
                 (1966, '1966'),
                 (1965, '1965'), (1964, '1964'), (1963, '1963'), (1962, '1962'), (1961, '1961'), (1960, '1960'),
                 (1959, '1959'),
                 (1958, '1958'), (1957, '1957'), (1956, '1956'), (1955, '1955'), (1954, '1954'), (1953, '1953'),
                 (1952, '1952'),
                 (1951, '1951'), (1950, '1950'), (1949, '1949'), (1948, '1948'), (1947, '1947'), (1946, '1946'),
                 (1945, '1945'),
                 (1944, '1944'), (1943, '1943'), (1942, '1942'), (1941, '1941'), (1940, '1940'), (1939, '1939'),
                 (1938, '1938'),
                 (1937, '1937'), (1936, '1936'), (1935, '1935'), (1934, '1934'), (1933, '1933'), (1932, '1932'),
                 (1931, '1931'),
                 (1930, '1930'), (1929, '1929'), (1928, '1928'), (1927, '1927'), (1926, '1926'), (1925, '1925'),
                 (1924, '1924'),
                 (1923, '1923'), (1922, '1922'), (1921, '1921'), (1920, '1920'), (1919, '1919'), (1918, '1918'),
                 (1917, '1917'),
                 (1916, '1916'), (1915, '1915'), (1914, '1914'), (1913, '1913'), (1912, '1912'), (1911, '1911'),
                 (1910, '1910'),
                 (1909, '1909'), (1908, '1908'), (1907, '1907'), (1906, '1906'), (1905, '1905'), (1904, '1904'),
                 (1903, '1903'),
                 (1902, '1902'), (1901, '1901'), (1900, '1900')]
    )
    password = PasswordField('Password', validators=[DataRequired()])


class PaymentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])

    cardnumber = StringField('Card', validators=[DataRequired()])

    adress = StringField('Adress', validators=[DataRequired()])

    Postnummer = StringField('Postal Number*', validators=[DataRequired()])

    Stad = StringField('City', validators=[DataRequired()])

    Land = StringField('Country', validators=[DataRequired()])

    submit = SubmitField('Send Order')


class AddToCart(FlaskForm):
    howManyToCart = IntegerField('amount', validators=[NumberRange(min=0, max=100)])
    addToCart = SubmitField('Add to cart')

    def defineMaxMin(self, min=0, max=100):
        self.howManyToCart.validators = [NumberRange(min=min, max=max)]

    def defineHowManyToCartId(self, id):
        self.howManyToCart.id = 'counter-display-' + str(id)


class cartForm(FlaskForm):
    form = []
    reload = SubmitField('Reload Cart')

    def __init__(self, id, itemsInCart, maxValue):
        super().__init__()
        for i in range(len(id)):
            self.form.append(cartIndividualForm())
            self.form[i].defineMaxMin(max=maxValue[i])
            self.form[i].defineStartUpValues(id[i], itemsInCart[i])
        # self.reload.id = "button continue-button reload-button"

    def getForm(self, index):
        return self.form[index]

    def getReload(self):
        return self.reload

    # howManyToCart = IntegerField('amount', validators=[NumberRange(min=0, max=100)])
    # addToCart = SubmitField('Remove')

    # def defineMaxMin(self, min=0, max=100):
    #    self.howManyToCart.validators = [NumberRange(min=min, max=max)]

    # def defineHowManyToCartId(self, id):
    #    self.howManyToCart.id = 'counter-display-' + str(id)


class cartIndividualForm(FlaskForm):
    howManyToCart = IntegerField('amount', validators=[NumberRange(min=0, max=100)])
    addToCart = SubmitField('Update')

    def defineMaxMin(self, min=0, max=100):
        self.howManyToCart.validators = [NumberRange(min=min, max=max)]

    def defineStartUpValues(self, id, itemsInCart):
        self.howManyToCart.id = 'counter-display-' + str(id)
        self.addToCart.id = 'remove-button-' + str(id)
        # self.howManyToCart.data = itemsInCart


class addProductsForm(FlaskForm):
    productName = StringField('Product name', validators=[DataRequired()])
    productDescription = StringField('Product description', widget=TextArea(),
                                     validators=[DataRequired(), Length(max=255)])
    productPrice = FloatField('Product price', validators=[DataRequired()])
    productLeft = IntegerField('Product left', validators=[DataRequired()])
    upload = SubmitField('Upload')


class User():
    def __init__(self, list):
        self.id = list[0]
        self.firstname = list[1]
        self.lastname = list[2]
        self.username = list[3]
        self.email = list[4]
        self.phone = list[5]
        self.birthday = list[6]

    def getId(self):
        return self.id

    def getFirstname(self):
        return self.firstname

    def getLastname(self):
        return self.lastname

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.email

    def getPhone(self):
        return self.phone

    def getBirthday(self):
        return self.birthday


class Admin():
    def __init__(self, list):
        self.id = list[0]
        self.name = list[1]
        self.username = list[2]
        self.Email = list[3]

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getUsername(self):
        return self.username

    def getEmail(self):
        return self.Email


class searchForm(FlaskForm):
    productName = StringField('Search product', validators=[Length(max=60)])


class Comment(FlaskForm):
    comment = StringField('comment', widget=TextArea())       
    rating = SelectField(
        'Rate',
        choices=[('-', '-'), (1, '1'), (2, '2'), (3, '3'), (4, '4'),
                 (5, '5')])     
    submit = SubmitField('POST')
   

   