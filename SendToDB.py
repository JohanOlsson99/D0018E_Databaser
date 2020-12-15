from Run import MySQL, USERNAMELOGIN, EMAILLOGIN, ORDERNOTSENT, ORDERRESERVED
from flask import url_for
from Forms import *
import sys
import traceback
from datetime import date

def mergeSqlCommand(commandStart, commandEnd, changedStrDB, changedForms):
    sqlCommand = commandStart
    for i in enumerate(changedStrDB):
        i = i[0]
        if i != 0: 
            sqlCommand += ", "
        if type(changedForms[i]) is int:
            sqlCommand += ("`" + changedStrDB[i] + "`=%s" % changedForms[i])
        else: 
            sqlCommand += ("`" + changedStrDB[i] + "`='%s'" % changedForms[i]) 
    sqlCommand += commandEnd
    return sqlCommand

def updateAdminInDB(form, con, userId):
    cur = con.cursor()
    cur.execute("SELECT * FROM Admin WHERE Admin_ID=%s", userId)
    data = cur.fetchall()
    data = dataUserFormating(data, 0)

    strDB = (
        'Name',
        'Username',
        'Email',
        'Password'
    )
    formList = [
        form.name.data,
        form.username.data,
        form.email.data,
        form.password.data
    ]

    changed = [idx for idx, i in enumerate(formList) if (i != data[idx] and i != '')]
    if form.username.data != data[1] and usernameAlreadyAssigned(form, con):
        changed = [i for i in changed if (i != 1)]
        form.username.data = data[1]
    if form.email.data != data[2] and emailAlreadyAssigned(form, con):
        changed = [i for i in changed if (i != 2)]
        form.email.data = data[2]
    if len(changed) > 0:
        changedForms = [formList[i] for i in changed]
        changedStrDB = [(strDB[i]) for i in changed]
        sqlCommand = mergeSqlCommand("UPDATE `Admin` SET ", " WHERE `Admin_ID`=%s;" % userId, changedStrDB, changedForms)
        cur.execute(sqlCommand)
        cur.close()
        con.commit()

    user = Admin([
        userId,
        form.name.data, 
        form.username.data,
        form.email.data
    ])

    return user

def updateUserInDB(form, con, userId):
    cur = con.cursor()
    cur.execute("SELECT * FROM Customer WHERE Customer_ID=%s", userId)
    data = cur.fetchall()
    data = dataUserFormating(data, 0)

    strDB = (
        'First_name', 
        'Last_name', 
        'Username', 
        'Email', 
        'Password', 
        'Phone_number', 
        'Birthday'
    )
    try:
        formDate = date(
            int(form.birthdayYear.data), 
            int(form.birthdayMonth.data), 
            int(form.birthdayDay.data)
        )
    except:
        formDate = None
    formList = [
        form.firstName.data, 
        form.surName.data, 
        form.username.data, 
        form.email.data, 
        form.password.data, 
        form.phone.data, 
        formDate
    ]

    changed = [idx for idx, i in enumerate(formList) if (i != data[idx] and i != '')]
    if form.username.data != data[2] and usernameAlreadyAssigned(form, con):
        changed = [i for i in changed if (i != 2)]
        form.username.data = data[2]
    if form.email.data != data[3] and emailAlreadyAssigned(form, con):
        changed = [i for i in changed if (i != 3)]
        form.email.data = data[3]
    if len(changed) > 0:
        changedForms = [formList[i] for i in changed]
        changedStrDB = [(strDB[i]) for i in changed]
        sqlCommand = mergeSqlCommand("UPDATE `Customer` SET ", " WHERE `Customer_ID`=%s;" % userId, changedStrDB, changedForms)
        cur.execute(sqlCommand)
        cur.close()
        con.commit()
        
    user = User([
        userId, 
        form.firstName.data, 
        form.surName.data, 
        form.username.data, 
        form.email.data, 
        form.phone.data, 
        formDate
    ])

    return user

def usernameAlreadyAssigned(form, con):
    try:
        if isAdmin(form, con):
            return True
        value = []
        cur = con.cursor()
        cur.execute("SELECT * FROM Customer WHERE Username=%s;", (form.username.data))
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

