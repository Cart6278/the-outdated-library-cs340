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
			query += ' order by memberid asc;'
		elif option == 'id_desc':
			query += ' order by memberid desc;'
		elif option == 'first_asc':
			query += ' order by memberfirst asc;'
		elif option == 'first_desc':
			query += ' order by memberfirst desc;'
		elif option == 'last_asc':
			query += ' order by memberlast asc;'
		elif option == 'first_asc':
			query += ' ORDER BY memberLast DESC;'
	elif request.method == 'GET':
		option = request.args.get('search_content')
	
		if option is None or option == '':	
			query += ';'
		else:
			query += ''' WHERE memberFirst LIKE %s ''' % ("\'%%" + option + "%%\'")
			query += ''' OR memberLast LIKE %s;''' % ("\'%%" + option + "%%\'")

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
		option = request.args.get('search_content')
	
		if option is None or option == '':	
			query += ';'
		else:
			query += ''' WHERE memberFirst LIKE %s ''' % ("\'%%" + option + "%%\'")
			query += ''' OR memberLast LIKE %s;''' % ("\'%%" + option + "%%\'")


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
def delete_reservations(id):
        db_connection = connect_to_database()
        query = "DELETE FROM Reservations WHERE reservationID = %s"
        data = (id,)

        result = execute_query(db_connection, query, data)
        return browse_reservations()

@webapp.route('/authors_browse', methods=['POST', 'GET'])
def browse_authors():
    db_connection = connect_to_database()
    query = ''' SELECT authorID, authorFirst, authorLast FROM Authors  '''

    if request.method == 'POST':
        option = request.form['type']

        if option == 'a_id_asc':
           query += ' ORDER BY authorID ASC;'
        elif option == 'a_id_desc':
           query += ' ORDER BY authorId DESC;'
        elif option == 'first_nam_asc':
            query += ' ORDER BY authorFirst ASC;'
        elif option == 'first_nam_desc':
           query += ' ORDER BY authorFirst DESC;'
        elif option == 'last_nam_asc':
            query += ' ORDER BY authorLast ASC;'
        elif option == 'last_nam_desc':
            query += ' ORDER BY authorLast DESC;'

    elif request.method == 'GET':
        query += ';'

    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('authors_browse.html', rows=result)

@webapp.route('/authors_add', methods=['POST','GET'])
def add_authors():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('authors_add.html')

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        query = 'INSERT INTO Authors (authorFirst, authorLast) VALUES (%s,%s);'
        data = (first_name, last_name)
        execute_query(db_connection, query, data)
        return render_template('authors_add.html')

@webapp.route('/books_browse', methods=['GET', 'POST'])
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
		INNER JOIN Books AS b ON ab.isbn=b.isbn'''

    # drop down menu for Book title sorting
    if request.method == 'POST':
        option = request.form['type']
        if option == 'title_asc':
            query += ' GROUP BY b.title ORDER BY b.title ASC;'
        elif option == 'title_dec':
            query += ' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'biography':
            query += ' WHERE b.genre=\'Biography\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'classics':
            query += ' WHERE b.genre=\'Classics\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'comics':
            query += ' WHERE b.genre=\'Comics/Graphic Novel\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'contemporary':
            query += ' WHERE b.genre=\'Contemporary\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'essay':
            query += ' WHERE b.genre=\'Essay\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'fffTale':
            query += ' WHERE b.genre=\'Fable/FolkTale/Fairy Tale\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'fantasy':
            query += ' WHERE b.genre=\'Fantasy\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'histFic':
            query += ' WHERE b.genre=\'Historical Fiction\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'horror':
            query += ' WHERE b.genre=\'Horror\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'humor':
            query += ' WHERE b.genre=\'Humor\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'journalism':
            query += ' WHERE b.genre=\'Journalism\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'legendMyth':
            query += ' WHERE b.genre=\'Legend/Mythology\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'mystery':
            query += ' WHERE b.genre=\'Mystery\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'reference':
            query += ' WHERE b.genre=\'Reference Book\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'romance':
            query += ' WHERE b.genre=\'Romance\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'sciFi':
            query += ' WHERE b.genre=\'Science Fiction\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'selfHelp':
            query += ' WHERE b.genre=\'Self-Help\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'short-story':
            query += ' WHERE b.genre=\'Short Story\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'suspenseThriller':
            query += ' WHERE b.genre=\'Suspense/Thriller\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'textbook':
            query += ' WHERE b.genre=\'Textbook\' GROUP BY b.title ORDER BY b.title DESC;'
        elif option == 'poems':
            query += '  WHERE b.genre=\'Poems\' GROUP BY b.title ORDER BY b.title DESC;'
    elif request.method == 'GET':
        query += ' GROUP BY b.title ORDER BY b.title ASC;'
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('books_browse.html', rows=result)

@webapp.route('/books_add', methods=['POST','GET'])
def add_books():
    db_connection = connect_to_database()
    if request.method == 'GET':
        return render_template('books_add.html')

    elif request.method == 'POST':
        bookTitle = request.form['bookTitle']
#       bookAuthor = request.form['bookAuthor']
        bookGenre = request.form['bookGenre']
        bookFiction = request.form['bookFiction']
        bookIsbn = request.form['bookIsbn']

        query = 'INSERT INTO Books (bookTitle, bookGenre, bookFiction, bookIsbn) VALUES (%s,%s,%s,%s)'
        data = (bookTitle, bookGenre, bookFiction, bookIsbn)
        execute_query(db_connection, query, data)
        return render_template('books_add.html')

# Library landing page
@webapp.route('/')
@webapp.route('/index')
def index():
    return render_template('index.html')
