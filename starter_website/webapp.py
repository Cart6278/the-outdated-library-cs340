from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)
webapp.config['DEBUG'] = True

@webapp.route('/members_browse', methods=['GET', 'POST'])
def browse_members():
	db_connection = connect_to_database()
	query = ''' SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IFNULL(email, '') as email FROM Members'''

	if request.method == 'POST':
		option = request.form['type']
	
		if option == 'id_asc':
			query += ' ORDER BY memberID ASC;'
		elif option == 'id_desc':
			query += ' ORDER BY memberID DESC;'
		elif option == 'first_asc':
			query += ' ORDER BY memberFirst ASC;'
		elif option == 'first_desc':
			query += ' ORDER BY memberFirst DESC;'
		elif option == 'last_asc':
			query += ' ORDER BY memberLast ASC;'
		elif option == 'first_asc':
			query += ' ORDER BY memberLast DESC;'

	elif request.method == 'GET':
		query += ';'

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

@webapp.route('/reservations_browse', methods=['POST', 'GET'])
def browse_reservations():
	db_connection = connect_to_database()

	query = ''' SELECT DISTINCT r.reservationID, r.memberID, m.memberFirst, m.memberLast, b.title, r.bookID, r.dateIssued, r.dateDue, (SELECT IF(isReturned, \'Yes\', \'No\')) FROM Reservations AS r 
		LEFT JOIN Members AS m ON r.memberID=m.memberID 
		LEFT JOIN Book_Items AS bi ON r.bookID=bi.bookID 
		LEFT JOIN Books AS b ON bi.isbn=b.isbn '''

	if request.method == 'POST':
		option = request.form['type']
	
		if option == 'first_asc':
			query += ' ORDER BY memberFirst ASC;'
		elif option == 'first_desc':
			query += ' ORDER BY memberFirst DESC;'
		elif option == 'last_asc':
			query += ' ORDER BY memberLast ASC;'
		elif option == 'last_desc':
			query += ' ORDER BY memberLast DESC;'
		elif option == 'issued_asc':
			query += ' ORDER BY dateIssued ASC;'
		elif option == 'issued_desc':
			query += ' ORDER BY dateIssued DESC;'
		elif option == 'due_asc':
			query += ' ORDER BY dateDue ASC;'
		elif option == 'due_desc':
			query += ' ORDER BY dateDue DESC;'
		elif option == 'returned':
			query += ' ORDER BY isReturned ASC;'
		elif option == 'not_returned':
			query += ' ORDER BY isReturned DESC;'
	
	elif request.method == 'GET':
		query += ';'

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

@webapp.route('/authors', methods = ['GET', 'POST'])
def browse_authors():
    db_connection = connect_to_database()
    query = ''' SELECT authorID, authorFirst, authorLast FROM Authors'''

    if request.method == 'POST':
        option = request.form['type']

        if option == 'a_id_asc':
            query += ' ORDER BY authorID ASC;'
        elif option == 'a_id_dec':
            query += ' ORDER BY authorId DESC;'
        elif option == 'first_nam_asc':
            query += ' ORDER BY authorFirst ASC;'
        elif option == 'first_nam_dec':
            query += ' ORDER BY authorFirst DESC;'
        elif option == 'last_nam_asc':
            query += ' ORDER BY authorLast ASC;'
        elif option == 'last_nam_dec':
            query += ' ORDER BY authorLast DESC;'

    elif request.method == 'GET':
        query += ';'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('authors.html', rows=result)

@webapp.route('/authors_add', methods=['POST','GET'])
def add_authors():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('authors_add.html')

    elif request.method == 'POST':
        print("Add new people!")
        authorFirst = request.form['authorFirst']
        authorLast = request.form['authorLast']

        query = 'INSERT INTO Authors (authorFirst, authorLast) VALUES (%s,%s);'
        data = (authorFirst, authorLast)
        execute_query(db_connection, query, data)
        return ('Author added!')

@webapp.route('/books', methods=['GET', 'POST'])
#the name of this function is just a cosmetic thing
def browse_books():
    print("Fetching and rendering books web page")
    db_connection = connect_to_database()
    # THIS CODE WORKS -- query = ''' SELECT b.isbn, b.title, GROUP_CONCAT(DISTINCT a.authorFirst, ' ', a.authorLast) AS authorName, b.genre, b.isFiction FROM Authors AS a
	#	INNER JOIN Author_Book AS ab ON ab.authorID=a.authorID
	#	INNER JOIN Books AS b ON ab.isbn=b.isbn
	#	GROUP BY b.title ORDER BY a.authorFirst, a.authorLast; '''

    query = ''' SELECT b.isbn, b.title, GROUP_CONCAT(DISTINCT a.authorFirst, ' ', a.authorLast) AS authorName, b.genre, b.isFiction FROM Authors AS a 
		INNER JOIN Author_Book AS ab ON ab.authorID=a.authorID 
		INNER JOIN Books AS b ON ab.isbn=b.isbn 
		GROUP BY b.title'''

    # drop down menu for Book title sorting
    if request.method == 'POST':
        option = request.form['type']
        if option == 'title_asc':
            query += ' ORDER BY title ASC;'
        elif option == 'title_dec':
            query += ' ORDER BY title DESC;'
    elif request.method == 'GET':
        query += ' ORDER BY a.authorFirst, a.authorLast;'
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('books.html', rows=result)

@webapp.route('/books_add', methods=['POST','GET'])
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
