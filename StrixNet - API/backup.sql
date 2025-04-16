/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: ztna
-- ------------------------------------------------------
-- Server version	11.7.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES
(1,'IT','2025-02-20 11:55:03'),
(2,'Human Resources','2025-02-20 11:55:03'),
(3,'Finance','2025-02-20 11:55:03'),
(4,'Marketing','2025-02-20 11:55:03'),
(5,'Sales','2025-02-20 11:55:03'),
(6,'Operations','2025-02-20 11:55:03'),
(7,'Customer Support','2025-02-20 11:55:03'),
(8,'Research and Development','2025-02-20 11:55:03'),
(9,'Legal','2025-02-20 11:55:03'),
(10,'Administration','2025-02-20 11:55:03');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_auth_requests`
--

DROP TABLE IF EXISTS `device_auth_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_auth_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` char(36) NOT NULL,
  `device_name` varchar(255) NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `status` enum('pending','approved','denied') DEFAULT 'pending',
  `requested_at` timestamp NULL DEFAULT current_timestamp(),
  `responded_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_uuid` (`uuid`),
  CONSTRAINT `device_auth_requests_ibfk_1` FOREIGN KEY (`uuid`) REFERENCES `users` (`uuid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_auth_requests`
--

LOCK TABLES `device_auth_requests` WRITE;
/*!40000 ALTER TABLE `device_auth_requests` DISABLE KEYS */;
INSERT INTO `device_auth_requests` VALUES
(1,'cd0b4688-018c-11f0-bc89-74d4dd62ab7d','CursedBook','BAF17279-6CEF-4841-B4EC-74D4DD62AB7D','192.168.1.5','approved','2025-04-08 12:36:43','2025-04-08 13:52:58');
/*!40000 ALTER TABLE `device_auth_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trusted_devices`
--

DROP TABLE IF EXISTS `trusted_devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `trusted_devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` varchar(255) NOT NULL,
  `device_fingerprint` varchar(255) NOT NULL,
  `device_name` varchar(255) NOT NULL,
  `device_type` enum('desktop','laptop') NOT NULL,
  `device_os` varchar(255) NOT NULL,
  `hardware_fingerprint` varchar(255) NOT NULL,
  `last_seen` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_id` (`device_id`),
  UNIQUE KEY `device_fingerprint` (`device_fingerprint`),
  UNIQUE KEY `hardware_fingerprint` (`hardware_fingerprint`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trusted_devices`
--

LOCK TABLES `trusted_devices` WRITE;
/*!40000 ALTER TABLE `trusted_devices` DISABLE KEYS */;
INSERT INTO `trusted_devices` VALUES
(1,'BAF17279-6CEF-4841-B4EC-74D4DD62AB7D','644e7650c2afd97545220bac6915b3254c38e676f0436e4abdefb5321c65d8f7','CursedBook','laptop','Windows 11','e590ff61518790ab2f0b0d32bc81d8ddbaeb3203ad4d02160f37f8cb7cc0d07c','2025-03-15 10:52:23','2025-03-15 10:52:23');
/*!40000 ALTER TABLE `trusted_devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdevicemapping`
--

DROP TABLE IF EXISTS `userdevicemapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdevicemapping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `status` enum('active','revoked','pending') DEFAULT 'active',
  `linked_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_id` (`u_id`,`d_id`),
  KEY `d_id` (`d_id`),
  CONSTRAINT `userdevicemapping_ibfk_1` FOREIGN KEY (`u_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `userdevicemapping_ibfk_2` FOREIGN KEY (`d_id`) REFERENCES `trusted_devices` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdevicemapping`
--

LOCK TABLES `userdevicemapping` WRITE;
/*!40000 ALTER TABLE `userdevicemapping` DISABLE KEYS */;
INSERT INTO `userdevicemapping` VALUES
(1,3,1,'active','2025-03-15 11:20:05');
/*!40000 ALTER TABLE `userdevicemapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` char(36) DEFAULT uuid(),
  `email` varchar(255) NOT NULL,
  `password` text NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'aec7dd42-018c-11f0-bc89-74d4dd62ab7d','kanav@behindmethods.com','$2b$10$AB.YHEIuFSfB6cQWNQrKK.6lAgnipNXc0WbNVpEyA8zQjOs4yLWYS',1,'2025-03-15 11:00:18'),
(2,'b9a0a6f3-018c-11f0-bc89-74d4dd62ab7d','aryanSharma@behindmethods.com','$2b$10$gko.4WKlglLCPc54g4eggeuFXhp8zFqZ6.wUXIIc88O9ZjPK50AGy',1,'2025-03-15 11:00:36'),
(3,'cd0b4688-018c-11f0-bc89-74d4dd62ab7d','test@mail.com','$2b$10$dp3hCCFyHrRXNQ74HwqUo.KRXR8shxg7GEkgy0UBs8Di.Wv1WkqZq',1,'2025-03-15 11:01:09');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-04-09  4:14:19
