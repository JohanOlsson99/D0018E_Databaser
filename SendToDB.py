from Run import MySQL, USERNAMELOGIN, EMAILLOGIN, ORDERNOTSENT
from flask import url_for
from Forms import *
import sys
import traceback
from datetime import date


def customerAlreadyInDB(form, con):
    try:
        if isAdmin(form, con):
            return True
        value = []
        cur = con.cursor()
        cur.execute("SELECT * FROM Customer WHERE Username=%s;", (form.username.data))
        value.append(cur.fetchall())
        cur.execute("SELECT * FROM Customer WHERE Email=%s;", (form.email.data))
        value.append(cur.fetchall())
        cur.close()

        print(value, file=sys.stderr)
        for i in range(len(value)):
            if (value[i] != ()):
                return True
        return False
    except:
        traceback.print_exc()
        return True

def isAdmin(form, con):
    try:
        cur = con.cursor()
        value = []
        cur.execute("SELECT * FROM Admin WHERE Username=%s;", (form.username.data))
        value.append(cur.fetchall())
        cur.execute("SELECT * FROM Admin WHERE Email=%s;", (form.email.data))
        value.append(cur.fetchall())
        cur.close()

        for i in range(len(value)):
            if (value[i] != ()):
                return True
        return False
    except:
        traceback.print_exc()
        return True

def addCustomerInDB(form, con):
    try:
        cur = con.cursor()
        cur.execute("SELECT MAX(Customer_ID) FROM Customer;")
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
        traceback.print_exc()
        return False


def adminUsernameAndPasswordCorrect(form, con):
    try:
        cur = con.cursor()
        cur.execute("SELECT Password FROM Admin WHERE Username=%s;", (form.email.data))
        password = cur.fetchall()
        cur.close()
        return correctPassword(form, password)
    except:
        traceback.print_exc()
        return False


def adminEmailAndPasswordCorrect(form, con):
    try:
        cur = con.cursor()
        cur.execute("SELECT Password FROM Admin WHERE Email=%s;", (form.email.data))
        password = cur.fetchall()
        cur.close()
        return correctPassword(form, password)
    except:
        traceback.print_exc()
        return False


def customerUsernameAndPasswordCorrect(form, con):
    try:
        cur = con.cursor()
        cur.execute("SELECT Password FROM Customer WHERE Username=%s;", (form.email.data))
        password = cur.fetchall()
        cur.close()
        return correctPassword(form, password)
    except:
        traceback.print_exc()
        return False


def customerEmailAndPasswordCorrect(form, con):
    try:
        cur = con.cursor()
        cur.execute("SELECT Password FROM Customer WHERE Email=%s;", (form.email.data))
        password = cur.fetchall()
        cur.close()
        return correctPassword(form, password)
    except:
        traceback.print_exc()
        return False

def correctPassword(form, password):
    if password != ():
        password = password[0][0]
        if password == form.password.data:
            return True
    else:
        return False

def getUser(form, con, value):
    cur = con.cursor()
    if value == USERNAMELOGIN:
        cur.execute("SELECT * FROM Customer WHERE Username=%s;", (form.email.data))
        data = cur.fetchall()
        cur.close()
        return User(dataUserFormating(data, 5))
    elif value == EMAILLOGIN:
        cur.execute("SELECT * FROM Customer WHERE Email=%s;", (form.email.data))
        data = cur.fetchall()
        cur.close()
        return User(dataUserFormating(data, 5))

def getAdmin(form, con, value):
    cur = con.cursor()
    if value == USERNAMELOGIN:
        cur.execute("SELECT * FROM Admin WHERE Username=%s;", (form.email.data))
        data = cur.fetchall()
        cur.close()
        return Admin(dataUserFormating(data, 4))
    elif value == EMAILLOGIN:
        cur.execute("SELECT * FROM Admin WHERE Email=%s;", (form.email.data))
        data = cur.fetchall()
        cur.close()
        return Admin(dataUserFormating(data, 4))



def dataUserFormating(data, removeIndex):
    print(data, file=sys.stderr)
    list = []

    for i in range(len(data[0])):
        if i == removeIndex:
            continue
        list.append(data[0][i])
    return list

