-- MySQL dump 10.13  Distrib 5.5.50, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ajabpay
-- ------------------------------------------------------
-- Server version	5.5.50-0ubuntu0.14.04.1

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

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_number` varchar(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `notes` varchar(400) DEFAULT NULL,
  `txn_withdraw_limit` decimal(6,2) DEFAULT NULL,
  `txn_deposit_limit` decimal(6,2) DEFAULT NULL,
  `total_withdraws` decimal(6,2) DEFAULT NULL,
  `total_deposits` decimal(6,2) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `date_updated` date DEFAULT NULL,
  `amount_currency_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_number` (`account_number`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  KEY `amount_currency_id` (`amount_currency_id`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `account_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `account_ibfk_3` FOREIGN KEY (`amount_currency_id`) REFERENCES `configcurrency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'FGH3228723OOHB',1,1,'Paypal-Mpesa Account',150.00,250.00,0.00,0.00,'2016-09-17','2016-09-17',1);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accountstatus`
--

DROP TABLE IF EXISTS `accountstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accountstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `reason` varchar(140) DEFAULT NULL,
  `approved_by_id` int(11) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  KEY `approved_by_id` (`approved_by_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `accountstatus_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `accountstatus_ibfk_2` FOREIGN KEY (`approved_by_id`) REFERENCES `user` (`id`),
  CONSTRAINT `accountstatus_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `configaccountstatus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accountstatus`
--

LOCK TABLES `accountstatus` WRITE;
/*!40000 ALTER TABLE `accountstatus` DISABLE KEYS */;
/*!40000 ALTER TABLE `accountstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('93e27f53e870');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

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
  PRIMARY KEY (`id`)
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
  CONSTRAINT `configledgeraccountingrule_ibfk_1` FOREIGN KEY (`credit_account_id`) REFERENCES `configledgeraccount` (`id`),
  CONSTRAINT `configledgeraccountingrule_ibfk_2` FOREIGN KEY (`debit_account_id`) REFERENCES `configledgeraccount` (`id`),
  CONSTRAINT `configledgeraccountingrule_ibfk_3` FOREIGN KEY (`transaction_type_id`) REFERENCES `configtransactiontype` (`id`),
  CONSTRAINT `configledgeraccountingrule_ibfk_4` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
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
-- Table structure for table `confignotificationtemplate`
--

DROP TABLE IF EXISTS `confignotificationtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `confignotificationtemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(100) DEFAULT NULL,
  `notification_type_id` int(11) DEFAULT NULL,
  `email_template` varchar(500) DEFAULT NULL,
  `sms_template` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `notification_type_id` (`notification_type_id`),
  CONSTRAINT `confignotificationtemplate_ibfk_1` FOREIGN KEY (`notification_type_id`) REFERENCES `confignotificationtype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `confignotificationtemplate`
--

LOCK TABLES `confignotificationtemplate` WRITE;
/*!40000 ALTER TABLE `confignotificationtemplate` DISABLE KEYS */;
INSERT INTO `confignotificationtemplate` VALUES (1,'Registration','REGISTRATION',1,'{0}, your account has been created successfully. Your Registration code is {1}','{0}, your account has been created successfully. Your Registration code is {1}');
/*!40000 ALTER TABLE `confignotificationtemplate` ENABLE KEYS */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `confignotificationtype`
--

