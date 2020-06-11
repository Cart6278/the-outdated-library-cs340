----
-- For all queries, ':' denotes a variable that will be filled out by the user or computed by the back-end
----

-- Query to get all Members for Browse Members page, with blank (NULL) e-mails replaced with empty string

SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IFNULL(email, '') as email FROM Members

-- Query to search through Members table using their first, last, or full name
-- This appended to the above query

WHERE memberFirst LIKE :memberFirstSearch
	OR memberLast LIKE :memberLastSearch
	OR (SELECT DISTINCT CONCAT(memberFirst, ' ', memberLast)) LIKE :memberFullSearch;

-- Queries to see all Members, sorted by selected option
-- These are appended to the first query to get all Members on members_browse.html

ORDER BY memberID ASC;
ORDER BY memberID DESC;
ORDER BY memberFirst ASC;
ORDER BY memberFirst DESC;
ORDER BY memberLast ASC;
ORDER BY memberLast DESC;

-- Query to get all Reservations for Browse Reservations page with boolean values shown as 'Yes' or 'No'

SELECT DISTINCT r.reservationID, r.memberID, m.memberFirst, m.memberLast, b.title, r.bookID, r.dateIssued, r.dateDue, (SELECT IF(isReturned, 'Yes', 'No')) FROM Reservations AS r 
		LEFT JOIN Members AS m ON r.memberID=m.memberID 
		LEFT JOIN Book_Items AS bi ON r.bookID=bi.bookID 
		LEFT JOIN Books AS b ON bi.isbn=b.isbn

-- Query to search through Reservations table using member's first, last, or full name
-- This is appended to the above query

WHERE memberFirst LIKE :memberFirstSearch
	OR memberLast LIKE :memberLastSearch
	OR (SELECT DISTINCT CONCAT(memberFirst, ' ', memberLast)) LIKE :memberFullSearch;

-- Queries to see all Reservations, sorted by selected option
-- These are appended to the first query to get all Reservations on reservations_browse.html

ORDER BY memberFirst ASC
ORDER BY memberFirst DESC;
ORDER BY memberLast ASC;
ORDER BY memberLast DESC;
ORDER BY dateIssued ASC;
ORDER BY dateIssued DESC;
ORDER BY dateDue ASC;
ORDER BY dateDue DESC;
ORDER BY isReturned ASC;
ORDER BY isReturned DESC;

-- Query to see all Authors

SELECT authorID, authorFirst, authorLast FROM Authors;

-- Query to search by author first, last, or full name

WHERE authorFirst LIKE :authorFirstSearch
	OR authorLast LIKE :authorLastSearch
	OR (SELECT DISTINCT CONCAT(authorFirst, ' ', authorLast)) LIKE :authorFullSearch;

-- Queries to sort all Authors

ORDER BY authorID ASC;
ORDER BY authorId DESC;
ORDER BY authorFirst ASC;
ORDER BY authorFirst DESC;
ORDER BY authorLast ASC;
ORDER BY authorLast DESC;

-- Query to see all Books

SELECT bi.isbn, b.title, GROUP_CONCAT(DISTINCT a.authorFirst, ' ', a.authorLast) AS authorName, b.genre, (SELECT IF(isFiction, 'Yes', 'No')) FROM Books AS b
		INNER JOIN Book_Items AS bi ON b.isbn=bi.isbn
		INNER JOIN Author_Book AS ab ON ab.ISBN=b.ISBN
		INNER JOIN Authors AS a ON ab.authorID=a.authorID;

-- Query to search Books

WHERE title LIKE :titleInput
	OR genre LIKE :genreInput
	OR authorFirst LIKE :authorFirstInput
	OR authorLast LIKE :authorLastInput
	OR (SELECT DISTINCT CONCAT(authorFirst, ' ', authorLast)) LIKE :authorFull
	GROUP BY b.isbn ORDER BY b.title ASC;

-- Queries to sort Books

GROUP BY b.isbn ORDER BY b.title ASC;
GROUP BY b.isbn ORDER BY b.title DESC;
WHERE b.genre = :selectedGenre
GROUP BY b.isbn ORDER BY b.title ASC;

-- Query to add a new row to Members table

INSERT INTO Members (memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, email) VALUES
	(:memberFirstInput, :memberLastInput, :streetAddrInput, :cityInput, :stateInput, :postalInput, :phoneInput, :emailInput);

