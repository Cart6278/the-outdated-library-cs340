--
-- Table structure for table `Members`
--

DROP TABLE IF EXISTS `Members`;
CREATE TABLE `Members`(
	`memberID` int(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`memberFirst` varchar(30) NOT NULL,
	`memberLast` varchar(30) NOT NULL,
	`streetAddr` varchar(255) NOT NULL,
	`city` char(30) NOT NULL,
	`state` char(2) NOT NULL,
	`postalCode` varchar(5) NOT NULL,
	`phoneNum` varchar(10) NOT NULL,
	`email` varchar(255),
	UNIQUE (`memberID`)
) ENGINE=InnoDB;

--
-- Dumping data for table 'Members'
--

INSERT INTO `Members` (`memberID`, `memberFirst`, `memberLast`, `streetAddr`, `city`, `state`, `postalCode`, `phoneNum`, `email`) VALUES
	(1, 'John', 'Smith', '123 Main Street', 'Corvallis', 'OR', '97331', '5051239988', 'jsmith@osu.edu'),
	(2, 'Katherine', 'Jones', '1892 SW 2nd Street, #200A', 'Corvallis', 'OR', '97331', '4441234568', NULL),
	(3, 'Eric', 'Zhang', '807 Roberts Drive', 'Salem', 'OR', '97302', '1234569090', 'zhangeric@gmail.com'),
	(4, 'Generic', 'Name', '987 Fake Road', 'Fake City', 'FL', '33708', '6457278014', 'fakeemail@yahoo.com');

--
-- Table structure for table `Books`
--

DROP TABLE IF EXISTS `Books`;
CREATE TABLE `Books`(
	`isbn` varchar(13) NOT NULL PRIMARY KEY,
	`title` varchar(255) NOT NULL,
	`genre` char(30) NOT NULL,
	`isFiction` boolean NOT NULL
) ENGINE=InnoDB;

INSERT INTO `Books` (`isbn`, `title`, `genre`, `isFiction`) VALUES
	('001284982154', 'Sample Book Title', 'Mystery', 1);

--
-- Table structure for table `Authors`
--

DROP TABLE IF EXISTS `Authors`;
CREATE TABLE `Authors`(
	`authorID` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`authorFirst` varchar(30) NOT NULL,
	`authorLast` varchar(30) NOT NULL,
	UNIQUE (`authorID`)
) ENGINE=InnoDB;

--
-- Table structure for table `Author_Book`
--

DROP TABLE IF EXISTS `Author_Book`;
CREATE TABLE `Author_Book`(
	`authorID` int(11) NOT NULL,
	`isbn` varchar(13) NOT NULL,
	CONSTRAINT `author_book_ibfk_1` FOREIGN KEY(`authorID`) REFERENCES `Authors`(`authorID`),
	CONSTRAINT `author_book_ibfk_2` FOREIGN KEY(`isbn`) REFERENCES `Books`(`isbn`)
) ENGINE=InnoDB;

--
-- Table structure for table `Book_Items`
--

DROP TABLE IF EXISTS `Book_Items`;
CREATE TABLE `Book_Items`(
	`bookID` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`isbn` varchar(13) NOT NULL,
	CONSTRAINT `book_items_ibfk_1` FOREIGN KEY(`isbn`) REFERENCES `Books`(`isbn`)
) ENGINE=InnoDB;

INSERT INTO `Book_Items` (`bookID`, `isbn`) VALUES
	(1, '001284982154'),
	(2, '001284982154');

--
-- Table structure for table `Reservations`
--

DROP TABLE IF EXISTS `Reservations`;
CREATE TABLE `Reservations`(
	`reservationID` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`memberID` int(8) NOT NULL,
	`bookID` int(11) NOT NULL,
	`dateIssued` date NOT NULL,
	`dateDue` date NOT NULL,
	`isReturned` boolean NOT NULL,
	CONSTRAINT `reservations_ibfk_1` FOREIGN KEY(`memberID`) REFERENCES `Members`(`memberID`),
	CONSTRAINT `reservations_ibfk_2` FOREIGN KEY(`bookID`) REFERENCES `Book_Items`(`bookID`)
) ENGINE=InnoDB;

INSERT INTO `Reservations` (`reservationID`, `memberID`, `bookID`, `dateIssued`, `dateDue`, `isReturned`) VALUES
	(1, 3, 1, '2020-05-14', '2020-05-28', 0);
