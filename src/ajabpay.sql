-- MySQL dump 10.13  Distrib 5.5.52, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ajabpay
-- ------------------------------------------------------
-- Server version	5.5.52-0ubuntu0.14.04.1

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
-- Table structure for table `account`
--

--
-- Table structure for table `configaccountstatus`
--

DROP TABLE IF EXISTS `configaccountstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configaccountstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configaccountstatus`
--

LOCK TABLES `configaccountstatus` WRITE;
/*!40000 ALTER TABLE `configaccountstatus` DISABLE KEYS */;
INSERT INTO `configaccountstatus` VALUES (1,'Active','ACTIVE'),(2,'Inactive','INACTIVE'),(3,'Unverified','UNVERIFIED'),(4,'Verified and Active','VERIFIED_AND_ACTIVE'),(5,'Dormant','DORMANT');
/*!40000 ALTER TABLE `configaccountstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configcurrency`
--

DROP TABLE IF EXISTS `configcurrency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configcurrency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configcurrency`
--

LOCK TABLES `configcurrency` WRITE;
/*!40000 ALTER TABLE `configcurrency` DISABLE KEYS */;
INSERT INTO `configcurrency` VALUES (1,'US Dollar','USD',1),(2,'Kenya Shilling','KES',1);
/*!40000 ALTER TABLE `configcurrency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configexchangerate`
--

DROP TABLE IF EXISTS `configexchangerate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configexchangerate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `local_currency` varchar(3) DEFAULT NULL,
  `foreign_currency` varchar(3) DEFAULT NULL,
  `buying` decimal(6,2) DEFAULT NULL,
  `selling` decimal(6,2) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configexchangerate`
--

LOCK TABLES `configexchangerate` WRITE;
/*!40000 ALTER TABLE `configexchangerate` DISABLE KEYS */;
INSERT INTO `configexchangerate` VALUES (1,'USD to KES','USD-KES','KES','USD',101.27,101.27,'2016-09-15'),(2,'KES to USD','KES-USD','USD','KES',101.27,101.27,'2016-09-15');
/*!40000 ALTER TABLE `configexchangerate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configledgeraccount`
--

DROP TABLE IF EXISTS `configledgeraccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configledgeraccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  `account_category_id` int(11) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `balance_direction` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`),
  KEY `account_category_id` (`account_category_id`),
  CONSTRAINT `configledgeraccount_ibfk_1` FOREIGN KEY (`account_category_id`) REFERENCES `configledgeraccountcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configledgeraccount`
--

LOCK TABLES `configledgeraccount` WRITE;
/*!40000 ALTER TABLE `configledgeraccount` DISABLE KEYS */;
INSERT INTO `configledgeraccount` VALUES (1,'Assets','10000000',1,'2016-09-15',NULL),(2,'Cash at Bank','11000000',1,'2016-09-15',NULL),(5,'Net Loan Portfolio','12000000',1,'2016-09-15',NULL),(6,'Accounts Receivable','13000000',1,'2016-09-15',NULL),(7,'Liabilities','20000000',2,'2016-09-15',NULL),(8,'Accounts Payables & Other Liabilities','21000000',2,'2016-09-15',NULL),(9,'Customer Transaction Accounts','21100000',2,'2016-09-15',NULL),(10,'Equity','30000000',3,'2016-09-15',NULL),(11,'Share Capital','31000000',3,'2016-09-15',NULL),(12,'Grants and Donations','32000000',3,'2016-09-15',NULL),(13,'Retained Earnings','33000000',3,'2016-09-08',NULL),(14,'Income','40000000',4,'2016-09-15',NULL),(15,'Financial Income','41000000',4,'2016-09-15',NULL),(16,'Interest Income','41100000',4,'2016-09-15',NULL),(17,'Fee Income','41200000',4,'2016-09-15',NULL),(18,'Penalty Income','41300000',4,'2016-09-15',NULL),(19,'Expenses','50000000',5,'2016-09-15',NULL),(20,'Financial Expense','51000000',5,'2016-09-15',NULL),(21,'Write-Off Expense','51200000',5,'2016-09-15',NULL),(22,'Interest Expense','51300000',5,'2016-09-15',NULL),(23,'M-Pesa Bank Account','11100000',1,'2016-09-16',NULL),(24,'Paypal Bank Account','11200000',1,'2016-09-16',NULL),(25,'Paypal Transactional Accounts','21110000',2,'2016-09-17',NULL),(26,'M-Pesa Transactional Accounts','21120000',2,'2016-09-17',NULL);
/*!40000 ALTER TABLE `configledgeraccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configledgeraccountcategory`
--

DROP TABLE IF EXISTS `configledgeraccountcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configledgeraccountcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configledgeraccountcategory`
--

LOCK TABLES `configledgeraccountcategory` WRITE;
/*!40000 ALTER TABLE `configledgeraccountcategory` DISABLE KEYS */;
INSERT INTO `configledgeraccountcategory` VALUES (1,'Asset','ASSET'),(2,'Liability','LIABILITY'),(3,'Equity','EQUITY'),(4,'Income','INCOME'),(5,'Expense','EXPENSE');
/*!40000 ALTER TABLE `configledgeraccountcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configledgeraccountingrule`
--

DROP TABLE IF EXISTS `configledgeraccountingrule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configledgeraccountingrule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_type_id` int(11) DEFAULT NULL,
  `debit_account_id` int(11) DEFAULT NULL,
  `credit_account_id` int(11) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `credit_account_id` (`credit_account_id`),
  KEY `debit_account_id` (`debit_account_id`),
  KEY `transaction_type_id` (`transaction_type_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `configledgeraccountingrule_ibfk_4` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `configledgeraccountingrule_ibfk_5` FOREIGN KEY (`transaction_type_id`) REFERENCES `configtransactiontype` (`id`),
  CONSTRAINT `configledgeraccountingrule_ibfk_6` FOREIGN KEY (`debit_account_id`) REFERENCES `configledgeraccount` (`id`),
  CONSTRAINT `configledgeraccountingrule_ibfk_7` FOREIGN KEY (`credit_account_id`) REFERENCES `configledgeraccount` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configledgeraccountingrule`
--

LOCK TABLES `configledgeraccountingrule` WRITE;
/*!40000 ALTER TABLE `configledgeraccountingrule` DISABLE KEYS */;
INSERT INTO `configledgeraccountingrule` VALUES (3,1,25,26,'2016-09-17',1),(4,2,26,25,'2016-09-17',1);
/*!40000 ALTER TABLE `configledgeraccountingrule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `confignotificationtype`
--

DROP TABLE IF EXISTS `confignotificationtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `confignotificationtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `email_html_template` varchar(500) DEFAULT NULL,
  `email_template` varchar(500) DEFAULT NULL,
  `sms_template` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `confignotificationtype`
--

LOCK TABLES `confignotificationtype` WRITE;
/*!40000 ALTER TABLE `confignotificationtype` DISABLE KEYS */;
INSERT INTO `confignotificationtype` VALUES (1,'Registration','REGISTRATION_COMPLETE','2016-10-17 16:03:00','notifications/registration_complete.html','notifications/registration_complete.txt','notifications/registration_complete.sms'),(2,'Transaction Complete','P2M_TXN_COMPLETE','2016-10-17 16:01:00','notifications/p2m_txn_complete.html','notifications/p2m_txn_complete.txt','notifications/p2m_txn_complete.sms'),(3,'Dispute Created','DISPUTE_CREATED','2016-10-17 16:00:00','notifications/dispute_created.html','notifications/dispute_created.txt','notifications/dispute_created.sms'),(4,'Dispute Resolved','DISPUTE_RESOLVED','2016-10-17 16:00:00','notifications/dispute_resolved.html','notifications/dispute_resolved.txt','notifications/dispute_resolved.sms'),(5,'Identity Revoked','AUTH_REVOKED','2016-10-17 15:59:00','notifications/auth_revoked.html','notifications/auth_revoked.txt','notifications/auth_revoked.sms'),(7,'Risk Dispute Created','RISK_DISPUTE_CREATED','2016-10-17 15:59:00','notifications/risk_dispute_created.html','notifications/risk_dispute_created.txt','notifications/risk_dispute_created.sms'),(8,'Sale Reversed','SALE_REVERSED','2016-10-17 15:59:00','notifications/sale_reversed.html','notifications/sale_reversed.txt','notifications/sale_reversed.sms'),(9,'Account Verification','ACCOUNT_VERIFICATION','2016-10-17 15:56:00','notifications/account_verification.html','notifications/account_verification.txt','notifications/account_verification.sms');
/*!40000 ALTER TABLE `confignotificationtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configpaypalparameter`
--

DROP TABLE IF EXISTS `configpaypalparameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configpaypalparameter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paypal_charge_percentage` decimal(10,2) DEFAULT NULL,
  `paypal_charge_constant` decimal(10,2) DEFAULT NULL,
  `foreign_exchange_rate` decimal(10,2) DEFAULT NULL,
  `foreign_charge_percentage` decimal(10,2) DEFAULT NULL,
  `foreign_charge_constant` decimal(10,2) DEFAULT NULL,
  `service_charge_percentage` decimal(10,2) DEFAULT NULL,
  `service_charge_max` decimal(10,2) DEFAULT NULL,
  `mobile_money_charge` decimal(10,2) DEFAULT NULL,
  `date_created` datetime NOT NULL,
  `foreign_currency` varchar(3) DEFAULT NULL,
  `local_currency` varchar(3) DEFAULT NULL,
  `service_charge_constant` decimal(5,2) DEFAULT NULL,
  `foreign_charge_constant_currency` varchar(3) DEFAULT NULL,
  `mobile_money_charge_currency` varchar(3) DEFAULT NULL,
  `paypal_charge_constant_currency` varchar(3) DEFAULT NULL,
  `service_charge_constant_currency` varchar(3) DEFAULT NULL,
  `service_charge_max_currency` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configpaypalparameter`
--

LOCK TABLES `configpaypalparameter` WRITE;
/*!40000 ALTER TABLE `configpaypalparameter` DISABLE KEYS */;
INSERT INTO `configpaypalparameter` VALUES (1,3.00,0.30,101.41,0.75,2.25,4.50,2000.00,66.00,'2016-09-20 21:19:00','USD','KES',1.00,'KES','KES','USD','USD','KES');
/*!40000 ALTER TABLE `configpaypalparameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configpaypaltransactiontype`
--

DROP TABLE IF EXISTS `configpaypaltransactiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configpaypaltransactiontype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configpaypaltransactiontype`
--

LOCK TABLES `configpaypaltransactiontype` WRITE;
/*!40000 ALTER TABLE `configpaypaltransactiontype` DISABLE KEYS */;
/*!40000 ALTER TABLE `configpaypaltransactiontype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configproducttype`
--

DROP TABLE IF EXISTS `configproducttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configproducttype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configproducttype`
--

LOCK TABLES `configproducttype` WRITE;
/*!40000 ALTER TABLE `configproducttype` DISABLE KEYS */;
INSERT INTO `configproducttype` VALUES (1,'Loan','LOAN'),(3,'Savings','SAVINGS'),(4,'Forex','FOREX');
/*!40000 ALTER TABLE `configproducttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configsmsgateway`
--

DROP TABLE IF EXISTS `configsmsgateway`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configsmsgateway` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  `endpoint` varchar(255) DEFAULT NULL,
  `api_key` varchar(100) DEFAULT NULL,
  `api_secret` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configsmsgateway`
--

LOCK TABLES `configsmsgateway` WRITE;
/*!40000 ALTER TABLE `configsmsgateway` DISABLE KEYS */;
INSERT INTO `configsmsgateway` VALUES (1,'TumaSMS','TUMASMS',NULL,'d9b2cb61ce86679d86cecb8f9666afed','iKhgdwOiNNnE7F5H1Vulmx1oyJ6zBUcj5ZrQXZ5PAkh6Qi6/jBe+xN5/uiDKG/MQ6jXwAZ/NLqC+ck1aVmbR89cKIH43brwTvtKaKeBZo2lry/607SnWIQImJhuarw2RjByyt3opgZaIMx953U8E9paizfwloOE1d+O0sXsX36c=');
/*!40000 ALTER TABLE `configsmsgateway` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configtransactionstatus`
--

DROP TABLE IF EXISTS `configtransactionstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configtransactionstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configtransactionstatus`
--

LOCK TABLES `configtransactionstatus` WRITE;
/*!40000 ALTER TABLE `configtransactionstatus` DISABLE KEYS */;
INSERT INTO `configtransactionstatus` VALUES (1,'Created','CREATED'),(2,'Pending Posting','PENDING_POSTING'),(3,'Posted','POSTED'),(4,'On-Hold','ON_HOLD');
/*!40000 ALTER TABLE `configtransactionstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configtransactiontype`
--

DROP TABLE IF EXISTS `configtransactiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configtransactiontype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configtransactiontype`
--

LOCK TABLES `configtransactiontype` WRITE;
/*!40000 ALTER TABLE `configtransactiontype` DISABLE KEYS */;
INSERT INTO `configtransactiontype` VALUES (1,'Withdrawal','WITHDRAWAL'),(2,'Deposit','DEPOSIT');
/*!40000 ALTER TABLE `configtransactiontype` ENABLE KEYS */;
UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-17 15:30:28
