#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from flask_table import Table, Col


class ResultsPerson(Table):
  person_id = Col('PersonID')
  p_name = Col('Name')
  address = Col('Address')

class ResultsBuyer(Table):
  person_id = Col('ID')
  p_name = Col('Name')
  address = Col('Address')
  account_balance = Col('Account Balance')

class ResultsSeller(Table):
  person_id = Col('ID')
  p_name = Col('Name')
  address = Col('Address')
  deposit = Col('Deposit')


class ResultsOrder(Table):
  order_id = Col('OrderID')
  total_cost = Col('Cost')
  quantity = Col('Quantity')

class ResultsProduct(Table):
  product_id = Col('ProductID')
  price = Col('Price')
  brand = Col('Brand')
  name = Col('Product Name')

class ResultsCat(Table):
  category_id = Col('CategoryID')
  name = Col('Name')
class ResultsShoppingCart(Table):
  cart_id = Col('CartID')

class ResultsQueryOne(Table):
  name = Col('Category Name')
class ResultsQueryTwo(Table):
  name = Col('Product Name')

class ResultQueryThree(Table):
  summation =  Col('Total Price')
class ResultQueryFour(Table):
  name =  Col('Product Name')

class ResultQueryFive(Table):
  name = Col('Buyer Name')
  cost = Col('Total Cost')


