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

@webapp.route('/members_add.html', methods=['POST','GET'])
def add_members():
    db_connection = connect_to_database()

    if request.method == 'GET':
        return render_template('members_add.html')

    elif request.method == 'POST':
        memberFirst = request.form['memberFirst']
        memberLast = request.form['memberLast']
        streetAddr = request.form['streetAddr']
        city = request.form['city']
        state = request.form['state']
        postalCode = request.form['postalCode']
        phoneNum = request.form['phoneNum']
        email = request.form['email']

        query = 'INSERT INTO Members (memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        data = (memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, email)
        execute_query(db_connection, query, data)

        return render_template('members_add.html')

@webapp.route('/reservations_browse.html')
def browse_reservations():
    print("Fetching and rendering reservations web page")
    db_connection = connect_to_database()
    query = 'SELECT * FROM Reservations;'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('reservations_browse.html')



@webapp.route('/authors_add.html', methods=['POST','GET'])
def add_authors():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('authors_add.html')

    elif request.method == 'POST':
        authorFirst = request.form['authorFirst']
        authorLast = request.form['authorLast']

        query = 'INSERT INTO Authors (authorFirst, authorLast) VALUES (%s,%s)'
        data = (authorFirst, authorLast)
        execute_query(db_connection, query, data)
        return render_template('authors_add.html')

@webapp.route('/authors.html')
#the name of this function is just a cosmetic thing
def browse_authors():
    print("Fetching and rendering authors web page")
    db_connection = connect_to_database()
    query = 'SELECT * FROM Authors;'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('authors.html', rows=result)

@webapp.route('/books_add.html', methods=['POST','GET'])
def add_books():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('books_add.html')

    elif request.method == 'POST':
        bookTitle = request.form['bookTitle']
       # bookAuthor = request.form['bookAuthor']
        bookGenre= request.form['bookGenre']
        bookFiction= request.form['bookFiction']
        bookIsbn= request.form['bookIsbn']

        query = 'INSERT INTO Books (bookTitle, bookGenre, bookFiction, bookIsbn) VALUES (%s,%s,%s,%s,%s)'
        data = (bookTitle, bookGenre, bookFiction, bookIsbn)
        execute_query(db_connection, query, data)

        return render_template('books_add.html')

@webapp.route('/books.html')
#the name of this function is just a cosmetic thing
def browse_books():
    print("Fetching and rendering books web page")
    db_connection = connect_to_database()
    query = 'SELECT * FROM Books;'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('books.html', rows=result)

#  working on update for books to see how it works
@webapp.route('/update_book/<id>', methods=['POST', 'GET'])
def update_book(id):
    db_connection = connect_to_database()
    if request.method == 'GET':
        book_query = 'SELECT isbn, title, genre, isFiction FROM Books WHERE isbn = %s' % (id)
        book_result = execute_query(db_connection, book_query).fetchone()
        if book_result == None:
            return "No such book found!"
    #  find author for book
        return render_template(add_books.html, rows=book_result)
    elif request.method == 'POST':
        isbn=request.form['isbn']
        title=request.form['title']
        genre=request.form['genre']
        isFiction=request.form['isFiction']

        query = 'UPDATE Books SET title= %s, genre= %s, isFiction= %s WHERE isbn= %s'
        data = (title, genre, isFiction, isbn)
        result = execute_query(db_connection, query, data)

        return redirect('/books.html')

# Library landing page
@webapp.route('/')
def index():
    return render_template('index.html')