-- Query to grab existing members in database when adding a reservation

SELECT memberID, memberFirst, memberLast FROM Members;

-- Query to add a new row to Reservations table

INSERT INTO Reservations (memberID, bookID, dateIssued, dateDue, isReturned) VALUES 
	(:selectedMember,
	(SELECT bi.bookID FROM Book_Items AS bi LEFT JOIN Books AS b ON bi.isbn=b.isbn WHERE b.isbn = :isbnInput),
	:issueInput,:dueInput,:isReturnedInput);

-- Query to add a new row to Authors table
-- Does not allow for duplicate authors

INSERT INTO Authors (authorFirst, authorLast) SELECT * FROM (SELECT :authorFirstInput, :authorLastInput) AS tmp
	WHERE NOT EXISTS (SELECT authorFirst, authorLast FROM Authors WHERE authorFirst = :authorFirstInput AND authorLast = :authorLastInput) LIMIT 1;

-- Add new row to Books
-- Requires multiple queries to add authors into Authors if they don't exist, and to add into Book_Items and Author_Books tables

INSERT INTO Books (isbn, title, genre, isFiction) VALUES(:isbn, :title, :genre, :isFiction);
INSERT INTO Authors (authorFirst, authorLast) SELECT * FROM (SELECT %s, %s) AS tmp
	WHERE NOT EXISTS (SELECT authorFirst, authorLast FROM Authors WHERE authorFirst = :authorFirst AND authorLast = :authorLast) LIMIT 1;
INSERT INTO Author_Book (authorID, isbn) VALUES ((SELECT a.authorID FROM Authors AS a WHERE a.authorFirst = :authorFirst AND a.authorLast = :authorLast), :isbn);
INSERT INTO Book_Items (isbn) VALUES :isbn;

-- Query to display member in Members table selected to be updated

SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IFNULL(email, '') as email FROM Members WHERE memberID = :selectedMember;

-- Query to update a row in Members table

UPDATE Members SET memberFirst = :memberFirstInput, memberLast = :memberLastInput, streetAddr = :streetAddrInput, city = :cityInput, state = :stateInput, postalCode = :postalInput, phone = :phoneInput, email = :emailInput 
WHERE memberID = :memberID;

-- Query to display reservation in Reservations table selected to be updated

SELECT DISTINCT r.reservationID, m.memberFirst, m.memberLast, b.isbn, r.dateIssued, r.dateDue, (SELECT IF(isReturned, 'Yes', 'No')) FROM Reservations AS r 
		LEFT JOIN Members AS m ON r.memberID=m.memberID 
		LEFT JOIN Book_Items AS bi ON r.bookID=bi.bookID 
		LEFT JOIN Books AS b ON bi.isbn=b.isbn
		WHERE reservationID = :selectedReservationID;

-- Query to update a row in Reservations table

UPDATE Reservations SET 
	memberID = (SELECT memberID FROM Members WHERE memberFirst = :memberFirstInput AND memberLast = :memberLastInput), 
	bookID = (SELECT bi.bookID FROM Book_Items AS bi LEFT JOIN Books AS b ON bi.isbn=b.isbn WHERE bi.isbn = :isbnInput LIMIT 1),
	dateIssued = :issuedInput, dateDue = :dueInput, isReturned = :isReturnedInput WHERE reservationID = :selectedReservationID;

-- Query to update row in Authors table
 
UPDATE Authors SET authorFirst = :authorFirstInput, authorLast=:authorLastInput WHERE authorID=:selectedAuthorID

-- Query to update row in Books table

UPDATE Books SET title = :title, genre = :genre, isFiction = :isFiction WHERE isbn = :isbn;

-- Query to delete a row from Members table
-- Must remove potential dependencies in Reservations table first

DELETE FROM Reservations WHERE memberID = :MemberID;
DELETE FROM Members WHERE memberID = :MemberID;

-- Query to delete a row from Reservations table

DELETE FROM Reservations WHERE reservationID = :reservationID;

-- Queries to delete from Authors table

DELETE FROM Authors WHERE authorID = :authorID;
DELETE FROM Author_Book WHERE authorID = :authorID;

-- Queries to delete from Books table
DELETE FROM Books WHERE isbn = :isbn;
DELETE FROM Author_Book WHERE isbn = :isbn;
DELETE FROM Book_Item WHERE isbn = :isbn;