class ResultQuerySix(Table):
  count = Col('Popularity')

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
DATABASEURI = "postgresql://zq2172:12345678@34.74.165.156/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""""")
# engine.execute("""""")


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
    import traceback; traceback.print_exc()
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
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like


  data = [
    {
      'name': 'Audrin',
      'place': 'kaka',
      'mob': '7736'
    },
    {
      'name': 'Stuvard',
      'place': 'Goa',
      'mob': '546464'
    }
  ]

  productList = query_one()
  sellerNameList = query_two()
  buyerNameList = query_three()
  orderList = query_five()
  categoryList = query_six()
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  return render_template("index.html", queryOne=productList, queryTwo = sellerNameList, queryThree = buyerNameList, queryFour = buyerNameList, queryFive = orderList, querySix = categoryList)

def query_one():
  cursor = g.conn.execute("SELECT name FROM product")
  products = cursor.fetchall()
  productList = []

  for p in products:
    productList.append({"productName" : p[0]})
  return productList

def query_two():
  cursor = g.conn.execute("SELECT p_name FROM seller")
  names = cursor.fetchall()
  nameList = []

  for p in names:
    nameList.append({"sellerName" : p[0]})
  return nameList

def query_three():
  cursor = g.conn.execute("SELECT p_name FROM buyer")
  names = cursor.fetchall()
  nameList = []

  for p in names:
    nameList.append({"buyerName" : p[0]})
  return nameList

def query_five():
  cursor = g.conn.execute("SELECT count(*) FROM \"order\"")
  count = cursor.fetchone()[0]
  countList = []
  for p in range(count):
    countList.append({"count" : p+1})
  return countList
def query_six():
  cursor = g.conn.execute("SELECT name FROM categories")
  catName = cursor.fetchall()
  catNameList = []
  for p in catName:
    catNameList.append({"category" : p[0]})
  return catNameList
#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#


@app.route('/result', methods = ['POST'])
def search_results():
  results = []
  # search_string = search.data['search']
  #
  # if search.data['search'] == '':
  tableName = request.form['tablename']
  cursor = g.conn.execute("SELECT * FROM "+"\""+tableName+"\"")
  results = cursor.fetchall()
  if not results:
   # flash('No results found!')
    return redirect('/')
  else:
    # display results
    if tableName == "buyer":
      table = ResultsBuyer(results)
    elif tableName == "seller":
      table = ResultsSeller(results)
    elif tableName == "person":
      table = ResultsPerson(results)
    elif tableName == "order":
      table = ResultsOrder(results)
    elif tableName == "categories":
      table = ResultsCat(results)
    elif tableName == "product":
      table = ResultsProduct(results)
    else:
      table = ResultsShoppingCart(results)
    table.border = True
    return render_template('result.html', table=table)
# Example of adding new data to the database

@app.route('/queryOne', methods = ['POST'])
def search_queryOne():
  results = []
  pname = request.form['queryOne']
  queryString = "SELECT DISTINCT c.name FROM product p, belongs_to bt, categories c WHERE bt.product_id = p.product_id AND c.category_id = bt.category_id AND p.name LIKE " + "\'"+pname + "%\'"
  print(queryString)

  cursor = g.conn.execute(sqlalchemy.text(queryString))
  results = cursor.fetchall()
  if not results:
   # flash('No results found!')
    return redirect('/')
  else:
    # display results

    table = ResultsQueryOne(results)

    table.border = True
    return render_template('queryOne.html', table=table)
@app.route('/queryTwo', methods = ['POST'])
def search_queryTwo():

  sellerName = request.form['queryTwo']
  queryString = "SELECT distinct p.name FROM product p, seller ser, sells s WHERE p.product_id = s.product_id AND ser.person_id = s.person_id AND ser.p_name = "+"\'"+sellerName+"\'"
  print(queryString)

  cursor = g.conn.execute(sqlalchemy.text(queryString))
  results = cursor.fetchall()
  if not results:
   # flash('No results found!')
    return redirect('/')
  else:
    # display results

    table = ResultsQueryTwo(results)

    table.border = True
    return render_template('result.html', table=table)

@app.route('/queryThree', methods=['POST'])
def search_queryThree():

  buyerName = request.form['queryThree']
  queryString = "SELECT SUM(p.price * has.quantity) AS summation FROM shopping_cart sc, has, product p, owns, person per WHERE p.product_id = has.product_id AND sc.cart_id = has.cart_id AND owns.person_id = per.person_id AND owns.cart_id = sc.cart_id AND per.p_name = "+"\'"+buyerName+"\'"

  cursor = g.conn.execute(sqlalchemy.text(queryString))
  results = cursor.fetchall()
  if not results:
    # flash('No results found!')
    return redirect('/')
  else:
    # display results

    table = ResultQueryThree(results)
    table.border = True
    return render_template('result.html', table=table)

@app.route('/queryFour', methods=['POST'])
def search_queryFour():

  buyerName = request.form['queryFour']
  queryString = "SELECT p.name AS name FROM shopping_cart sc, has, product p, owns, person per WHERE p.product_id = has.product_id AND sc.cart_id = has.cart_id AND owns.person_id = per.person_id AND owns.cart_id = sc.cart_id AND per.p_name = "+"\'"+buyerName+"\'"

  cursor = g.conn.execute(sqlalchemy.text(queryString))
  results = cursor.fetchall()
  # if not results:
  #   # flash('No results found!')
  #   return redirect('/')
  # else:
    # display results

  table = ResultQueryFour(results)
  table.border = True
  return render_template('result.html', table=table)



@app.route('/queryFive', methods=['POST'])
def search_queryFive():

  rank = int(request.form['queryFive'])-1
  print(rank)
  queryString = "SELECT per.p_name as name, o.total_cost as cost FROM  person per, places pl, \"order\" o WHERE per.person_id = pl.person_id AND o.order_id = pl.order_id ORDER BY o.total_cost DESC LIMIT 1 OFFSET "+str(rank)

  cursor = g.conn.execute(sqlalchemy.text(queryString))
  results = cursor.fetchall()
  if not results:
    # flash('No results found!')
    return redirect('/')
  else:
    # display results

    table = ResultQueryFive(results)
    table.border = True
    return render_template('result.html', table=table)

@app.route('/querySix', methods=['POST'])
def search_querySix():

  catergoryName = request.form['querySix']

  queryString = "SELECT COUNT(c.order_id) FROM product p, \"contains\" c, \"order\" o, belongs_to bt, categories cat WHERE  c.product_id = p.product_id AND c.order_id = o.order_id AND bt.product_id = p.product_id AND cat.category_id = bt.category_id AND cat.name = "+"\'"+catergoryName+"\'"

  cursor = g.conn.execute(sqlalchemy.text(queryString))
  results = cursor.fetchall()
  if not results:
    # flash('No results found!')
    return redirect('/')
  else:
    # display results

    table = ResultQuerySix(results)
    table.border = True
    return render_template('result.html', table=table)
# Example of adding new data to the database

@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  #g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login')
def login():
    # abort(401)
    # this_is_never_executed()
    pass


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
