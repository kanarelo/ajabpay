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

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_number` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `notes` varchar(400) DEFAULT NULL,
  `amount_currency_id` int(11) NOT NULL,
  `total_withdraws` decimal(18,2) DEFAULT NULL,
  `total_deposits` decimal(18,2) DEFAULT NULL,
  `txn_withdrawal_limit` decimal(18,2) DEFAULT NULL,
  `txn_deposit_limit` decimal(18,2) DEFAULT NULL,
  `daily_withdraw_limit` decimal(18,2) DEFAULT NULL,
  `daily_deposit_limit` decimal(18,2) DEFAULT NULL,
  `weekly_withdraw_limit` decimal(18,2) DEFAULT NULL,
  `weekly_deposit_limit` decimal(18,2) DEFAULT NULL,
  `monthly_withdraw_limit` decimal(18,2) DEFAULT NULL,
  `monthly_deposit_limit` decimal(18,2) DEFAULT NULL,
  `yearly_withdraw_limit` decimal(18,2) DEFAULT NULL,
  `yearly_deposit_limit` decimal(18,2) DEFAULT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_number` (`account_number`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  KEY `amount_currency_id` (`amount_currency_id`),
  CONSTRAINT `account_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `account_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  CONSTRAINT `account_ibfk_3` FOREIGN KEY (`amount_currency_id`) REFERENCES `configcurrency` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
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
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `account_id` (`account_id`),
  KEY `status_id` (`status_id`),
  KEY `approved_by_id` (`approved_by_id`),
  CONSTRAINT `accountstatus_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `accountstatus_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `configaccountstatus` (`id`),
  CONSTRAINT `accountstatus_ibfk_3` FOREIGN KEY (`approved_by_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('534d70ab0902');
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configpaypalparameter`
--

LOCK TABLES `configpaypalparameter` WRITE;
/*!40000 ALTER TABLE `configpaypalparameter` DISABLE KEYS */;
INSERT INTO `configpaypalparameter` VALUES (1,3.00,0.30,101.25,1.50,101.25,4.00,500.00,66.00,'2016-09-20 21:19:00');
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

--
-- Table structure for table `emailmessage`
--

DROP TABLE IF EXISTS `emailmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emailmessage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_type` int(11) DEFAULT NULL,
  `message_recipient` varchar(100) DEFAULT NULL,
  `message_sender` varchar(100) DEFAULT NULL,
  `delivered` tinyint(1) DEFAULT NULL,
  `date_delivered` datetime DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emailmessage`
--

LOCK TABLES `emailmessage` WRITE;
/*!40000 ALTER TABLE `emailmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `emailmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpesaprofile`
--

DROP TABLE IF EXISTS `mpesaprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mpesaprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `mobile_phone_no` varchar(25) NOT NULL,
  `registered_name` varchar(100) DEFAULT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `mobile_phone_no` (`mobile_phone_no`),
  CONSTRAINT `mpesaprofile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mpesaprofile`
--

LOCK TABLES `mpesaprofile` WRITE;
/*!40000 ALTER TABLE `mpesaprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `mpesaprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mpesatransaction`
--

DROP TABLE IF EXISTS `mpesatransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mpesatransaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mpesa_transaction_no` varchar(50) DEFAULT NULL,
  `mpesa_txn_id` varchar(50) DEFAULT NULL,
  `recipient_phone_no` varchar(50) NOT NULL,
  `total_amount` varchar(50) NOT NULL,
  `total_amount_currency` varchar(4) NOT NULL,
  `reference_id` varchar(50) DEFAULT NULL,
  `merchant_transaction_id` varchar(50) NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_approved` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `merchant_transaction_id` (`merchant_transaction_id`),
  KEY `recipient_phone_no` (`recipient_phone_no`),
  CONSTRAINT `mpesatransaction_ibfk_1` FOREIGN KEY (`merchant_transaction_id`) REFERENCES `transaction` (`transaction_no`),
  CONSTRAINT `mpesatransaction_ibfk_2` FOREIGN KEY (`recipient_phone_no`) REFERENCES `mpesaprofile` (`mobile_phone_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `paypal_profile_id` int(11) NOT NULL,
  `street_address` varchar(100) NOT NULL,
  `locality` varchar(50) NOT NULL,
  `region` varchar(50) NOT NULL,
  `postal_code` varchar(15) DEFAULT NULL,
  `country` varchar(3) NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paypal_profile_id` (`paypal_profile_id`),
  CONSTRAINT `paypaladdress_ibfk_1` FOREIGN KEY (`paypal_profile_id`) REFERENCES `paypalprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
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
  `email` varchar(100) NOT NULL,
  `paypal_user_id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `given_name` varchar(100) NOT NULL,
  `family_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `phone_number` varchar(100) NOT NULL,
  `birthday` date NOT NULL,
  `email_verified` tinyint(1) DEFAULT NULL,
  `verified_account` tinyint(1) NOT NULL,
  `account_type` varchar(10) NOT NULL,
  `account_creation_date` datetime NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `paypal_user_id` (`paypal_user_id`),
  CONSTRAINT `paypalprofile_ibfk_1` FOREIGN KEY (`email`) REFERENCES `user` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypalprofile`
--

LOCK TABLES `paypalprofile` WRITE;
/*!40000 ALTER TABLE `paypalprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `paypalprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paypaltransaction`
--

DROP TABLE IF EXISTS `paypaltransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paypaltransaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `paypal_transaction_type_code` varchar(50) NOT NULL,
  `paypal_payer_id` varchar(50) DEFAULT NULL,
  `payer_id` int(11) DEFAULT NULL,
  `paypal_transaction_id` varchar(50) DEFAULT NULL,
  `sale_id` varchar(50) DEFAULT NULL,
  `invoice_number` varchar(50) DEFAULT NULL,
  `parent_transaction_id` varchar(50) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime DEFAULT NULL,
  `state` varchar(50) NOT NULL,
  `intent` varchar(20) DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `paypal_transaction_id` (`paypal_transaction_id`),
  KEY `payer_id` (`payer_id`),
  KEY `parent_transaction_id` (`parent_transaction_id`),
  CONSTRAINT `paypaltransaction_ibfk_1` FOREIGN KEY (`payer_id`) REFERENCES `paypalprofile` (`id`),
  CONSTRAINT `paypaltransaction_ibfk_2` FOREIGN KEY (`paypal_transaction_id`) REFERENCES `transaction` (`transaction_no`),
  CONSTRAINT `paypaltransaction_ibfk_3` FOREIGN KEY (`parent_transaction_id`) REFERENCES `transaction` (`transaction_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paypaltransaction`
--

LOCK TABLES `paypaltransaction` WRITE;
/*!40000 ALTER TABLE `paypaltransaction` DISABLE KEYS */;
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
  `code` varchar(50) DEFAULT NULL,
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
  `date_updated` datetime DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
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
INSERT INTO `product` VALUES 
(1,'Paypal to M-Pesa Exchange','P2M',1,4,250.00,500.00,250.00,250.00,500.00,500.00,1000.00,1000.00,6000.00,6000.00,'2016-09-17 00:00:00','2016-09-17 00:00:00',1),
(2,'M-Pesa to Paypal Exchange','M2P',1,4,250.00,500.00,250.00,250.00,500.00,500.00,1000.00,1000.00,6000.00,6000.00,'2016-09-17 00:00:00','2016-09-17 00:00:00',1);
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
  `message_sender` varchar(15) DEFAULT NULL,
  `message_recipient` varchar(15) DEFAULT NULL,
  `sms_gateway_id` int(11) DEFAULT NULL,
  `delivered` tinyint(1) DEFAULT NULL,
  `date_delivered` datetime DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `message` varchar(320) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sms_gateway_id` (`sms_gateway_id`),
  CONSTRAINT `smsmessage_ibfk_1` FOREIGN KEY (`sms_gateway_id`) REFERENCES `configsmsgateway` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `transaction_no` (`transaction_no`),
  KEY `transaction_type_id` (`transaction_type_id`),
  KEY `account_id` (`account_id`),
  KEY `reversing_transaction_id` (`reversing_transaction_id`),
  KEY `currency_id` (`currency_id`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`transaction_type_id`) REFERENCES `configtransactiontype` (`id`),
  CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `transaction_ibfk_3` FOREIGN KEY (`reversing_transaction_id`) REFERENCES `transaction` (`id`),
  CONSTRAINT `transaction_ibfk_4` FOREIGN KEY (`currency_id`) REFERENCES `configcurrency` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
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
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `transaction_id` (`transaction_id`),
  KEY `account_id` (`account_id`),
  KEY `ledger_account_id` (`ledger_account_id`),
  CONSTRAINT `transactionentry_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`id`),
  CONSTRAINT `transactionentry_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `transactionentry_ibfk_3` FOREIGN KEY (`ledger_account_id`) REFERENCES `configledgeraccount` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactionentry`
--

LOCK TABLES `transactionentry` WRITE;
/*!40000 ALTER TABLE `transactionentry` DISABLE KEYS */;
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
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `transaction_id` (`transaction_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `transactionstatus_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`id`),
  CONSTRAINT `transactionstatus_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `configtransactionstatus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactionstatus`
--

LOCK TABLES `transactionstatus` WRITE;
/*!40000 ALTER TABLE `transactionstatus` DISABLE KEYS */;
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
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(25) NOT NULL,
  `date_joined` datetime NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `date_updated` datetime NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
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

-- Dump completed on 2016-10-07  6:48:14