def emailAlreadyAssigned(form, con):
    try:
        if isAdmin(form, con):
            return True
        value = []
        cur = con.cursor()
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

        cur.execute("SELECT `Order_details_ID` FROM `Order_details` WHERE `Customer_ID`=%s AND status=%s;", (customerID, ORDERNOTSENT))
        orderDetailsId = cur.fetchone()
        if orderDetailsId is not None:
        #print(orderDetailsId)
        #print(status, 'status')
        #if status != ():
        #    status = status[0][0]
        #else:
        #    status = None
        #print(status, 'status')

        #if (status == "pending"):
            #cur.execute("SELECT `Order_details_ID` FROM `Order_details` WHERE `Customer_ID`=%s;", customerID)
            #orderID = cur.fetchall()[0][0]
            cur.execute("SELECT `Amount_ordered` FROM `Ordered_products_list` WHERE `Product_ID`=%s AND Order_details_ID=%s;", (productID, orderDetailsId))
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
                cur.execute("INSERT INTO `Ordered_products_list` (`ordered_products_list_ID`, Product_ID, Order_details_ID, Amount_ordered) VALUES (%s, %s, %s, %s);", (newID, productID, orderDetailsId, howManyItems))
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
            orderDetailIdmax = cur.fetchone()[0]
            print(orderDetailIdmax, "orderdetail")
            if (orderDetailIdmax == None):
                orderDetailId = 0
            else:
                orderDetailId = int(int(orderDetailIdmax) + 1)
            #orderID = str(int(cur.fetchall()[0][0]) + 1)
            cur.execute("SELECT MAX(ordered_products_list_ID) FROM Ordered_products_list;")
            orderProdId = cur.fetchall()
            print(orderProdId)
            if (orderProdId[0][0] == None):
                orderProdId = 0
            else:
                orderProdId = int(int(orderProdId[0][0]) + 1)
            #newID = 0
            cur.execute("INSERT INTO Order_details (Order_details_ID, Customer_ID, status, date, name) VALUES (%s, %s, %s, %s, %s);", (orderDetailId, customerID, ORDERNOTSENT, str(date.today().strftime("%y-%m-%d")), 'a'))
            con.commit()

            cur.execute("INSERT INTO Ordered_products_list (ordered_products_list_ID, Product_ID, Order_details_ID, Amount_ordered) VALUES (%s, %s, %s, %s);", (orderProdId, productID, orderDetailId, howManyItems))
            con.commit()

            cur.execute("SELECT Products_left_in_stock FROM Products WHERE Products_ID=%s;", productID)
            newAmount = str(int(cur.fetchall()[0][0]) - int(howManyItems))

            cur.execute("UPDATE Products SET Products_left_in_stock=%s WHERE Products_ID=%s;", (newAmount, productID))
            con.commit()
            cur.close()
            return True
    except:
        traceback.print_exc()
        return False

def getProductsInCartNew(con, customerId):
    #print("CORRECT METHOD")
    query = "SELECT " \
    "Product_ID, Product_name, Product_price, Product_description, Products_left_in_stock, " \
            "Amount_ordered FROM Ordered_products_list " \
            "INNER JOIN Products ON Ordered_products_list.Order_details_ID = %s AND " \
            "Products.Products_ID = Ordered_products_list.Product_ID;"

    cur = con.cursor()
    cur.execute("SELECT Order_details_ID FROM Order_details WHERE Customer_ID=%s AND status=%s;", (customerId, ORDERNOTSENT))
    orderDetailID = cur.fetchone()
    #print(orderDetailID)
    if orderDetailID == None:
        return False, [], [], [], [], [], [], []
    else:
        cur.execute(query, (orderDetailID))
        data = cur.fetchall()
        cur.close()
        #print(data)
        #print(dataCartFormatingNew(data))
        return dataCartFormatingNew(data)

def dataCartFormatingNew(data):
    #print("CORRECT METHOD")
    productId = []
    descList = []
    imageLinkList = []
    itemsInCart = []
    nameList = []
    prodLeftList = []
    priceList = []

    for i in range(len(data)):
        productId.append(data[i][0])
        nameList.append(data[i][1])
        priceList.append(data[i][2])
        descList.append(data[i][3])
        prodLeftList.append(data[i][4])
        itemsInCart.append(data[i][5])
        imageLinkList.append(url_for('static', filename=('image/' + str(productId[i]) + '.jpg')))

    return True, productId, descList, imageLinkList, itemsInCart, nameList, prodLeftList, priceList


