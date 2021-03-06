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

	if request.method == 'GET':
		option = request.args.get('search_content')
	
		if option is None or option == '':	
			query += ';'
		else:
			query += ''' WHERE memberFirst LIKE %s ''' % ("\'%%" + option + "%%\'")
			query += ''' OR memberLast LIKE %s ''' % ("\'%%" + option + "%%\'")
			query += ''' OR (SELECT DISTINCT CONCAT(memberFirst, ' ', memberLast)) LIKE %s; ''' % ("\'%%" + option + "%%\'")

	elif request.method == 'POST':
		option2 = request.form['type']

		if option2 == 'id_asc':
			query += ' ORDER BY memberID ASC'
		elif option2 == 'id_desc':
			query += ' ORDER BY memberID DESC'
		elif option2 == 'first_asc':
			query2 += ' ORDER BY  memberFirst ASC'
		elif option2 == 'first_desc':
			query2 += ' ORDER BY memberFirst DESC'
		elif option2 == 'last_asc':
			query2 += ' ORDER BY memberLast ASC'
		elif option2 == 'first_asc':
			query += ' ORDER BY memberLast DESC'
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

@webapp.route('/members_update/<int:id>', methods=['POST','GET'])
def update_members(id):
	db_connection = connect_to_database()

	if request.method == 'GET':
		member_query = ''' SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IFNULL(email, '') as email FROM Members WHERE memberID = %s''' % (id)
		member_result = execute_query(db_connection, member_query).fetchone()
		return render_template('members_update.html', member = member_result)

	elif request.method == 'POST':
		memberID = request.form['memberID']
		memberFirst = request.form['memberFirst']
		memberLast = request.form['memberLast']
		streetAddr = request.form['streetAddr']
		city = request.form['city']
		state = request.form['state']
		postalCode = request.form['postalCode']
		phoneNum = request.form['phoneNum']
		email = request.form['email']

		query = 'UPDATE Members SET memberFirst = %s, memberLast = %s, streetAddr = %s, city = %s, state = %s, postalCode = %s, phoneNum = %s, email = %s WHERE memberID = %s'
		data = (memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, email, memberID)
		execute_query(db_connection, query, data)

		return redirect('/members_browse')

@webapp.route('/members_browse/<int:id>')
def delete_members(id):
	db_connection = connect_to_database()

	# Delete reservations associated with member ID before deleting member 
	query1 = "DELETE FROM Reservations WHERE memberID = %s;"
	query2 = "DELETE FROM Members WHERE memberID = %s;"

	data = (id,)
	execute_query(db_connection, query1, data)
	execute_query(db_connection, query2, data)

	return redirect('/members_browse') 

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
			query += ''' OR memberLast LIKE %s ''' % ("\'%%" + option + "%%\'")
			query += ''' OR (SELECT DISTINCT CONCAT(memberFirst, ' ', memberLast)) LIKE %s; ''' % ("\'%%" + option + "%%\'")


	result = execute_query(db_connection, query).fetchall()
	print(result)
	return render_template('reservations_browse.html', rows=result)

@webapp.route('/reservations_add', methods=['POST', 'GET'])
def add_reservations():
	db_connection = connect_to_database()

	if request.method == 'GET':
		query = "SELECT memberID, memberFirst, memberLast FROM Members;"
		result = execute_query(db_connection, query).fetchall()
		return render_template('reservations_add.html', members = result)

	elif request.method == 'POST':
		memberID = request.form['memberID']
		isbn = request.form['isbn']
		dateIssued = request.form['dateIssued']
		dateDue = request.form['dateDue']
		isReturned = request.form['isReturned']

	# Error handle	
	try:
		query = ''' INSERT INTO Reservations (memberID, bookID, dateIssued, dateDue, isReturned) VALUES 
				(%s,
				 (SELECT bi.bookID FROM Book_Items AS bi LEFT JOIN Books AS b ON bi.isbn=b.isbn WHERE b.isbn = %s),
				 %s,%s,%s) '''
		data = (memberID, isbn, dateIssued, dateDue, isReturned)

		execute_query(db_connection, query, data)

	except:
		print("Invalid reservation input")	

	query = "SELECT memberID, memberFirst, memberLast FROM Members;"
	result = execute_query(db_connection, query).fetchall()
	return render_template('reservations_add.html', members = result)

