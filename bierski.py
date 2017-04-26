import flask
from flask import Flask
from flask import g, request, render_template

import flask, flask.views, linecache, os, functools, json, ConfigParser, werkzeug, collections
from flask import g, request, render_template, jsonify

app = Flask(__name__)
app.secret_key = "123"

########################################### DATABASE CONNETION ############################################


config = ConfigParser.SafeConfigParser()
config.read('/home/BierSki/config.ini')
app.config['MYSQL_MYSQL_USER'] = config.get('KEY', 'user')
app.config['MYSQL_PASSWORD'] = config.get('KEY', 'password')
app.config['MYSQL_DB'] = config.get('KEY', 'database')
app.config['MYSQL_HOST'] = config.get('KEY', 'host')
mysql = MySQL(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR']


# @app.route('/')
# def hello_world():
#     return flask.render_template('index.html')

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        ifLoginProperly = 0
        username = flask.request.form['username']
        password = flask.request.form['password']
        if username == 'admin' and password == 'admin':
            flask.session['username'] = username
            ifLoginProperly =1
        if ifLoginProperly == 0:
            flask.flash("Login lub haslo bledne")
        if 'gosc' in flask.request.form:
            print 'Proba logowania jako gosc'

        return flask.redirect(flask.url_for('index'))

app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["GET", "POST"])

app.debug = True
app.run()
