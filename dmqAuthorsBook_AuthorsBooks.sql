
--Get Author Information
SELECT a.author_id AS authorID, a.first_name as a.authorFirst, a.last_name as a.authorLast FROM Authors a;
--Get book information
SELECT a.first_name, a.last_name FROM Books b LEFT JOIN Author_Book ab ON ab.isbn=b.isbn LEFT JOIN Authors a ON
ab.authorID=a.authorID GROUP BY a.authorID, b.isbn ORDER BY a.last_name ASC;

INSERT INTO Authors (authorID, authorFirst, authorLast) -- do we include authorID, that's supposed to be created by the database
VALUES (:aIDInput, :aFirstInput, :aLastInput);

INSERT INTO Books (isbn, title, genre, isFiction)
VALUES (:isbnInput, :titleInput, :genreInput, :isFicInput);

INSERT INTO Author_Book (authorID, isbn) VALUES (:authorIDInput, :isbnInput);

UPDATE Authors SET authorFirst = :aFirstInput, authorLast = :aLastInput
WHERE authorID= :aIDFromForm;

UPDATE Books SET isbn= :isbnInput title = :titleInput  genre = :genreInput, isFiction = :isFicInput
WHERE isbn= :bookIDFromForm;

DELETE FROM Authors WHERE id= :aIDFromDele;

DELETE FROM Books WHERE id= :bookIDFromDele;