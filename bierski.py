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
    print 'Hakuna'
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

def listEquipment():
    listOfEquipment = []
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipment")
    rows = cursor.fetchall()
    for row in rows:
        listOfEquipment.append(row)
    return listOfEquipment

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
        elif 'removeEquipment' in flask.request.form:
            flask.flash("Funkcja w budowie")
            print "Metoda w budowie"
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

app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/add/',
                 view_func=Add.as_view('add'),
                 methods=["GET","POST"])
app.add_url_rule('/equipment/',
                 view_func=Equipment.as_view('equipment'),
                 methods=["GET","POST"])
app.debug = True
app.run('192.166.218.153')
