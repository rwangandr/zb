-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 172.16.50.201    Database: AutoResults
-- ------------------------------------------------------
-- Server version	5.6.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `BuildTracker`
--

DROP TABLE IF EXISTS `BuildTracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BuildTracker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `component` char(50) NOT NULL,
  `build` varchar(50) NOT NULL,
  `individual_smoke` varchar(50) DEFAULT NULL,
  `individual_validation` varchar(50) DEFAULT NULL,
  `integration_combination` varchar(50) DEFAULT NULL,
  `integrated_smoke` varchar(50) DEFAULT NULL,
  `integrated_validation` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `DetailedResults`
--

DROP TABLE IF EXISTS `DetailedResults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DetailedResults` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `component` char(50) NOT NULL,
  `roundId` char(30) NOT NULL,
  `layer` smallint(6) NOT NULL,
  `casePriority` char(8) DEFAULT NULL,
  `caseId` varchar(20) DEFAULT NULL,
  `caseTitle` varchar(250) DEFAULT NULL,
  `result` char(8) DEFAULT NULL,
  `startTime` char(25) DEFAULT NULL,
  `endTime` char(25) DEFAULT NULL,
  `elapsed` char(10) DEFAULT NULL,
  `runTime` char(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LPB`
--

DROP TABLE IF EXISTS `LPB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LPB` (
  `id` int(11) NOT NULL,
  `component` char(50) DEFAULT NULL,
  `individual_ltb` varchar(50) DEFAULT NULL,
  `individual_lpb` varchar(50) DEFAULT NULL,
  `integrated_ltb` varchar(50) DEFAULT NULL,
  `integrated_lpb` varchar(50) DEFAULT NULL,
  `nightly_ltb` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RoundMapping`
--

DROP TABLE IF EXISTS `RoundMapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RoundMapping` (
  `roundId` char(30) NOT NULL,
  `component` char(50) DEFAULT NULL,
  `build` varchar(50) DEFAULT NULL,
  `time` char(18) DEFAULT NULL,
  `type` varchar(40) DEFAULT NULL,
  `version` varchar(50) DEFAULT NULL,
  `db` varchar(25) DEFAULT NULL,
  `errorMessage` text,
  PRIMARY KEY (`roundId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `TestServers`
--

DROP TABLE IF EXISTS `TestServers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TestServers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `component` char(15) DEFAULT NULL,
  `server` varchar(30) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `TotalResults`
--

DROP TABLE IF EXISTS `TotalResults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TotalResults` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `component` char(50) NOT NULL,
  `line` varchar(20) DEFAULT NULL,
  `build` varchar(50) NOT NULL,
  `category` varchar(25) NOT NULL,
  `time` char(18) NOT NULL,
  `total_num` smallint(6) NOT NULL,
  `pass_num` smallint(6) NOT NULL,
  `fail_num` smallint(6) NOT NULL,
  `na_num` smallint(6) DEFAULT NULL,
  `block_num` smallint(6) DEFAULT NULL,
  `startTime` char(25) NOT NULL,
  `endTime` char(25) NOT NULL,
  `duration` time NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-13  9:28:10