def getProducts(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM Products;")
    data = cur.fetchall()
    print(data)
    cur.close()
    return dataProductFormating(data)

def dataProductFormating(data):
    idList = []
    nameList = []
    priceList = []
    descList = []
    prodLeftList = []
    imageLinkList = []

    for i in range(len(data)):
        idList.append(data[i][0])
        nameList.append(data[i][1])
        priceList.append(data[i][2])
        descList.append(data[i][3])
        prodLeftList.append(data[i][4])
        imageLinkList.append(url_for('static', filename=('image/' + str(idList[i]) + '.jpg')))
    return idList, nameList, priceList, descList, prodLeftList, imageLinkList

def getProductFromId(con, id):
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM Products WHERE Products_ID=%s;", id)
        data = cur.fetchall()
        cur.close()
        return True, data[0]
    except:
        traceback.print_exc()
        return False, None

#First check if there already excist an order_details for this customer that has status (for example) pending
#if there excist an order_details then add a new Ordered_product_list with a product and number of items of that product
#remove the same amount from the product which we added to the ordered_product_list.
#if it doesn't exicist an order_details then create a new one and do the same with ordered_product_list as above.
#return True if you successfully added the product to the list and False otherwise

def addItemToOrder(con, productID, customerID, howManyItems):
    try:
        cur = con.cursor()
        cur.execute("SELECT status FROM `Order_details` WHERE `Customer_ID`=%s;", customerID)
        status = cur.fetchall()
        if status != ():
            status = status[0][0]
        else:
            status = None
        if (status == "pending"):
            cur.execute("SELECT `Order_details_ID` FROM `Order_details` WHERE `Customer_ID`=%s;", customerID)
            orderID = cur.fetchall()[0][0]
            cur.execute("SELECT `Amount_ordered` FROM `Ordered_products_list` WHERE `Product_ID`=%s AND Order_details_ID=%s;", (productID, orderID))
            check = cur.fetchall()
            cur.execute("SELECT MAX(ordered_products_list_ID) FROM Ordered_products_list;")
            newID = cur.fetchall()[0][0]
            print('test')
            print(newID)
            print('test1')
            print(check)
            if(newID == None):
                newID = 0
            else:
                newID = int(newID) + 1
            if (isEmpty(check) == False):
                newAmount = int(howManyItems) + int(check[0][0])
                cur.execute("UPDATE `Ordered_products_list` SET `Amount_ordered`=%s WHERE Product_ID=%s;", (newAmount, productID))
                #con.commit()
            else:
                cur.execute("INSERT INTO `Ordered_products_list` (`ordered_products_list_ID`, Product_ID, Order_details_ID, Amount_ordered) VALUES (%s, %s, %s, %s);", (newID, productID, orderID, howManyItems))
                #con.commit()

            cur.execute("SELECT `Products_left_in_stock` FROM Products WHERE Products_ID=%s;", productID)
            data = int(cur.fetchall()[0][0])
            newAmount = str(data - int(howManyItems))

            cur.execute("UPDATE `Products` SET `Products_left_in_stock`=%s WHERE `Products_ID`=%s;", (newAmount, productID))
            con.commit()
            cur.close()
            return True
        else:
            cur.execute("SELECT MAX(Order_details_ID) FROM Order_details;")
            orderDetailId = cur.fetchall()[0][0]
            print(orderDetailId, "orderdetail")
            if (orderDetailId == None):
                orderDetailId = 0
            else:
                orderDetailId = int(int(orderDetailId) + 1)
            #orderID = str(int(cur.fetchall()[0][0]) + 1)
            cur.execute("SELECT MAX(Order_details_ID) FROM Order_details;")
            orderProdId = cur.fetchall()[0][0]
            print(orderProdId)
            if (orderProdId == None):
                orderProdId = 0
            else:
                orderProdId = int(int(orderProdId) + 1)
            #newID = 0
            cur.execute("INSERT INTO Order_details (Order_details_ID, Customer_ID, status, date, name) VALUES (%s, %s, %s, %s, %s);", (orderDetailId, customerID, ORDERNOTSENT, str(date.today().strftime("%y-%m-%d")), 'a'))
            #con.commit()

            cur.execute("INSERT INTO Ordered_products_list (ordered_products_list_ID, Product_ID, Order_details_ID, Amount_ordered) VALUES (%s, %s, %s, %s);", (orderProdId, productID, orderDetailId, howManyItems))
            #con.commit()

            cur.execute("SELECT Products_left_in_stock FROM Products WHERE Products_ID=%s;", productID)
            newAmount = str(int(cur.fetchall()[0][0]) - int(howManyItems))

            cur.execute("UPDATE Products SET Products_left_in_stock=%s WHERE Products_ID=%s;", (newAmount, productID))
            con.commit()
            cur.close()
            return True
    except:
        traceback.print_exc()
        return False



def getProductsInCart(con, customerId):
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM Order_details WHERE Customer_ID=%s AND status=%s;", (customerId, ORDERNOTSENT))
        orderDetailID = cur.fetchall()
        print(orderDetailID)
        if orderDetailID != ():
            orderDetailID = orderDetailID[0][0]
            print(orderDetailID)
        else:
            return False, [], [], [], [], [], [], [],
        cur.execute("SELECT * FROM ordered_products_list WHERE Order_details_ID=%s", (orderDetailID))
        data = cur.fetchall()
        print(data)
        cur.close()
        productId = []
        itemsInCart = []
        for i in range(len(data)):
            productId.append(data[i][1])
            itemsInCart.append(data[i][3])
        productId, descList, imageLinkList, itemsInCart, nameList, prodLeftList, priceList = dataCartFormating(con, productId, itemsInCart)
        return True, productId, descList, imageLinkList, itemsInCart, nameList, prodLeftList, priceList

    except:
        traceback.print_exc()
        return False, [], None, None, None, None, None, None


def dataCartFormating(con, productId, itemsInCart):
    descList = []
    imageLinkList = []
    nameList = []
    prodLeftList = []
    priceList = []
    for i in range(len(productId)):
        data = getProductFromId(con, productId[i])[1]
        nameList.append(data[1])
        priceList.append(data[2])
        descList.append(data[3])
        prodLeftList.append(data[4])
        imageLinkList.append(url_for('static', filename=('image/' + str(productId[i]) + '.jpg')))
    return productId, descList, imageLinkList, itemsInCart, nameList, prodLeftList, priceList


def updateOrder(con, amount, prodId, userId):
    try:
        cur = con.cursor()
        cur.execute("SELECT `Order_details_ID` FROM `Order_details` WHERE Customer_ID=%s AND status=%s;", (userId, ORDERNOTSENT))
        orderDetailsId = cur.fetchone()
        #print('fetchone', orderDetailsId)

        if orderDetailsId != None:
            orderDetailsId = orderDetailsId[0]
            cur.execute("SELECT * FROM `Ordered_products_list` WHERE `Order_details_ID`=%s AND `Product_ID`=%s;", (orderDetailsId, prodId))
            data = cur.fetchone()
            #print("data for ordered_products_list", data)
            #print('amount and data[3]', amount, data[3])
            if amount != data[3]:
                if amount == 0:
                    cur.execute("SET foreign_key_checks = 0;")
                    cur.execute("DELETE FROM `Ordered_products_list` WHERE Order_details_ID=%s AND Product_ID=%s;", (orderDetailsId, prodId))
                    cur.execute("SELECT * FROM `Ordered_products_list` WHERE Order_details_ID=%s;", (orderDetailsId))
                    temp = cur.fetchall()
                    if temp == ():
                        cur.execute("DELETE FROM `Order_details` WHERE Order_details_ID=%s;", (orderDetailsId))
                    cur.execute("SET foreign_key_checks = 1;")
                else:
                    cur.execute("UPDATE `Ordered_products_list` SET Amount_ordered=%s WHERE Order_details_ID=%s AND Product_ID=%s;", (amount, orderDetailsId, prodId))
                    #con.commit()
                cur.execute("SELECT Products_left_in_stock FROM Products WHERE Products_ID=%s", (prodId))
                diff = amount - int(data[3])
                left = cur.fetchone()[0]
                left = left - diff

                cur.execute("UPDATE Products SET Products_left_in_stock=%s WHERE Products_ID=%s", (left, prodId))
                con.commit()
                cur.close()
                return True
        cur.close()
        return False
    except:
        traceback.print_exc()
        return False

def isEmpty(structure):
    if structure:
        return False
    else:
        return True