@webapp.route('/reservations_update/<int:id>', methods=['POST', 'GET'])
def update_reservations(id):
	db_connection = connect_to_database()

	if request.method == 'GET':
		reservation_query = ''' SELECT DISTINCT r.reservationID, m.memberFirst, m.memberLast, b.isbn, r.dateIssued, r.dateDue, (SELECT IF(isReturned, \'Yes\', \'No\')) FROM Reservations AS r 
		LEFT JOIN Members AS m ON r.memberID=m.memberID 
		LEFT JOIN Book_Items AS bi ON r.bookID=bi.bookID 
		LEFT JOIN Books AS b ON bi.isbn=b.isbn
		WHERE reservationID = %s ''' % (id)

		reservation_result = execute_query(db_connection, reservation_query).fetchone()
		return render_template('reservations_update.html', reservation = reservation_result)

	elif request.method == 'POST':
		reservationID = request.form['reservationID']
		memberFirst = request.form['memberFirst']
		memberLast = request.form['memberLast']
		isbn = request.form['isbn']
		dateIssued = request.form['dateIssued']
		dateDue = request.form['dateDue']
		isReturned = request.form['isReturned']

		query = ''' UPDATE Reservations SET 
				memberID = (SELECT memberID FROM Members WHERE memberFirst = %s AND memberLast = %s), 
				bookID = (SELECT bi.bookID FROM Book_Items AS bi LEFT JOIN Books AS b ON bi.isbn=b.isbn WHERE bi.isbn = %s LIMIT 1),
				dateIssued = %s, dateDue = %s, isReturned = %s WHERE reservationID = %s ''' 

		data = (memberFirst, memberLast, isbn, dateIssued, dateDue, isReturned, reservationID)
		execute_query(db_connection, query, data)

		return redirect('/reservations_browse')

@webapp.route('/reservations_browse/<int:id>')
def delete_reservations(id):
        db_connection = connect_to_database()
        query = "DELETE FROM Reservations WHERE reservationID = %s"
        data = (id,)

        result = execute_query(db_connection, query, data)
        return redirect('/reservations_browse') 

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
        option = request.args.get('search_content')
        if option is None or option == '':
            query += ';'
        else:
            query += ''' WHERE authorFirst LIKE %s ''' % ("\'%%" + option + "%%\'")
            query += ''' OR authorLast LIKE %s ''' % ("\'%%" + option + "%%\'")
            query += ''' OR (SELECT DISTINCT CONCAT(authorFirst, ' ', authorLast)) LIKE %s; ''' % ("\'%%" + option + "%%\'")

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

        query = ''' INSERT INTO Authors (authorFirst, authorLast) SELECT * FROM (SELECT %s, %s) AS tmp
                WHERE NOT EXISTS (SELECT authorFirst, authorLast FROM Authors WHERE authorFirst = %s AND authorLast = %s) LIMIT 1;'''
        data = (first_name, last_name, first_name, last_name)
        execute_query(db_connection, query, data)
        return render_template('authors_add.html')

@webapp.route('/authors_update/<int:id>', methods=['POST', 'GET'])
def update_authors(id):
    db_connection = connect_to_database()

    if request.method == 'GET':
        author_query = ''' SELECT authorID, authorFirst, authorLast FROM Authors WHERE authorID=%s ''' % id
        authors_result = execute_query(db_connection, author_query).fetchone()
        return render_template('authors_update.html', authors = authors_result)

    elif request.method == 'POST':
        author_id = request.form['authorID']
        first_name = request.form['authorFirst']
        last_name = request.form['authorLast']

        query = ''' UPDATE Authors SET authorFirst = %s, authorLast=%s WHERE authorID=%s'''
        data = (first_name, last_name, author_id)
        execute_query(db_connection, query, data)
        return redirect('/authors_browse')

@webapp.route('/authors_browse/<int:id>')
def delete_author(id):
    db_connection = connect_to_database()
    query1 = "DELETE FROM Authors WHERE authorID = %s;"
    query2 = "DELETE FROM Author_Book WHERE authorID=%s;"
    data = (id,)

    execute_query(db_connection, query1, data)
    execute_query(db_connection, query2, data)

    return redirect('/authors_browse')


@webapp.route('/books_browse', methods=['GET', 'POST'])
def browse_books():
	print("Fetching and rendering books web page")
	db_connection = connect_to_database()

	query = ''' SELECT bi.isbn, b.title, GROUP_CONCAT(DISTINCT a.authorFirst, ' ', a.authorLast) AS authorName, b.genre, (SELECT IF(isFiction, \'Yes\', \'No\'))FROM Books AS b
		INNER JOIN Book_Items AS bi ON b.isbn=bi.isbn
		INNER JOIN Author_Book AS ab ON ab.ISBN=b.ISBN
		INNER JOIN Authors AS a ON ab.authorID=a.authorID '''

	# drop down menu for Book title sorting
	if request.method == 'POST':
		option = request.form['type']

		if option == 'title_asc':
			query += 'GROUP BY b.isbn ORDER BY b.title ASC;'
		elif option == 'title_dec':
			query += 'GROUP BY b.isbn ORDER BY b.title DESC;'
		else:
			query += 'WHERE b.genre=%s ' % ("\'" + option + "\'")
			query += 'GROUP BY b.isbn ORDER BY b.title ASC;'

	elif request.method == 'GET':
		option = request.args.get('search_content')

		if option is None or option == '':
		    query += 'GROUP BY b.isbn ORDER BY b.title ASC;'
		else:
		    query += ''' WHERE title LIKE %s ''' % ("\'%%" + option + "%%\'")
		    query += ''' OR genre LIKE %s ''' % ("\'%%" + option + "%%\'")
		    query += ''' OR authorFirst LIKE %s ''' % ("\'%%" + option + "%%\'")
		    query += ''' OR authorLast LIKE %s ''' % ("\'%%" + option + "%%\'")
		    query += ''' OR (SELECT DISTINCT CONCAT(authorFirst, ' ', authorLast)) LIKE %s ''' % ("\'%%" + option + "%%\'")
		    query += 'GROUP BY b.isbn ORDER BY b.title ASC;'

	result = execute_query(db_connection, query).fetchall()
	print(result)
	return render_template('books_browse.html', rows=result)

