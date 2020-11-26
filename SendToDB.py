from Run import MySQL, USERNAMELOGIN, EMAILLOGIN
from forms import *
import sys


def customerAlreadyInDB(form, con):
    try:
        if isAdmin(form, con):
            return True
        value = []
        cur = con.cursor()
        cur.execute("SELECT * FROM Customer WHERE Username=%s", (form.username.data))
        value.append(cur.fetchall())
        cur.execute("SELECT * FROM Customer WHERE Email=%s", (form.email.data))
        value.append(cur.fetchall())
        cur.close()

        print(value, file=sys.stderr)
        for i in range(len(value)):
            if (value[i] != ()):
                return True
        return False
    except:
        return True

def isAdmin(form, con):
    try:
        cur = con.cursor()
        value = []
        cur.execute("SELECT * FROM Admin WHERE Username=%s", (form.username.data))
        value.append(cur.fetchall())
        cur.execute("SELECT * FROM Admin WHERE Email=%s", (form.email.data))
        value.append(cur.fetchall())
        cur.close()

        for i in range(len(value)):
            if (value[i] != ()):
                return True
        return False
    except:
        return True

def addCustomerInDB(form, con):
    try:
        cur = con.cursor()
        cur.execute("SELECT MAX(Customer_ID) FROM Customer")
        highestID = cur.fetchall()
        if highestID[0][0] != None:
            print(highestID[0][0], file=sys.stderr)
            highestID = int(highestID[0][0]) + 1
            print(highestID, file=sys.stderr)
        else:
            highestID = 0

        if str(form.birthdayYear.data) == '-' or str(form.birthdayMonth.data) == '-' or str(
                form.birthdayDay.data) == '-':
            date = None
        else:
            date = str(form.birthdayYear.data) + '-' + str(form.birthdayMonth.data) + '-' + str(form.birthdayDay.data)
        cur.execute(
            "INSERT INTO Customer (Customer_ID, First_name, Last_name, Username, Email, Password, Phone_number, Birthday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
            (highestID, form.firstName.data, form.surName.data, form.username.data, form.email.data, form.password.data,
             form.phone.data, date))
        con.commit()
        cur.close()
        return True
    except:
        return False


def adminUsernameAndPasswordCorrect(form, con):
    try:
        cur = con.cursor()

        cur.execute("SELECT Password FROM Admin WHERE Username=%s", (form.email.data))
        password = cur.fetchall()
        cur.close()
        if password != ():
            password = password[0][0]
        if password == form.password.data:
            return True
        else:
            return False
    except:
        return False


def adminEmailAndPasswordCorrect(form, con):
    try:
        cur = con.cursor()
        cur.execute("SELECT Password FROM Admin WHERE Email=%s", (form.email.data))
        password = cur.fetchall()
        cur.close()
        if password != ():
            password = password[0][0]
        else:
            return False
        if password == form.password.data:
            return True
        else:
            return False
    except:
        return False


def customerUsernameAndPasswordCorrect(form, con):
    try:
        cur = con.cursor()

        cur.execute("SELECT Password FROM Customer WHERE Username=%s", (form.email.data))
        password = cur.fetchall()
        cur.close()
        if password != ():
            password = password[0][0]
        if password == form.password.data:
            return True
        else:
            return False
    except:
        return False


def customerEmailAndPasswordCorrect(form, con):
    try:
        cur = con.cursor()
        cur.execute("SELECT Password FROM Customer WHERE Email=%s", (form.email.data))
        password = cur.fetchall()
        cur.close()
        if password != ():
            password = password[0][0]
        else:
            return False
        if password == form.password.data:
            return True
        else:
            return False
    except:
        return False


def getUser(form, con, value):
    cur = con.cursor()
    if value == USERNAMELOGIN:
        cur.execute("SELECT * FROM Customer WHERE Username=%s", (form.email.data))
        data = cur.fetchall()
        cur.close()
        return User(dataFormating(data, 5))
    elif value == EMAILLOGIN:
        cur.execute("SELECT * FROM Customer WHERE Email=%s", (form.email.data))
        data = cur.fetchall()
        cur.close()
        return User(dataFormating(data, 5))

def getAdmin(form, con, value):
    cur = con.cursor()
    if value == USERNAMELOGIN:
        cur.execute("SELECT * FROM Admin WHERE Username=%s", (form.email.data))
        data = cur.fetchall()
        cur.close()
        return Admin(dataFormating(data, 4))
    elif value == EMAILLOGIN:
        cur.execute("SELECT * FROM Admin WHERE Email=%s", (form.email.data))
        data = cur.fetchall()
        cur.close()
        return Admin(dataFormating(data, 4))



def dataFormating(data, removeIndex):
    print(data, file=sys.stderr)
    list = []

    for i in range(len(data[0])):
        if i == removeIndex:
            continue
        list.append(data[0][i])
    return list

def getProducts(con):

