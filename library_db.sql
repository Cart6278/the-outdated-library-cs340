-- MariaDB dump 10.17  Distrib 10.4.11-MariaDB, for Linux (x86_64)
--
-- Host: classmysql.engr.oregonstate.edu    Database: cs340_tonm
-- ------------------------------------------------------
-- Server version	10.4.11-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Author_Book`
--

DROP TABLE IF EXISTS `Author_Book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Author_Book` (
  `authorID` int(11) NOT NULL,
  `isbn` varchar(13) NOT NULL,
  KEY `author_book_ibfk_1` (`authorID`),
  KEY `author_book_ibfk_2` (`isbn`),
  CONSTRAINT `author_book_ibfk_1` FOREIGN KEY (`authorID`) REFERENCES `Authors` (`authorID`) ON DELETE CASCADE,
  CONSTRAINT `author_book_ibfk_2` FOREIGN KEY (`isbn`) REFERENCES `Books` (`isbn`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Author_Book`
--

LOCK TABLES `Author_Book` WRITE;
/*!40000 ALTER TABLE `Author_Book` DISABLE KEYS */;
INSERT INTO `Author_Book` VALUES (12,'001284982154'),(13, '001284982154'),(6,'9780871404237'),(7,'9780689878558'),(11,'9871862301382');
/*!40000 ALTER TABLE `Author_Book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Authors`
--

DROP TABLE IF EXISTS `Authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Authors` (
  `authorID` int(11) NOT NULL AUTO_INCREMENT,
  `authorFirst` varchar(30) NOT NULL,
  `authorLast` varchar(30) NOT NULL,
  PRIMARY KEY (`authorID`),
  UNIQUE KEY `authorID` (`authorID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Authors`
--

LOCK TABLES `Authors` WRITE;
/*!40000 ALTER TABLE `Authors` DISABLE KEYS */;
INSERT INTO `Authors` VALUES (1,'JK','Rowling'),(3,'JRR','Tolkein'),(4,'Wesley','Chu'),(5,'Mary','Beard'),(6,'Sharon Kay','Penman'),(7,'Tamora','Pierce'),(8,'Philip','Pullman'),(9,'Marlon','James'),(11,'Brian','Jaques'),(12,'Sample','Author'),(13,'Sample','SecondAuthor');
/*!40000 ALTER TABLE `Authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Book_Items`
--

DROP TABLE IF EXISTS `Book_Items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Book_Items` (
  `bookID` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` varchar(13) NOT NULL,
  PRIMARY KEY (`bookID`),
  KEY `book_items_ibfk_1` (`isbn`),
  CONSTRAINT `book_items_ibfk_1` FOREIGN KEY (`isbn`) REFERENCES `Books` (`isbn`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Book_Items`
--

LOCK TABLES `Book_Items` WRITE;
/*!40000 ALTER TABLE `Book_Items` DISABLE KEYS */;
INSERT INTO `Book_Items` VALUES (1,'001284982154'),(2,'001284982154'),(3,'9780553448122'),(4,'9780679879244'),(5,'9780689878558'),(6,'9780871404237'),(7,'9871862301382');
/*!40000 ALTER TABLE `Book_Items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Books`
--

DROP TABLE IF EXISTS `Books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Books` (
  `isbn` varchar(13) NOT NULL,
  `title` varchar(255) NOT NULL,
  `genre` char(30) NOT NULL,
  `isFiction` tinyint(1) NOT NULL,
  PRIMARY KEY (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Books`
--

LOCK TABLES `Books` WRITE;
/*!40000 ALTER TABLE `Books` DISABLE KEYS */;
INSERT INTO `Books` VALUES ('001284982154','Sample Book Title','Mystery',1),('9780553448122','Artemis','Science Fiction',1),('9780679879244','The Golden Compass','Fantasy',1),('9780689878558','Alanna: The First Adventure','Fantasy',1),('9780871404237','SPQR: A History of Ancient Rome','Refrence',0),('9871862301382','Redwall','Fantasy',1);
/*!40000 ALTER TABLE `Books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Members`
--

DROP TABLE IF EXISTS `Members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Members` (
  `memberID` int(8) NOT NULL AUTO_INCREMENT,
  `memberFirst` varchar(30) NOT NULL,
  `memberLast` varchar(30) NOT NULL,
  `streetAddr` varchar(255) NOT NULL,
  `city` char(30) NOT NULL,
  `state` char(2) NOT NULL,
  `postalCode` varchar(5) NOT NULL,
  `phoneNum` varchar(10) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`memberID`),
  UNIQUE KEY `memberID` (`memberID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Members`
--

LOCK TABLES `Members` WRITE;
/*!40000 ALTER TABLE `Members` DISABLE KEYS */;
INSERT INTO `Members` VALUES (1,'John','Smith','123 Main Street','Corvallis','OR','97331','5051239988','jsmith@osu.edu'),(2,'Katherine','Jones','1892 SW 2nd Street, #200A','Corvallis','OR','97331','4441234568',NULL),(3,'Eric','Zhang','807 Roberts Drive','Salem','OR','97302','1234569090','zhangeric@gmail.com'),(4,'Generic','Name','987 Fake Road','Fake City','FL','33708','6457278014','fakeemail@yahoo.com'),(5,'Jenny','White','55892 N 8th Ave','New Town','CA','12345','5559413299',NULL);
/*!40000 ALTER TABLE `Members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reservations`
--

DROP TABLE IF EXISTS `Reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Reservations` (
  `reservationID` int(11) NOT NULL AUTO_INCREMENT,
  `memberID` int(8) NOT NULL,
  `bookID` int(11) NOT NULL,
  `dateIssued` date NOT NULL,
  `dateDue` date NOT NULL,
  `isReturned` tinyint(1) NOT NULL,
  PRIMARY KEY (`reservationID`),
  KEY `reservations_ibfk_1` (`memberID`),
  KEY `reservations_ibfk_2` (`bookID`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`memberID`) REFERENCES `Members` (`memberID`),
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`bookID`) REFERENCES `Book_Items` (`bookID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reservations`
--

LOCK TABLES `Reservations` WRITE;
/*!40000 ALTER TABLE `Reservations` DISABLE KEYS */;
INSERT INTO `Reservations` VALUES (1,3,1,'2020-05-14','2020-05-28',0),(2,2,2,'2020-05-14','2020-05-28',0),(3,1,7,'2020-04-28','2020-05-12',1);
/*!40000 ALTER TABLE `Reservations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-16 11:58:54
