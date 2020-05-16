INSERT INTO Authors (authorID, authorFirst, authorLast)
VALUES (:aIDInput, :aFirstInput, :aLastInput);

INSERT INTO Books (isbn, title, genre, isFiction)
VALUES (:isbnInput, :titleInput, :genreInput, :isFicInput);

UPDATE Authors SET authorFirst = :aFirstInput, authorLast = :aLastInput
WHERE authorID=:aIDFromForm;

UPDATE Books SET isbn= :isbnInput title = :titleInput  genre = :genreInput, isFiction = :isFicInput
WHERE id= :bookIDFromForm;

DELETE FROM Authors WHERE id= :aIDFromDele;

DELETE FROM Books WHERE id= :bookIDFromDele;