@webapp.route('/books_add', methods=['POST','GET'])
def add_books():
	db_connection = connect_to_database()
	if request.method == 'GET':
		return render_template('books_add.html')

	elif request.method == 'POST':
		try:
			bookTitle = request.form['book_title']
			bookGenre = request.form['book_genre']
			bookFiction = request.form['isFiction']
			bookIsbn = request.form['isbn']
			bookAuthorFirst = request.form['author_first']
			bookAuthorLast = request.form['author_last']
			second_author = request.form['second_author']
			bookAuthorFirst2 = request.form['author_first2']
			bookAuthorLast2 = request.form['author_last2']

			query1 = 'INSERT INTO Books (isbn, title, genre, isFiction) VALUES(%s, %s, %s, %s); '
			query2 = ''' INSERT INTO Authors (authorFirst, authorLast) SELECT * FROM (SELECT %s, %s) AS tmp
				WHERE NOT EXISTS (SELECT authorFirst, authorLast FROM Authors WHERE authorFirst = %s AND authorLast = %s) LIMIT 1;'''
			query3 = 'INSERT INTO Author_Book (authorID, isbn) VALUES ((SELECT a.authorID FROM Authors AS a WHERE a.authorFirst = %s AND a.authorLast = %s), %s)'
			query4 = 'INSERT INTO Book_Items (isbn) VALUES (%s)'

			data1 = (bookIsbn, bookTitle, bookGenre, bookFiction)
			data2 = (bookAuthorFirst, bookAuthorLast, bookAuthorFirst, bookAuthorLast,)
			data3 = (bookAuthorFirst, bookAuthorLast, bookIsbn,)
			data4 = (bookIsbn,)

			execute_query(db_connection, query1, data1)
			execute_query(db_connection, query2, data2)
			execute_query(db_connection, query3, data3)
			execute_query(db_connection, query4, data4)

			if second_author == 1:
			    query5 = ''' INSERT INTO Authors (authorFirst, authorLast) SELECT * FROM (SELECT %s, %s) AS tmp
				WHERE NOT EXISTS (SELECT authorFirst, authorLast FROM Authors WHERE authorFirst = %s AND authorLast = %s) LIMIT 1;'''
			    query6 = 'INSERT INTO Author_Book (authorID, isbn) VALUES ((SELECT a.authorID FROM Authors AS a WHERE a.authorFirst = %s AND a.authorLast = %s), %s)'
			    data5 = (bookAuthorFirst2, bookAuthorLast2, bookAuthorFirst2, bookAuthorLast2)
			    data6 = (bookAuthorFirst2, bookAuthorLast2, bookIsbn,)
			    execute_query(db_connection, query5, data5)
			    execute_query(db_connection, query6, data6)
		except:
			print("ISBN already exists in database.")
	    
	return render_template('books_add.html')

@webapp.route('/books_update/<int:id>', methods=['POST','GET'])
def update_books(id):
    db_connection = connect_to_database()

    if request.method == 'GET':
        book_query = ''' SELECT isbn, title, genre, isFiction FROM Books WHERE isbn= %s ''' % id
        book_result = execute_query(db_connection, book_query).fetchone()
        return render_template('books_update.html', book = book_result)
    elif request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        genre = request.form['genre']
        isFiction = request.form['isFiction']


        query = '''UPDATE Books SET title = %s, genre = %s, isFiction = %s WHERE isbn = %s'''
        data = (title, genre, isFiction, isbn)
        execute_query(db_connection, query, data)
        return redirect('/books_browse')

@webapp.route('/books_browse/<int:id>')
def delete_book(id):
    db_connection = connect_to_database()
    query1 = "DELETE FROM Books WHERE isbn = %s"
    query2 = "DELETE FROM Author_Book WHERE isbn = %s"
    query3 = "DELETE FROM Book_Items WHERE isbn = %s"
    data = (id,)

    execute_query(db_connection, query2, data)
    execute_query(db_connection, query3, data)
    execute_query(db_connection, query1, data)
    return redirect('/books_browse')


# Library landing page
@webapp.route('/')
@webapp.route('/index')
def index():
    return render_template('index.html')
