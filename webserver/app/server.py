"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
# accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import request, render_template, g, redirect, Response
from app import app

# Connects to our database
DATABASEURI = "postgresql://xl3082:646915@34.73.36.248/project1"

# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database,
# containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
    """
    request is a special object that Flask provides to access web request information:

    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

    See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
    """
    # DEBUG: this is debugging code to see what request looks like

    return render_template("index.html")


@app.route('/player')
def player():
    mycursor = g.conn.execute("SELECT * FROM player")
    data = mycursor.fetchall()
    return render_template("player.html", data=data)


@app.route('/team')
def team():
    mycursor = g.conn.execute("SELECT * FROM team")
    data = mycursor.fetchall()
    return render_template("team.html", data=data)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    # name = request.form['name']
    # g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
    return redirect('/')


# @app.route('/search', methods=['GET'])
# def search():
#     team = request.args.get('q')
#     print(team)
#     mycursor = g.conn.execute("SELECT * FROM team WHERE name='{}'".format(team))
#     data = mycursor.fetchall()
#     # name = request.form['name']
#     # g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#     return render_template('search.html', data=data)


@app.route('/profile', methods=['GET'])
def teampage():
    team = request.args.get('q')
    print(team)
    mycursor = g.conn.execute("SELECT * FROM team WHERE name='{}'".format(team))
    data = mycursor.fetchall()
    name = data[0][1]
    region = data[0][2]
    coach = data[0][3]
    seeding = data[0][4]
    print(data)
    return render_template("teampage.html", name=name, region=region, coach=coach, seeding=seeding)


@app.route('/login')
def login():
    # abort(401)
    # this_is_never_executed()
    return

