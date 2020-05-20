from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)
webapp.config['DEBUG'] = True

# EXAMPLE: 
# provide a route where requests on the web application can be addressed
# @webapp.route('/hello')
# provide a view (fancy name for a function) which responds to any requests on this route
# def hello():
#    return "Hello World!"
#

@webapp.route('/members_browse.html')
#the name of this function is just a cosmetic thing
def browse_members():
    print("Fetching and rendering members web page")
    db_connection = connect_to_database()
    query = 'SELECT * FROM Members;'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('members_browse.html', rows=result)

@webapp.route('/members_add', methods=['POST','GET'])
def add_new_people():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('people_add_new.html', planets = result)
    elif request.method == 'POST':
        print("Add new people!")
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
        data = (fname, lname, age, homeworld)
        execute_query(db_connection, query, data)
        return ('Person added!')

@webapp.route('/authors.html')
#the name of this function is just a cosmetic thing
def browse_members():
    print("Fetching and rendering authors web page")
    db_connection = connect_to_database()
    query = 'SELECT * FROM Authors;'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('authors.html', rows=result)

@webapp.route('/authors_add', methods=['POST','GET'])
def add_new_people():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT id, name from Authors'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('authors_add.html', author = result)
    elif request.method == 'POST':
        print("Add new people!")
        authorFirst = request.form['authorFirst']
        authorLast = request.form['authorLast']

        query = 'INSERT INTO Authors (authorFirst, authorLast) VALUES (%s,%s)'
        data = (authorFirst, authorLast)
        execute_query(db_connection, query, data)
        return ('Author added!')
@webapp.route('/authors.html')
#the name of this function is just a cosmetic thing
def browse_members():
    print("Fetching and rendering authors web page")
    db_connection = connect_to_database()
    query = 'SELECT * FROM Books;'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('books.html', rows=result)

@webapp.route('/books_add', methods=['POST','GET'])
def add_new_people():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT id, name from Authors'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('books_add.html', author = result)
    elif request.method == 'POST':
        print("Add new people!")
        authorFirst = request.form['authorFirst']
        authorLast = request.form['authorLast']

        query = 'INSERT INTO Books (author, genre, isFiction, isbn) VALUES (%s,%s)'
        data = (author, genre, isFiction, isbn)
        execute_query(db_connection, query, data)
        return ('Book added!')

# Library landing page
@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/home')
def home():
    db_connection = connect_to_database()
    query = "DROP TABLE IF EXISTS diagnostic;"
    execute_query(db_connection, query)
    query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
    execute_query(db_connection, query)
    query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
    execute_query(db_connection, query)
    query = "SELECT * from diagnostic;"
    result = execute_query(db_connection, query)
    for r in result:
        print(f"{r[0]}, {r[1]}")
    return render_template('home.html', result = result)

@webapp.route('/db_test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from bsg_people;"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)

#display update form and process any updates, using the same function
@webapp.route('/update_people/<int:id>', methods=['POST','GET'])
def update_people(id):
    print('In the function')
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        people_query = 'SELECT id, fname, lname, homeworld, age from bsg_people WHERE id = %s'  % (id)
        people_result = execute_query(db_connection, people_query).fetchone()

        if people_result == None:
            return "No such person found!"

        planets_query = 'SELECT id, name from bsg_planets'
        planets_results = execute_query(db_connection, planets_query).fetchall()

        print('Returning')
        return render_template('people_update.html', planets = planets_results, person = people_result)
    elif request.method == 'POST':
        print('The POST request')
        character_id = request.form['character_id']
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE id = %s"
        data = (fname, lname, age, homeworld, character_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_bsg_people')

@webapp.route('/delete_people/<int:id>')
def delete_people(id):
    '''deletes a person with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM bsg_people WHERE id = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return (str(result.rowcount) + "row deleted")
