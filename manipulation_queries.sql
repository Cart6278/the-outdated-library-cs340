----
-- For all queries, ':' denotes a variable that will be filled out by the user or computed by the back-end
----

-- Query to display members on Browse Members page, with NULL e-mails replaced by empty string
SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IfNull(email, '') as email FROM Members;

-- Queries to display members, sorted by selected option
SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IfNull(email, '') as email FROM Members
ORDER BY memberID ASC;

SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IfNull(email, '') as email FROM Members
ORDER BY memberID DESC;

SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IfNull(email, '') as email FROM Members
ORDER BY memberFirst ASC;

SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IfNull(email, '') as email FROM Members
ORDER BY memberFirst DESC;

SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IfNull(email, '') as email FROM Members
ORDER BY memberLast DESC;

SELECT memberID, memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, IfNull(email, '') as email FROM Members
ORDER BY memberLast DESC;

-- Query to display reservations on Browse Reservations page, with boolean values shown as 'Yes' or 'No'
SELECT reservationID, memberFirst, memberLast, isbn, dateIssued, dateDue, (SELECT IF(isReturned, 'Yes', 'No')) as isReturned FROM Reservations;

-- Queries to display reservations, sorted by selected option
SELECT reservationID, memberFirst, memberLast, isbn, dateIssued, dateDue, (SELECT IF(isReturned, 'Yes', 'No')) as isReturned FROM Reservations
ORDER BY dateIssued ASC;

SELECT reservationID, memberFirst, memberLast, isbn, dateIssued, dateDue, (SELECT IF(isReturned, 'Yes', 'No')) as isReturned FROM Reservations
ORDER BY dateIssued DESC;

SELECT reservationID, memberFirst, memberLast, isbn, dateIssued, dateDue, (SELECT IF(isReturned, 'Yes', 'No')) as isReturned FROM Reservations
ORDER BY dateDue ASC;

SELECT reservationID, memberFirst, memberLast, isbn, dateIssued, dateDue, (SELECT IF(isReturned, 'Yes', 'No')) as isReturned FROM Reservations
ORDER BY dateDue DESC;

SELECT reservationID, memberFirst, memberLast, isbn, dateIssued, dateDue, (SELECT IF(isReturned, 'Yes', 'No')) as isReturned FROM Reservations
WHERE isReturned = 1;

SELECT reservationID, memberFirst, memberLast, isbn, dateIssued, dateDue, (SELECT IF(isReturned, 'Yes', 'No')) as isReturned FROM Reservations
WHERE isReturned = 0;

-- Query to display author information
SELECT a.author_id AS authorID, a.first_name as a.authorFirst, a.last_name as a.authorLast FROM Authors a;

-- Query to display book information
SELECT a.first_name, a.last_name FROM Books b LEFT JOIN Author_Book ab ON ab.isbn=b.isbn LEFT JOIN Authors a ON
ab.authorID=a.authorID GROUP BY a.authorID, b.isbn ORDER BY a.last_name ASC;

-- Query to add a new member 
INSERT INTO Members (memberFirst, memberLast, streetAddr, city, state, postalCode, phoneNum, email) VALUES
	(:memberFirstInput, :memberLastInput, :streetAddrInput, :cityInput, :stateInput, :postalInput, :phoneInput, :emailInput);

-- Query to add a new reservation 
INSERT INTO Reservations (memberFirst, memberLast, isbn, dateIssued, dateDue, isReturned) VALUES
	(:memberFirstInput, :memberLastInput, :isbnInput, :dateIssuedInput, :dateDueInput, 0);

-- Query to add a new author
INSERT INTO Authors (authorID, authorFirst, authorLast) -- do we include authorID, that's supposed to be created by the database
VALUES (:aIDInput, :aFirstInput, :aLastInput);

-- Query to add a new book
INSERT INTO Books (isbn, title, genre, isFiction)
VALUES (:isbnInput, :titleInput, :genreInput, :isFicInput);

INSERT INTO Author_Book (authorID, isbn) VALUES (:authorIDInput, :isbnInput);

-- Query to update a member 
UPDATE Members SET memberFirst = :memberFirstInput, memberLast = :memberLastInput, streetAddr = :streetAddrInput, city = :cityInput, state = :stateInput, postalCode = :postalInput, phone = :phoneInput, email = :emailInput 
WHERE memberID = :memberID;

-- Query to update a reservation
UPDATE Reservations SET memberFirst = :memberFirstInput, memberLast = :memberLastInput, isbn = :isbnInput, dateIssued = :dateIssuedInput, dateDueInput = :dateDueInput, isReturned = :isReturnedInput
WHERE reservationID = :reservationID;

-- Query to update an author
UPDATE Authors SET authorFirst = :aFirstInput, authorLast = :aLastInput
WHERE authorID= :aIDFromForm;

-- Query to update a book
UPDATE Books SET isbn= :isbnInput title = :titleInput  genre = :genreInput, isFiction = :isFicInput
WHERE isbn= :bookIDFromForm;

-- Query to delete a row from Members
-- Must remove potential dependencies in Reservations table first
DELETE FROM Reservations WHERE memberID = :MemberID;
DELETE FROM Members WHERE memberID = :MemberID;

-- Query to delete a row from Reservations
DELETE FROM Reservations WHERE reservationID = :reservationID;

-- Query to delete a row from Authors
DELETE FROM Authors WHERE id= :aIDFromDele;

-- Query to delete a row from Books
DELETE FROM Books WHERE id= :bookIDFromDele;