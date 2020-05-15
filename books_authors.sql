-- MySQL dump 10.16  Distrib 10.1.37-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: library
------------------------------------------------------
-- Server version 10.1.37-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

---- Table structure for table `Books`--

DROP TABLE IF EXISTS `Books`
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Books`(
    `isbn` varchar NOT NULL DEFAULT '0',
    `title` varchar NOT NULL DEFAULT '0',
    `genre` char NOT NULL,
    `isFiction` boolean NOT NULL,
    `author` int(11) NOT NULL,
    PRIMARY KEY(`isbn`),
    KEY `isbn`(`isbn`),
    CONSTRAINT `Books_ibfk_1` FOREIGN KEY(`author`) REFRENCES `Authors` (`authorID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
---- Dumping data for table `Books`
LOCK TABLES `Books` WRITE;
/*!40000 ALTER TABLE `Books` DISABLE KEYS */;
/*!40000 ALTER TABLE `Books` ENABLE KEYS */;
UNLOCK TABLES;

---- Table structure for table `Authors`--
DROP TABLE IF EXISTS `Authors`
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Authors`(
    `authorID` int(11) NOT NULL AUTO_INCREMENT,
    `authorFirst` varchar NOT NULL DEFAULT '0',
    `authorLast` varchar NOT NULL DEFAULT '0',
    PRIMARY KEY(`authorID`),
    KEY `isbn`(`authorID`),
) ENGINE=InnoDB AUTO_INCREMENT=5 CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
---- Dumping data for table `Books`

LOCK TABLES `Books` WRITE;
/*!40000 ALTER TABLE `Books` DISABLE KEYS */;
/*!40000 ALTER TABLE `Books` ENABLE KEYS */;
UNLOCK TABLES;