LOCK TABLES `confignotificationtype` WRITE;
/*!40000 ALTER TABLE `confignotificationtype` DISABLE KEYS */;
INSERT INTO `confignotificationtype` VALUES (1,'Registration','REGISTRATION'),(2,'Transaction Done','TXN_DONE'),(3,'Dispute Created','DISPUTE_CREATED'),(4,'Dispute Resolved','DISPUTE_RESOLVED'),(5,'Identity Revoked','AUTH_REVOKED'),(7,'Risk Dispute Created','RISK_DISPUTE_CREATED'),(8,'Sale Reversed','SALE_REVERSED');
/*!40000 ALTER TABLE `confignotificationtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configpaypalaccountwebhook`
--

DROP TABLE IF EXISTS `configpaypalaccountwebhook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configpaypalaccountwebhook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `url_for` varchar(20) DEFAULT NULL,
  `paypal_api_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `paypal_api_id` (`paypal_api_id`),
  CONSTRAINT `configpaypalaccountwebhook_ibfk_1` FOREIGN KEY (`paypal_api_id`) REFERENCES `configpaypalapiaccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configpaypalaccountwebhook`
--

LOCK TABLES `configpaypalaccountwebhook` WRITE;
/*!40000 ALTER TABLE `configpaypalaccountwebhook` DISABLE KEYS */;
/*!40000 ALTER TABLE `configpaypalaccountwebhook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configpaypalapiaccount`
--

DROP TABLE IF EXISTS `configpaypalapiaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configpaypalapiaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` date DEFAULT NULL,
  `live` tinyint(1) DEFAULT NULL,
  `account_email` varchar(100) DEFAULT NULL,
  `client_id` varchar(100) DEFAULT NULL,
  `client_secret` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configpaypalapiaccount`
--

LOCK TABLES `configpaypalapiaccount` WRITE;
/*!40000 ALTER TABLE `configpaypalapiaccount` DISABLE KEYS */;
INSERT INTO `configpaypalapiaccount` VALUES (1,'2016-09-15',0,'info-facilitator@ajabworld.net','ATo_Io1R9XCX9SmfHdGbeXYSKZnireDROhLUwcjO_VtLiUx7yB7CuMjTWJO0JgfGSXhxCLsLXna3KIn0','EIbbidsOH9Y_2aXPiInRs7Wf-2Emn6fBzTfHXjxgZwC23Lu00zhvA2rImcz-7nkr1OfaDNuwq4yUWgYV'),(2,'2016-09-15',1,'info@ajabworld.net','AbkGI35O5ZanygiMziTYOI5UTDcu-DxyWxRg_3RnVjxDlcDsECuyt1JhY1e8T3gIe5Iasgn3h7V2J2ff','EGpfDwk6j7Gk78AGv-B_57f5H372_cziqaEkT2yXjVMzGEvlY3bfswGfJ7_KaditWleKy9zMC61Cs10K');
/*!40000 ALTER TABLE `configpaypalapiaccount` ENABLE KEYS */;
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

--
-- Table structure for table `configwebhookeventtype`
--

DROP TABLE IF EXISTS `configwebhookeventtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configwebhookeventtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configwebhookeventtype`
--

