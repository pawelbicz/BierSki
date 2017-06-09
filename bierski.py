import flask
from flask import Flask
from flask import g, request, render_template
import datetime
import flask, flask_mysqldb, flask.views, linecache, os, functools, json, ConfigParser, werkzeug, collections
from flask import g, request, render_template, jsonify

from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "123"

########################################### DATABASE CONNETION ############################################

config = ConfigParser.SafeConfigParser()
config.read('/home/BierSki/config.ini')
app.config['MYSQL_USER'] = config.get('KEY', 'user')
app.config['MYSQL_PASSWORD'] = config.get('KEY', 'password')
app.config['MYSQL_DB'] = config.get('KEY', 'database')
app.config['MYSQL_HOST'] = config.get('KEY', 'host')
mysql = MySQL(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR']
# @app.route('/')

def logowanie():
    print "logowanie metoda!!!!"
    print flask.request.form
    if 'logout' in flask.request.form:
        flask.session.pop('username', None)
        return "Wylogowano"
        # return flask.redirect(flask.url_for('index'))
    if 'login' in flask.request.form:
        print 'hakuna'
        username = flask.request.form['username']
        password = flask.request.form['password']
        ifLoginProperly = 0
        conn = mysql.connection
        cursor = conn.cursor()
        print cursor.execute("SELECT * FROM users")
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print row
            if username == row[1] and password == row[2]:
                flask.session['username'] = username
                ifLoginProperly = 1
        if ifLoginProperly == 0:
            flask.flash("Login lub haslo bledne")
        return "Logowanie"

def addUserToDatabase(login,password,role):
    print 'addUserToData'
    ifLoginExists = 0
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if login == row[1]:
            ifLoginExists = 1
    if ifLoginExists == 1:
        print "Debug: Nie dodano uzytkownika poniewaz jest juz w bazie"
        return "Nie dodano uzytkownika poniewaz jest juz w bazie"
    else:
        mysqlCmd = "INSERT INTO users (`u_username`,`u_password`,`u_role`) VALUES (" + "'"+str(login)+"','"+str(password)+"','"+str(role)+"');"
        print "mysqlCmd: "+mysqlCmd
        cursor.execute(mysqlCmd)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print row
        return "Dodano uzytkownika do bazy danych"

def listUsers():
    listOfUsers = []
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        listOfUsers.append(row)
    return listOfUsers

def removeUserFromDatabase(login):
    ifLoginExist = 0
    listOfUsers = listUsers()
    for user in listOfUsers:
        if login == user[1]:
            print 'uzytkowniek jest w bazie'
            ifLoginExist = 1
    if ifLoginExist == 0:
        print "Uzytkownika nie ma bazie"
        return "Uzytkownika nie ma bazie"
    else:
        print 'hakuna'
        conn = mysql.connection
        cursor = conn.cursor()
        mysqlCmd = "DELETE FROM `users` WHERE u_username = "+"'"+str(login)+"';"
        print mysqlCmd
        cursor.execute(mysqlCmd)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print row
        return "Uzytkownik o podanym loginie zostal usuniety z bazy"

def addEquipmentToDatabase(type,brand,prod_year,status):
    print 'addEquipmentToDatabase'
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    mysqlCmd = ( "INSERT INTO `equipment`"
                 "(`e_type`,`e_brand`,`e_prod_year`,`e_status`)"
                 " VALUES ("
                 "'"+str(type)+"','"+str(brand)+"','"+prod_year+"','"+status+"');"
               )
    print mysqlCmd
    cursor.execute(mysqlCmd)
    cursor.execute("SELECT * FROM equipment")
    rows = cursor.fetchall()
    for row in rows:
        print row
    return "Dodano sprzet do bazy danych"

def RentEquipment(year,month,day,user_id,equipment_id):
    print RentEquipment
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    mysqlCmd = "INSERT INTO `orders` (`o_date_start`, `u_id`, `e_id`) VALUES ('"+str(year)+"-"+str(month)+"-"+str(day)+"','"+str(user_id)+"','"+str(equipment_id)+"');"
    print mysqlCmd
    cursor.execute(mysqlCmd)
    return "Wypozyczono sprzet"

def listEquipment():
    listOfEquipment = []
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipment")
    rows = cursor.fetchall()
    for row in rows:
        listOfEquipment.append(row)
    return listOfEquipment

def removeEquipmentFromDatabase(e_id):
    print "e_id= "+e_id
    listOfEquipment = listEquipment()
    for i in range(len(listOfEquipment)):
        print listOfEquipment[i][0]
        print 'type(listOfEquipment[i][0])'+type(listOfEquipment[i][0])
        if e_id == listOfEquipment[i][0]:
            print "ID sprzetu do usuniecia sie zgadza"
        else:
            print "Id niezgodne"
    return listOfEquipment

def listOrders():
    listOfOrders = []
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    for row in rows:
        listOfOrders.append(row)
    return listOfOrders

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
    def post(self):
        logowanie()
        if 'wypozycz' in flask.request.form:
            print "przejdz do sklepu dziala"
        print 'redirect page!!!'
        return flask.redirect(flask.url_for('index'))

class Add(flask.views.MethodView):
    def get(self):
        return flask.render_template('addUser.html')
    def post(self):
        if 'removeUser' in flask.request.form:
            print 'kliknieto removeUser'
            login = flask.request.form['username']
            removeUserFromDatabase(login)
        elif 'adduser' in flask.request.form:
            print 'kliknieto adduser'
            username = flask.request.form['username']
            password = flask.request.form['password']
            role = flask.request.form['role']
            result = addUserToDatabase(username,password,role)
            listUsers()
        elif 'listUsers' in flask.request.form:
            print 'kliknieto listUser'
            listOfUsers = []
            loginList = []
            listOfUsers = listUsers()
            print "uwaga printuje"
            for user in listOfUsers:
                loginList.append(user[1])
            print loginList
            loginList = [x.encode('utf8') for x in loginList]
            for x in range(len(loginList)):
                flask.flash(loginList[x])
        return flask.redirect(flask.url_for('add'))

class Equipment(flask.views.MethodView):
    def get(self):
        return flask.render_template('equipment.html')
    def post(self):
        if 'addEquipment' in flask.request.form:
            type = flask.request.form['type']
            brand = flask.request.form['brand']
            prod_year = flask.request.form['prod_year']
            status = flask.request.form['status']
            addEquipmentToDatabase(type,brand,prod_year,status)
        elif 'removeEquipmentButton' in flask.request.form:
            print 'kliknieto removeEquipment'
            e_id = flask.request.form['idToRemove']
            e_id = int(e_id)
            ifIdCorrect = 0
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipment")
            rows = cursor.fetchall()
            print "przed forem"
            for row in rows:
                print row[0]
                if e_id == row[0]:
                    print e_id
                    ifIdCorrect = 1
            if ifIdCorrect == 1:
                print "Id poprawne"
                mysqlCmd = "DELETE FROM `equipment` WHERE `e_id`='"+str(e_id)+"';"
                print "mysqlCmd: "+mysqlCmd
                cursor.execute(mysqlCmd)
            else:
                print "Id niepoprawne"
        elif 'listOfEquipment' in flask.request.form:
            EncodedListOfEquipment =[]
            ListOfEquipment = listEquipment()
            for index in range(0,len(ListOfEquipment)):
                encoded = "ID:"
                encoded+=str(ListOfEquipment[index][0])
                encoded+=' '
                encoded+=(ListOfEquipment[index][1].encode('utf8'))
                encoded+=' '
                encoded+=(ListOfEquipment[index][2].encode('utf8'))
                encoded+=' '
                encoded+=(ListOfEquipment[index][3].encode('utf8'))
                encoded+=' '
                if ListOfEquipment[index][4] == 1:
                    encoded+='status: dostepny'
                elif ListOfEquipment[index][4] == 0:
                    encoded+='status: niedostepny'
                EncodedListOfEquipment.append(encoded)
                print encoded
            print EncodedListOfEquipment
            for index in range(len(EncodedListOfEquipment)):
                flask.flash(EncodedListOfEquipment[index])
        return flask.redirect(flask.url_for('equipment'))

class Orders(flask.views.MethodView):
    def get(self):
        return flask.render_template('orders.html')
    def post(self):
        if 'RentEquipment' in  flask.request.form:
            year = flask.request.form['year']
            month = flask.request.form['month']
            day = flask.request.form['day']
            user_id = flask.request.form['user_id']
            equipment_id = flask.request.form['equipment_id']
            RentEquipment(year,month,day,user_id,equipment_id)
        elif 'listOfOrders' in  flask.request.form:
            EncodedListOfOrders =[]
            ListOfOrders = listOrders()
            for index in range(0,len(ListOfOrders)):
                encoded = "Order Id:"
                encoded+=str(ListOfOrders[index][0])
                encoded+=' User Id: '
                encoded+=str(ListOfOrders[index][1])
                encoded+='   Equipment Id:'
                encoded+=str(ListOfOrders[index][2])
                encoded+='   Date start:'
                encoded+=str(ListOfOrders[index][3])
                encoded+='   Date end:'
                encoded+=str(ListOfOrders[index][4])
                encoded+='   Charge:'
                encoded+=str(ListOfOrders[index][5])
                EncodedListOfOrders.append(encoded)
                print encoded
            print EncodedListOfOrders
            for index in range(len(EncodedListOfOrders)):
                flask.flash(EncodedListOfOrders[index])
        return flask.render_template('orders.html')

@app.route('/applogin', methods=['POST'])
def logowanie():
    login =  flask.request.form['login']
    password = flask.request.form['password']
    result = "Zwracam "
    result += login
    result += password
    return result
app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/add/',
                 view_func=Add.as_view('add'),
                 methods=["GET","POST"])
app.add_url_rule('/equipment/',
                 view_func=Equipment.as_view('equipment'),
                 methods=["GET","POST"])
app.add_url_rule('/orders/',
                 view_func=Orders.as_view('orders'),
                 methods=["GET","POST"])
app.debug = True
app.run('192.166.218.153')
