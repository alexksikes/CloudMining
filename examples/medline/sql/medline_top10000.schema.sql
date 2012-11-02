-- MySQL dump 10.13  Distrib 5.1.63, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: medline_sample
-- ------------------------------------------------------
-- Server version	5.1.63-0+squeeze1

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
-- Table structure for table `author_full_names`
--

DROP TABLE IF EXISTS `author_full_names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author_full_names` (
  `filename` varchar(32) DEFAULT NULL,
  `pmid` int(12) unsigned DEFAULT NULL,
  `author_full_name` varchar(150) DEFAULT NULL,
  KEY `pmid` (`pmid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `author_terms`
--

DROP TABLE IF EXISTS `author_terms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author_terms` (
  `id` int(32) unsigned NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author` (`author`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authors` (
  `filename` varchar(32) DEFAULT NULL,
  `pmid` int(12) unsigned DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  KEY `author` (`author`),
  KEY `pmid` (`pmid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `citations`
--

DROP TABLE IF EXISTS `citations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `citations` (
  `filename` varchar(32) DEFAULT NULL,
  `pmid` int(12) unsigned NOT NULL,
  `volume` varchar(50) DEFAULT NULL,
  `issue` varchar(50) DEFAULT NULL,
  `pagination` varchar(150) DEFAULT NULL,
  `date_of_publication` varchar(100) DEFAULT NULL,
  `year` int(4) unsigned DEFAULT NULL,
  `title` text,
  `book_title` varchar(250) DEFAULT NULL,
  `collection_title` varchar(250) DEFAULT NULL,
  `abstract` text,
  `affiliation` varchar(500) DEFAULT NULL,
  `journal_title_abbreviation` varchar(150) DEFAULT NULL,
  `journal_title` varchar(250) DEFAULT NULL,
  `journal_id` varchar(12) DEFAULT NULL,
  `pmc_id` int(12) DEFAULT NULL,
  `entrez_date` date DEFAULT NULL,
  `source` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`pmid`),
  KEY `journal_title_abbreviation` (`journal_title_abbreviation`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `docids`
--

DROP TABLE IF EXISTS `docids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `docids` (
  `pmid` int(32) unsigned NOT NULL,
  `docid` int(32) unsigned DEFAULT NULL,
  PRIMARY KEY (`pmid`),
  KEY `docid` (`docid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `journal_terms`
--

DROP TABLE IF EXISTS `journal_terms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `journal_terms` (
  `id` int(32) unsigned NOT NULL,
  `journal` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `journal` (`journal`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mesh`
--

DROP TABLE IF EXISTS `mesh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mesh` (
  `filename` varchar(32) DEFAULT NULL,
  `pmid` int(12) unsigned DEFAULT NULL,
  `mesh_term` varchar(200) DEFAULT NULL,
  KEY `pmid` (`pmid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mesh_terms`
--

DROP TABLE IF EXISTS `mesh_terms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mesh_terms` (
  `filename` varchar(32) DEFAULT NULL,
  `pmid` int(12) unsigned DEFAULT NULL,
  `mesh_term` varchar(200) DEFAULT NULL,
  KEY `mesh_term` (`mesh_term`),
  KEY `pmid` (`pmid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 MAX_ROWS=4294967295;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mesh_terms_terms`
--

DROP TABLE IF EXISTS `mesh_terms_terms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mesh_terms_terms` (
  `id` int(32) unsigned NOT NULL,
  `mesh_term` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mesh_term` (`mesh_term`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pmc_citations`
--

DROP TABLE IF EXISTS `pmc_citations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pmc_citations` (
  `filename` varchar(32) DEFAULT NULL,
  `pmid` int(12) unsigned DEFAULT NULL,
  `cited_pmid` int(12) unsigned DEFAULT NULL,
  KEY `pmid` (`pmid`),
  KEY `cited_pmid` (`cited_pmid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pmc_num_citations`
--

DROP TABLE IF EXISTS `pmc_num_citations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pmc_num_citations` (
  `pmid` int(12) unsigned NOT NULL,
  `count` int(12) DEFAULT NULL,
  PRIMARY KEY (`pmid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `publication_types`
--

DROP TABLE IF EXISTS `publication_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `publication_types` (
  `filename` varchar(32) DEFAULT NULL,
  `pmid` int(12) unsigned DEFAULT NULL,
  `publication_type` varchar(150) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-11-02 12:22:02
