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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-18 22:25:52.231649'),(2,'contenttypes','0002_remove_content_type_name','2025-06-18 22:25:52.375977'),(3,'auth','0001_initial','2025-06-18 22:25:52.654158'),(4,'auth','0002_alter_permission_name_max_length','2025-06-18 22:25:52.726385'),(5,'auth','0003_alter_user_email_max_length','2025-06-18 22:25:52.731950'),(6,'auth','0004_alter_user_username_opts','2025-06-18 22:25:52.737680'),(7,'auth','0005_alter_user_last_login_null','2025-06-18 22:25:52.743490'),(8,'auth','0006_require_contenttypes_0002','2025-06-18 22:25:52.747008'),(9,'auth','0007_alter_validators_add_error_messages','2025-06-18 22:25:52.752550'),(10,'auth','0008_alter_user_username_max_length','2025-06-18 22:25:52.759420'),(11,'auth','0009_alter_user_last_name_max_length','2025-06-18 22:25:52.766316'),(12,'auth','0010_alter_group_name_max_length','2025-06-18 22:25:52.780648'),(13,'auth','0011_update_proxy_permissions','2025-06-18 22:25:52.793165'),(14,'auth','0012_alter_user_first_name_max_length','2025-06-18 22:25:52.799590'),(15,'usuarios','0001_initial','2025-06-18 22:25:54.159074'),(16,'account','0001_initial','2025-06-18 22:29:18.597449'),(17,'account','0002_email_max_length','2025-06-18 22:29:18.605124'),(18,'account','0003_alter_emailaddress_create_unique_verified_email','2025-06-18 22:29:18.609399'),(19,'account','0004_alter_emailaddress_drop_unique_email','2025-06-18 22:29:18.613451'),(20,'account','0005_emailaddress_idx_upper_email','2025-06-18 22:29:18.617154'),(21,'admin','0001_initial','2025-06-18 22:30:03.570871'),(22,'admin','0002_logentry_remove_auto_add','2025-06-18 22:30:03.581189'),(23,'admin','0003_logentry_add_action_flag_choices','2025-06-18 22:30:03.593219'),(24,'componentes','0001_initial','2025-06-18 22:30:03.632234'),(25,'sessions','0001_initial','2025-06-18 22:30:03.674050'),(26,'sites','0001_initial','2025-06-18 22:30:03.701056'),(27,'sites','0002_alter_domain_unique','2025-06-18 22:30:03.724139'),(28,'socialaccount','0001_initial','2025-06-18 22:30:04.287238'),(29,'socialaccount','0002_token_max_lengths','2025-06-18 22:30:04.339671'),(30,'socialaccount','0003_extra_data_default_dict','2025-06-18 22:30:04.350849'),(31,'socialaccount','0004_app_provider_id_settings','2025-06-18 22:30:04.558573'),(32,'socialaccount','0005_socialtoken_nullable_app','2025-06-18 22:30:04.726457'),(33,'socialaccount','0006_alter_socialaccount_extra_data','2025-06-18 22:30:04.804418');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 18:26:03
