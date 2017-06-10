import flask
from flask import Flask
from flask import g, request, render_template
import datetime
import flask, flask_mysqldb, flask.views, linecache, os, functools, json, ConfigParser, werkzeug, collections
from flask import g, request, render_template, jsonify
from datetime import datetime
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
    elif 'goShop' in flask.request.form:
        print "tmp"
        return flask.render_template('equipment.html')

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
    #wstawka
    mysqlCmd = "UPDATE `equipment` SET `e_status` = 0 WHERE `e_id` = "+str(equipment_id)
    print mysqlCmd
    cursor.execute(mysqlCmd)
    #koniec wstawki
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

def GetDateStart(e_id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT o_date_start FROM orders WHERE e_id='"+str(e_id)+"'and o_charge is NULL;")
    rows = cursor.fetchall()
    return str(rows)

def calcDays(start_date, stop_date):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    stop = datetime.strptime(stop_date, date_format)
    delta = stop - start
    return delta.days

def UpdateCharge(o_charge,o_date_end,e_id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("UPDATE `orders` SET `o_date_end`='"+str(o_date_end)+"',`o_charge`='"+str(o_charge)+"' WHERE `e_id`='"+str(e_id)+"' and o_charge is NULL;")
    rows = cursor.fetchall()
    #wstawka
    mysqlCmd = "UPDATE `equipment` SET `e_status` = 1 WHERE `e_id` = "+str(e_id)
    print mysqlCmd
    cursor.execute(mysqlCmd)
    #koniec wstawki
    return str(rows)

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
    def post(self):
        logowanie()
        if 'wypozycz' in flask.request.form:
            print "przejdz do sklepu dziala"
        print 'redirect page!!!'
        if 'listOfEquipment' in flask.request.form:
            print "w Przejdz do sklepu"
            flask.redirect(flask.url_for('equipment'))
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
        if 'RentEquipment' in flask.request.form:
            year = flask.request.form['year']
            month = flask.request.form['month']
            day = flask.request.form['day']
            user_id = flask.request.form['user_id']
            equipment_id = flask.request.form['equipment_id']
            RentEquipment(year,month,day,user_id,equipment_id)
        elif 'ReturnEquipment' in flask.request.form:
            print 'kliknieto ReturnEquipment button'
            equipment_id = flask.request.form['return_eq']
            year = flask.request.form['year']
            month = flask.request.form['month']
            day = flask.request.form['day']
            dateStart = GetDateStart(equipment_id)
            dateStart = dateStart[16:26].replace(",","-").replace(" ","")
            print dateStart
            dateEnd = ""+str(year)+"-"+str(month)+"-"+str(day)+""
            print dateEnd
            dayRent=(calcDays(dateStart, dateEnd))
            print dayRent
            charge = dayRent *10
            print charge
            UpdateCharge(charge,dateEnd,equipment_id)
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
def logowanieAplikacja():
    login =  flask.request.form['login']
    password = flask.request.form['password']
    ifLoginProperly = 0
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if login == row[1] and password == row[2]:
            flask.session['username'] = login
            ifLoginProperly = 1
    if ifLoginProperly == 0:
        print "error"
        return "error"
    print "ok"
    return "ok"

@app.route('/appshowequipment', methods=['POST'])
def appshowequipment():
    listOfEquipment = listEquipment()
    records = []
    for equipment in listOfEquipment:
        dictionary = collections.OrderedDict()
        dictionary['e_id'] = equipment[0]
        dictionary['e_type'] = str(equipment[1])
        dictionary['e_brand'] = str(equipment[2])
        dictionary['e_prod_year'] = str(equipment[3])
        dictionary['e_status'] = equipment[4]
        records.append(dictionary)
    return jsonify({"wyswietl":records})

@app.route('/apprentequipment', methods=['POST'])
def apprentequipment():
    year = flask.request.form['year']
    month = flask.request.form['month']
    day = flask.request.form['day']
    user_id = flask.request.form['user_id']
    equipment_id = flask.request.form['equipment_id']
    RentEquipment(year,month,day,user_id,equipment_id)
    return "done"

@app.route('/appreturnequipment', methods=['POST'])
def appreturnequipment():
    year = flask.request.form['year']
    month = flask.request.form['month']
    day = flask.request.form['day']
    user_id = flask.request.form['user_id']
    equipment_id = flask.request.form['equipment_id']
    print "app1"
    dateStart = GetDateStart(equipment_id)
    print dateStart
    dateStart = dateStart[16:26].replace(",","-").replace(" ","")
    dateEnd = ""+str(year)+"-"+str(month)+"-"+str(day)+""
    print "app2"
    print dateEnd
    dayRent=(calcDays(dateStart, dateEnd))
    charge = dayRent *10
    UpdateCharge(charge,dateEnd,equipment_id)
    return "done"

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