def getProductsInCart(con, customerId):
    #print("WRONG METHOD")
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM Order_details WHERE Customer_ID=%s AND status=%s;", (customerId, ORDERNOTSENT))
        orderDetailID = cur.fetchall()
        #print(orderDetailID)
        if orderDetailID != ():
            orderDetailID = orderDetailID[0][0]
            #print(orderDetailID)
        else:
            return False, [], [], [], [], [], [], []
        cur.execute("SELECT * FROM Ordered_products_list WHERE Order_details_ID=%s", (orderDetailID))
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
            orderDetailsId = orderDetailsId
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

                cur.execute("UPDATE Products SET Products_left_in_stock=%s WHERE Products_ID=%s;", (left, prodId))
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


def setReservedOrder(con, customerId):
    cur = con.cursor()
    cur.execute("SELECT `Order_details_ID` FROM `Order_details` WHERE Customer_ID=%s AND status=%s;",
                (customerId, ORDERNOTSENT))
    orderDetailsId = cur.fetchone()
    # print('fetchone', orderDetailsId)

    if orderDetailsId != None:
        orderDetailsId = orderDetailsId[0]
    else:
        return False
    cur.execute("UPDATE `Order_details` SET status=%s WHERE Order_details_ID=%s", (ORDERRESERVED, orderDetailsId))
    con.commit()
    cur.close()
    return True


def getAllCommentsForOneItem(con, productId):
    cur = con.cursor()
    cur.execute("SELECT * FROM `comments` WHERE `Product_ID`=%s;", (productId))
    data = cur.fetchall()
    #print('comment data', data)
    if data != ():
        customerList = []
        adminList = []
        comment = []
        dateList = []
        print(len(data))
        for i in range(len(data)):
            if((data[i][1] == None) and (data[i][2] != None)):
                #print('Admin Data')
                cur.execute("SELECT Name FROM `Admin` WHERE Admin_ID=%s", (data[i][2]))
                customerList.append(None)
                adminList.append(cur.fetchone()[0])
            elif((data[i][1] != None) and (data[i][2] == None)):
                #print('customer data')
                cur.execute("SELECT First_name, Last_name FROM `Customer` WHERE Customer_ID=%s", (data[i][1]))
                name = cur.fetchall()
                name = str(name[0][0]) + " " + str(name[0][1])
                customerList.append(name)
                adminList.append(None)
            else:
                #print('both None')
                continue
            comment.append(data[i][4])
            dateList.append(data[i][5])
        return customerList, adminList, comment, dateList
    else:
        #print('no data')
        return [], [], [], []

def addCommentToAProduct(con, productId, customerId, adminId, form):
    cur = con.cursor()
    cur.execute("SELECT MAX(Comments_ID) FROM `Comments`;")
    newId = cur.fetchone()[0]
    if newId != None:
        newId = int(newId) + 1
    else:
        newId = 0
    #comment = form.comment.data
    comment = form
    currentDate = date.today().strftime("%y-%m-%d")
    cur.execute("INSERT INTO `Comments` VALUES (%s, %s, %s, %s, %s, %s);", (newId, customerId,
                                                                            adminId, productId, comment, currentDate))
    con.commit()
    #Comments_ID, Customer_ID, Admin_ID, Product_ID, Comment, date

def addNewProductAndGetNewId(con, form):
    cur = con.cursor()
    cur.execute("SELECT MAX(Products_ID) FROM Products;")
    maxId = cur.fetchone()
    print(maxId)
    if maxId is not None:
        newId = int(maxId[0]) + 1
    else:
        newId = 0

    cur.execute("INSERT INTO `Products`"
                "(`Products_ID`, `Product_name`, `Product_price`, `Product_description`, `Products_left_in_stock`)"
                "VALUES (%s, %s, %s, %s, %s);", (newId, str(form.productName.data), form.productPrice.data,
                                     str(form.productDescription.data), form.productLeft.data))
    con.commit()
    return newId
