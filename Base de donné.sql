-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : dim. 04 juin 2023 à 15:04
-- Version du serveur : 5.7.36
-- Version de PHP : 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `velibs`
--

-- --------------------------------------------------------

--
-- Structure de la table `history_change`
--

DROP TABLE IF EXISTS `history_change`;
CREATE TABLE IF NOT EXISTS `history_change` (
  `user` varchar(255) DEFAULT NULL,
  `date_insertion` datetime DEFAULT NULL,
  `table_names` varchar(255) DEFAULT NULL,
  `action` varchar(255) DEFAULT NULL,
  `station_code` varchar(30) DEFAULT NULL,
  KEY `clé_étrangère` (`station_code`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `station_information`
--

DROP TABLE IF EXISTS `station_information`;
CREATE TABLE IF NOT EXISTS `station_information` (
  `stationcode` varchar(30) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `lon` varchar(120) DEFAULT NULL,
  `lat` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`stationcode`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déclencheurs `station_information`
--
DROP TRIGGER IF EXISTS `history_delete_station_information`;
DELIMITER $$
CREATE TRIGGER `history_delete_station_information` AFTER DELETE ON `station_information` FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_information', 'delete', OLD.stationcode)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `history_insert_station_information`;
DELIMITER $$
CREATE TRIGGER `history_insert_station_information` AFTER INSERT ON `station_information` FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_information', 'insertion', NEW.stationcode)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `history_update_station_information`;
DELIMITER $$
CREATE TRIGGER `history_update_station_information` AFTER UPDATE ON `station_information` FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_information', 'update', NEW.stationcode)
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Structure de la table `station_status`
--

DROP TABLE IF EXISTS `station_status`;
CREATE TABLE IF NOT EXISTS `station_status` (
  `stationcode` varchar(30) NOT NULL,
  `is_installed` tinyint(4) DEFAULT NULL,
  `numdocksavailable` int(11) DEFAULT NULL,
  `numbikesavailable` int(11) DEFAULT NULL,
  `mechanical` int(11) DEFAULT NULL,
  `ebike` int(11) DEFAULT NULL,
  `nom_arrondissement_communes` varchar(255) DEFAULT NULL,
  `date_insertion` datetime NOT NULL,
  PRIMARY KEY (`stationcode`,`date_insertion`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déclencheurs `station_status`
--
DROP TRIGGER IF EXISTS `history_delete_station_status`;
DELIMITER $$
CREATE TRIGGER `history_delete_station_status` AFTER DELETE ON `station_status` FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_status', 'delete', OLD.stationcode)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `history_insert_station_status`;
DELIMITER $$
CREATE TRIGGER `history_insert_station_status` AFTER INSERT ON `station_status` FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_status', 'insertion', NEW.stationcode)
$$
DELIMITER ;
DROP TRIGGER IF EXISTS `history_update_station_status`;
DELIMITER $$
CREATE TRIGGER `history_update_station_status` AFTER UPDATE ON `station_status` FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_status', 'update', NEW.stationcode)
$$
DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
