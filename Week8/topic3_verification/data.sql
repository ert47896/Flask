-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: assignment6
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sessionid` varchar(255) DEFAULT NULL,
  `sessionid_create_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_index` (`username`),
  UNIQUE KEY `sessionid_index` (`sessionid`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Ken','apple','1234','2021-03-29 23:24:18',NULL,NULL),(2,'Albert','book','10000','2021-03-29 23:25:44',NULL,NULL),(3,'Park','rice','1000','2021-03-29 23:31:24',NULL,NULL),(4,'Annie','good','1234','2021-03-29 23:38:53',NULL,NULL),(5,'Amy','window','1234','2021-03-30 00:08:03',NULL,NULL),(6,'Volvo','car','1000','2021-03-30 00:22:12',NULL,NULL),(7,'York','new','1000','2021-03-30 12:04:26',NULL,NULL),(8,'Ghost','abcd','1111','2021-04-01 16:57:38',NULL,NULL),(9,'田豐','urus','yooo','2021-04-02 11:23:28',NULL,NULL),(10,'歐陽','queen','1234','2021-04-02 11:23:59',NULL,NULL),(11,'方洋','www','123','2021-04-02 11:25:44',NULL,NULL),(12,'戈巴','zoo','tooo','2021-04-08 10:28:53',NULL,NULL),(13,'Westbrook','player','12345a','2021-04-13 14:27:49',NULL,NULL),(14,'Jemmy','basketball','1234','2021-04-13 18:37:47',NULL,NULL),(15,'Jemmy','desk','1234','2021-04-13 18:40:04',NULL,NULL),(16,'Jeff','baseball','1234','2021-04-13 18:42:37',NULL,NULL),(17,'陳雷','singer','1234','2021-04-13 20:35:27',NULL,NULL),(18,'楊珍','y1234','1234','2021-04-14 15:17:42',NULL,NULL),(19,'宋先生','w1234','1234','2021-04-14 15:25:52',NULL,NULL),(20,'柯南','kone','1234','2021-04-14 15:51:55',NULL,NULL),(21,'田壘','sblking','1234','2021-04-14 16:52:40',NULL,NULL);
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

-- Dump completed on 2021-04-14 17:07:24
