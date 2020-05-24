from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)
webapp.config['DEBUG'] = True

@webapp.route('/members_browse')
#the name of this function is just a cosmetic thing
def browse_members():
        db_connection = connect_to_database()
        print("Fetching and rendering members web page")
        query = 'SELECT * FROM Members;'

        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('members_browse.html', rows=result)

@webapp.route('/members_add', methods=['POST','GET'])
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

@webapp.route('/reservations_browse')
def browse_reservations():
    print("Fetching and rendering reservations web page")
    db_connection = connect_to_database()
    query = ''' SELECT r.reservationID, r.memberID, m.memberFirst, m.memberLast, b.title, r.bookID, r.dateIssued, r.dateDue, (SELECT IF(isReturned, \'Yes\', \'No\')) FROM Reservations AS r 
		LEFT JOIN Members AS m ON r.memberID=m.memberID 
		LEFT JOIN Book_Items AS bi ON r.bookID=bi.bookID 
		LEFT JOIN Books AS b ON bi.isbn=b.isbn; '''

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('reservations_browse.html', rows=result)

@webapp.route('/reservations_add', methods=['POST', 'GET'])
def add_reservations():
    db_connection = connect_to_database()

    if request.method == 'GET':
        return render_template('reservations_add.html')

    elif request.method == 'POST':
        memberFirst = request.form['memberFirst']
        memberLast = request.form['memberLast']
        isbn = request.form['isbn']
        dateIssued = request.form['dateIssued']
        dateDue = request.form['dateDue']
        isReturned = request.form['isReturned']

        query = ''' INSERT INTO Reservations (memberID, bookID, dateIssued, dateDue, isReturned) VALUES 
			((SELECT memberID FROM Members WHERE memberFirst=%s AND memberLast=%s),
		 	 (SELECT bi.bookID FROM Book_Items AS bi LEFT JOIN Books AS b ON bi.isbn=b.isbn WHERE b.isbn = %s),
		 	 %s,%s,%s) '''
        data = (memberFirst, memberLast, isbn, dateIssued, dateDue, isReturned)
        execute_query(db_connection, query, data)

        return render_template('reservations_add.html')

#
# Need to fix page re-direction after delete
#

@webapp.route('/reservations_browse/<int:id>')
#the name of this function is just a cosmetic thing
def delete_reservations(id):
        db_connection = connect_to_database()
        query = "DELETE FROM Reservations WHERE reservationID = %s"
        data = (id,)

        result = execute_query(db_connection, query, data)
        return browse_reservations()

@webapp.route('/authors.html')
#the name of this function is just a cosmetic thing
def browse_authors():
    print("Fetching and rendering authors web page")
    db_connection = connect_to_database()
    query = 'SELECT a.authorID, a.authorFirst, a.authorLast FROM Authors AS a;'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('authors.html', rows=result)

@webapp.route('/authors_add.html', methods=['POST','GET'])
def add_authors():
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

@webapp.route('/books.html')
#the name of this function is just a cosmetic thing
def browse_books():
    print("Fetching and rendering books web page")
    db_connection = connect_to_database()
    query = ''' SELECT b.isbn, b.title, GROUP_CONCAT(DISTINCT a.authorFirst, ' ', a.authorLast) AS authorName, b.genre, b.isFiction FROM Authors AS a 
		INNER JOIN Author_Book AS ab ON ab.authorID=a.authorID 
		INNER JOIN Books AS b ON ab.isbn=b.isbn 
		GROUP BY b.title ORDER BY a.authorFirst, a.authorLast; '''
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('books.html', rows=result)

@webapp.route('/books_add.html', methods=['POST','GET'])
def add_books():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT id, name from Authors'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('books_add.html', author = result)
    elif request.method == 'POST':
        bookTitle = request.form['bookTitle']
#       bookAuthor = request.form['bookAuthor']
        bookGenre= request.form['bookGenre']
        bookFiction= request.form['bookFiction']
        bookIsbn= request.form['bookIsbn']

        query = 'INSERT INTO Books (bookTitle, bookGenre, bookFiction, bookIsbn) VALUES (%s,%s,%s,%s)'
        data = (bookTitle, bookGenre, bookFiction, bookIsbn)
        execute_query(db_connection, query, data)
        return render_template('books_add.html')

# Library landing page
@webapp.route('/')
def index():
    return render_template('index.html')