LOCK TABLES `configwebhookeventtype` WRITE;
/*!40000 ALTER TABLE `configwebhookeventtype` DISABLE KEYS */;
INSERT INTO `configwebhookeventtype` VALUES (1,'Customer dispute created','CUSTOMER_DISPUTE_CREATED',1),(2,'Customer dispute resolved','CUSTOMER_DISPUTE_RESOLVED',1),(3,'Identity authorization-consent revoked','IDENTITY_AUTH_REVOKED',1),(4,'Payment sale completed','SALE_COMPLETED',1),(5,'Payment sale denied','SALE_DENIED',1),(6,'Payment sale pending','SALE_PENDING',1),(7,'Payment sale refunded','SALE_REFUNDED',1),(8,'Payment sale reversed','SALE_REVERSED',1),(9,'Risk dispute created','RISK_DISPUTE_CREATED',1);
/*!40000 ALTER TABLE `configwebhookeventtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emailmessage`
--

DROP TABLE IF EXISTS `emailmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emailmessage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_type` int(11) DEFAULT NULL,
  `email_arguments` varchar(255) DEFAULT NULL,
  `message_recipient` varchar(100) DEFAULT NULL,
  `template_id` int(11) DEFAULT NULL,
  `delivered` tinyint(1) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_delivered` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `template_id` (`template_id`),
  CONSTRAINT `emailmessage_ibfk_1` FOREIGN KEY (`template_id`) REFERENCES `confignotificationtemplate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emailmessage`
--

LOCK TABLES `emailmessage` WRITE;
/*!40000 ALTER TABLE `emailmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `emailmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpesatransaction`
--

DROP TABLE IF EXISTS `mpesatransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mpesatransaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mpesa_transaction_no` varchar(100) DEFAULT NULL,
  `transaction_id` int(11) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mpesa_transaction_no` (`mpesa_transaction_no`),
  KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `mpesatransaction_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mpesatransaction`
--

LOCK TABLES `mpesatransaction` WRITE;
/*!40000 ALTER TABLE `mpesatransaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `mpesatransaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paypaladdress`
--

DROP TABLE IF EXISTS `paypaladdress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypaladdress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paypal_profile_id` int(11) DEFAULT NULL,
  `street_address` varchar(100) DEFAULT NULL,
  `locality` varchar(50) DEFAULT NULL,
  `region` varchar(50) DEFAULT NULL,
  `postal_code` varchar(15) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `paypal_profile_id` (`paypal_profile_id`),
  CONSTRAINT `paypaladdress_ibfk_1` FOREIGN KEY (`paypal_profile_id`) REFERENCES `paypalprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypaladdress`
--

LOCK TABLES `paypaladdress` WRITE;
/*!40000 ALTER TABLE `paypaladdress` DISABLE KEYS */;
/*!40000 ALTER TABLE `paypaladdress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paypalprofile`
--

DROP TABLE IF EXISTS `paypalprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypalprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL,
  `payer_id` varchar(20) DEFAULT NULL,
  `paypal_user_id` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `given_name` varchar(100) DEFAULT NULL,
  `family_name` varchar(100) DEFAULT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `phone_number` varchar(100) DEFAULT NULL,
  `age_range` varchar(10) DEFAULT NULL,
  `email_verified` tinyint(1) DEFAULT NULL,
  `verified_account` tinyint(1) DEFAULT NULL,
  `account_type` varchar(10) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `date_updated` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `payer_id` (`payer_id`),
  UNIQUE KEY `paypal_user_id` (`paypal_user_id`),
  KEY `account_id` (`account_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `paypalprofile_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `paypalprofile_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypalprofile`
--

LOCK TABLES `paypalprofile` WRITE;
/*!40000 ALTER TABLE `paypalprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `paypalprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paypaltoken`
--

DROP TABLE IF EXISTS `paypaltoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypaltoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paypal_profile_id` int(11) DEFAULT NULL,
  `scope` varchar(100) DEFAULT NULL,
  `access_token` varchar(255) DEFAULT NULL,
  `refresh_token` varchar(255) DEFAULT NULL,
  `token_type` varchar(15) DEFAULT NULL,
  `expires_in` int(11) DEFAULT NULL,
  `exires_at` date DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `paypal_profile_id` (`paypal_profile_id`),
  CONSTRAINT `paypaltoken_ibfk_1` FOREIGN KEY (`paypal_profile_id`) REFERENCES `paypalprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypaltoken`
--

LOCK TABLES `paypaltoken` WRITE;
/*!40000 ALTER TABLE `paypaltoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `paypaltoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paypaltransaction`
--

DROP TABLE IF EXISTS `paypaltransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypaltransaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paypal_transaction_id` varchar(50) DEFAULT NULL,
  `transaction_id` int(11) DEFAULT NULL,
  `create_time` date DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `intent` varchar(20) DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `paypal_transaction_id` (`paypal_transaction_id`),
  KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `paypaltransaction_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypaltransaction`
--

LOCK TABLES `paypaltransaction` WRITE;
/*!40000 ALTER TABLE `paypaltransaction` DISABLE KEYS */;
INSERT INTO `paypaltransaction` VALUES (1,'PAY-7NB40724BD666335FK7O2XWI',12,'2016-09-17','created','sale','paypal','2016-09-17');
/*!40000 ALTER TABLE `paypaltransaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `product_type_id` int(11) DEFAULT NULL,
  `txn_withdrawal_limit` decimal(6,2) DEFAULT NULL,
  `txn_deposit_limit` decimal(6,2) DEFAULT NULL,
  `daily_withdraw_limit` decimal(6,2) DEFAULT NULL,
  `daily_deposit_limit` decimal(6,2) DEFAULT NULL,
  `weekly_withdraw_limit` decimal(6,2) DEFAULT NULL,
  `weekly_deposit_limit` decimal(6,2) DEFAULT NULL,
  `monthly_withdraw_limit` decimal(6,2) DEFAULT NULL,
  `monthly_deposit_limit` decimal(6,2) DEFAULT NULL,
  `yearly_withdraw_limit` decimal(6,2) DEFAULT NULL,
  `yearly_deposit_limit` decimal(6,2) DEFAULT NULL,
  `date_updated` date DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `amount_currency_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_type_id` (`product_type_id`),
  KEY `amount_currency_id` (`amount_currency_id`),
  CONSTRAINT `product_ibfk_2` FOREIGN KEY (`product_type_id`) REFERENCES `configproducttype` (`id`),
  CONSTRAINT `product_ibfk_3` FOREIGN KEY (`amount_currency_id`) REFERENCES `configcurrency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Paypal Exchange','PP-MPESA-F',1,4,250.00,500.00,250.00,250.00,500.00,500.00,1000.00,1000.00,6000.00,6000.00,'2016-09-17','2016-09-17',1);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smsmessage`
--

DROP TABLE IF EXISTS `smsmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `smsmessage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_type` int(11) DEFAULT NULL,
  `message_recipient` varchar(15) DEFAULT NULL,
  `sms_gateway_id` int(11) DEFAULT NULL,
  `delivered` tinyint(1) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `date_delivered` datetime DEFAULT NULL,
  `message_arguments` varchar(255) DEFAULT NULL,
  `template_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sms_gateway_id` (`sms_gateway_id`),
  KEY `template_id` (`template_id`),
  CONSTRAINT `smsmessage_ibfk_1` FOREIGN KEY (`sms_gateway_id`) REFERENCES `configsmsgateway` (`id`),
  CONSTRAINT `smsmessage_ibfk_2` FOREIGN KEY (`template_id`) REFERENCES `confignotificationtemplate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smsmessage`
--

LOCK TABLES `smsmessage` WRITE;
/*!40000 ALTER TABLE `smsmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `smsmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_no` varchar(100) DEFAULT NULL,
  `transaction_type_id` int(11) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL,
  `reversing_transaction_id` int(11) DEFAULT NULL,
  `currency_id` int(11) DEFAULT NULL,
  `amount` decimal(18,2) DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  `notified` tinyint(1) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `transaction_no` (`transaction_no`),
  KEY `account_id` (`account_id`),
  KEY `currency_id` (`currency_id`),
  KEY `reversing_transaction_id` (`reversing_transaction_id`),
  KEY `transaction_type_id` (`transaction_type_id`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`currency_id`) REFERENCES `configcurrency` (`id`),
  CONSTRAINT `transaction_ibfk_3` FOREIGN KEY (`reversing_transaction_id`) REFERENCES `transaction` (`id`),
  CONSTRAINT `transaction_ibfk_5` FOREIGN KEY (`transaction_type_id`) REFERENCES `configtransactiontype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` VALUES (10,'PAY-4WE16517E2938544XK7O2UBY',1,1,NULL,1,50.00,NULL,0,'2016-09-17'),(12,'PAY-7NB40724BD666335FK7O2XWI',1,1,NULL,1,50.00,NULL,0,'2016-09-17');
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactionentry`
--

DROP TABLE IF EXISTS `transactionentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transactionentry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_id` int(11) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL,
  `ledger_account_id` int(11) DEFAULT NULL,
  `item_type` int(11) DEFAULT NULL,
  `balance_increment` decimal(6,2) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  KEY `ledger_account_id` (`ledger_account_id`),
  KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `transactionentry_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `transactionentry_ibfk_2` FOREIGN KEY (`ledger_account_id`) REFERENCES `configledgeraccount` (`id`),
  CONSTRAINT `transactionentry_ibfk_3` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactionentry`
--

LOCK TABLES `transactionentry` WRITE;
/*!40000 ALTER TABLE `transactionentry` DISABLE KEYS */;
INSERT INTO `transactionentry` VALUES (1,10,1,25,0,-50.00,NULL),(2,10,1,26,1,50.00,NULL),(3,12,1,25,0,-50.00,NULL),(4,12,1,26,1,50.00,NULL);
/*!40000 ALTER TABLE `transactionentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactionstatus`
--

DROP TABLE IF EXISTS `transactionstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transactionstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `details` varchar(400) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `status_id` (`status_id`),
  KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `transactionstatus_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `configtransactionstatus` (`id`),
  CONSTRAINT `transactionstatus_ibfk_2` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactionstatus`
--

LOCK TABLES `transactionstatus` WRITE;
/*!40000 ALTER TABLE `transactionstatus` DISABLE KEYS */;
INSERT INTO `transactionstatus` VALUES (10,10,2,NULL,'2016-09-17'),(12,12,2,NULL,'2016-09-17');
/*!40000 ALTER TABLE `transactionstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(25) DEFAULT NULL,
  `date_joined` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Onesmus','Mukewa','info-buyer@ajabworld.net','mkemonda','703266966',NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-20  8:42:53
