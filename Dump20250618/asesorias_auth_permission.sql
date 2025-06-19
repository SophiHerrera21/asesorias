-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: asesorias
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add Configuración',1,'add_configuracion'),(2,'Can change Configuración',1,'change_configuracion'),(3,'Can delete Configuración',1,'delete_configuracion'),(4,'Can view Configuración',1,'view_configuracion'),(5,'Can add Usuario',2,'add_usuario'),(6,'Can change Usuario',2,'change_usuario'),(7,'Can delete Usuario',2,'delete_usuario'),(8,'Can view Usuario',2,'view_usuario'),(9,'Can add aprendiz',3,'add_aprendiz'),(10,'Can change aprendiz',3,'change_aprendiz'),(11,'Can delete aprendiz',3,'delete_aprendiz'),(12,'Can view aprendiz',3,'view_aprendiz'),(13,'Can add asesor',4,'add_asesor'),(14,'Can change asesor',4,'change_asesor'),(15,'Can delete asesor',4,'delete_asesor'),(16,'Can view asesor',4,'view_asesor'),(17,'Can add codigo recuperacion',5,'add_codigorecuperacion'),(18,'Can change codigo recuperacion',5,'change_codigorecuperacion'),(19,'Can delete codigo recuperacion',5,'delete_codigorecuperacion'),(20,'Can view codigo recuperacion',5,'view_codigorecuperacion'),(21,'Can add coordinador',6,'add_coordinador'),(22,'Can change coordinador',6,'change_coordinador'),(23,'Can delete coordinador',6,'delete_coordinador'),(24,'Can view coordinador',6,'view_coordinador'),(25,'Can add grupo',7,'add_grupo'),(26,'Can change grupo',7,'change_grupo'),(27,'Can delete grupo',7,'delete_grupo'),(28,'Can view grupo',7,'view_grupo'),(29,'Can add notificacion',8,'add_notificacion'),(30,'Can change notificacion',8,'change_notificacion'),(31,'Can delete notificacion',8,'delete_notificacion'),(32,'Can view notificacion',8,'view_notificacion'),(33,'Can add prueba',9,'add_prueba'),(34,'Can change prueba',9,'change_prueba'),(35,'Can delete prueba',9,'delete_prueba'),(36,'Can view prueba',9,'view_prueba'),(37,'Can add reunion',10,'add_reunion'),(38,'Can change reunion',10,'change_reunion'),(39,'Can delete reunion',10,'delete_reunion'),(40,'Can view reunion',10,'view_reunion'),(41,'Can add permission',11,'add_permission'),(42,'Can change permission',11,'change_permission'),(43,'Can delete permission',11,'delete_permission'),(44,'Can view permission',11,'view_permission'),(45,'Can add group',12,'add_group'),(46,'Can change group',12,'change_group'),(47,'Can delete group',12,'delete_group'),(48,'Can view group',12,'view_group'),(49,'Can add content type',13,'add_contenttype'),(50,'Can change content type',13,'change_contenttype'),(51,'Can delete content type',13,'delete_contenttype'),(52,'Can view content type',13,'view_contenttype'),(53,'Can add Asesoría',14,'add_asesoria'),(54,'Can change Asesoría',14,'change_asesoria'),(55,'Can delete Asesoría',14,'delete_asesoria'),(56,'Can view Asesoría',14,'view_asesoria'),(57,'Can add Grupo',15,'add_grupo'),(58,'Can change Grupo',15,'change_grupo'),(59,'Can delete Grupo',15,'delete_grupo'),(60,'Can view Grupo',15,'view_grupo'),(61,'Can add Reunión',16,'add_reunion'),(62,'Can change Reunión',16,'change_reunion'),(63,'Can delete Reunión',16,'delete_reunion'),(64,'Can view Reunión',16,'view_reunion'),(65,'Can add Prueba',17,'add_prueba'),(66,'Can change Prueba',17,'change_prueba'),(67,'Can delete Prueba',17,'delete_prueba'),(68,'Can view Prueba',17,'view_prueba'),(69,'Can add Entrega de prueba',18,'add_entregaprueba'),(70,'Can change Entrega de prueba',18,'change_entregaprueba'),(71,'Can delete Entrega de prueba',18,'delete_entregaprueba'),(72,'Can view Entrega de prueba',18,'view_entregaprueba'),(73,'Can add PQRS',19,'add_pqrs'),(74,'Can change PQRS',19,'change_pqrs'),(75,'Can delete PQRS',19,'delete_pqrs'),(76,'Can view PQRS',19,'view_pqrs'),(77,'Can add Respuesta PQRS',20,'add_respuestapqrs'),(78,'Can change Respuesta PQRS',20,'change_respuestapqrs'),(79,'Can delete Respuesta PQRS',20,'delete_respuestapqrs'),(80,'Can view Respuesta PQRS',20,'view_respuestapqrs'),(81,'Can add Notificación',21,'add_notificacion'),(82,'Can change Notificación',21,'change_notificacion'),(83,'Can delete Notificación',21,'delete_notificacion'),(84,'Can view Notificación',21,'view_notificacion'),(85,'Can add log entry',22,'add_logentry'),(86,'Can change log entry',22,'change_logentry'),(87,'Can delete log entry',22,'delete_logentry'),(88,'Can view log entry',22,'view_logentry'),(89,'Can add session',23,'add_session'),(90,'Can change session',23,'change_session'),(91,'Can delete session',23,'delete_session'),(92,'Can view session',23,'view_session'),(93,'Can add site',24,'add_site'),(94,'Can change site',24,'change_site'),(95,'Can delete site',24,'delete_site'),(96,'Can view site',24,'view_site'),(97,'Can add email address',25,'add_emailaddress'),(98,'Can change email address',25,'change_emailaddress'),(99,'Can delete email address',25,'delete_emailaddress'),(100,'Can view email address',25,'view_emailaddress'),(101,'Can add email confirmation',26,'add_emailconfirmation'),(102,'Can change email confirmation',26,'change_emailconfirmation'),(103,'Can delete email confirmation',26,'delete_emailconfirmation'),(104,'Can view email confirmation',26,'view_emailconfirmation'),(105,'Can add social account',27,'add_socialaccount'),(106,'Can change social account',27,'change_socialaccount'),(107,'Can delete social account',27,'delete_socialaccount'),(108,'Can view social account',27,'view_socialaccount'),(109,'Can add social application',28,'add_socialapp'),(110,'Can change social application',28,'change_socialapp'),(111,'Can delete social application',28,'delete_socialapp'),(112,'Can view social application',28,'view_socialapp'),(113,'Can add social application token',29,'add_socialtoken'),(114,'Can change social application token',29,'change_socialtoken'),(115,'Can delete social application token',29,'delete_socialtoken'),(116,'Can view social application token',29,'view_socialtoken'),(117,'Can add componente',30,'add_componente'),(118,'Can change componente',30,'change_componente'),(119,'Can delete componente',30,'delete_componente'),(120,'Can view componente',30,'view_componente');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 18:26:04
