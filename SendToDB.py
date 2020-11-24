from Run import MySQL
from forms import *
import sys

def addCustomerInDB(form, mysql, con):
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

        if str(form.birthdayYear.data) == '-' or str(form.birthdayMonth.data) == '-' or str(form.birthdayDay.data) == '-':
            date = None
        else:
            date = str(form.birthdayYear.data) + '-' + str(form.birthdayMonth.data) + '-' + str(form.birthdayDay.data)
        cur.execute(
            "INSERT INTO Customer (Customer_ID, First_name, Last_name, Username, Email, Password, Phone_number, Birthday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
            (highestID, form.firstName.data, form.surName.data, form.username.data, form.email.data, form.password.data, form.phone.data, date))
        con.commit()
        cur.close()
        return True
    except:
        return False


def customerAlreadyInDB(form, mysql, con):
    try:
        value = []
        cur = con.cursor()

        cur.execute("SELECT * FROM customer WHERE Username=%s", (form.username.data))
        value.append(cur.fetchall())
        cur.execute("SELECT * FROM customer WHERE Email=%s", (form.email.data))
        value.append(cur.fetchall())

        print(value, file=sys.stderr)
        for i in range(len(value)):
            if (value[i] != ()):
                return True
        return False
    except:
        return True