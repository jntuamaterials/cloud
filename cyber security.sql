/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - cyber_security
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`cyber_security` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `cyber_security`;

/*Table structure for table `dp` */

DROP TABLE IF EXISTS `dp`;

CREATE TABLE `dp` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `dp` */

insert  into `dp`(`id`,`name`,`email`,`pwd`,`pno`,`addr`) values (1,'Lakshmi','lakshmi@gmail.com','Lakshmi@506','9630258741','303, AVR Buildings, Balaji Colony  Opp S.V.music College, Tirupati, Chittoor Dist, Andhra Pradesh'),(2,'Fathima','cse.takeoff@gmail.com','Fathima@506','6302589741','234, Srinihita womens hostel,\r\n balaji colony,\r\n tirupati, chittoor dist, \r\nAP');

/*Table structure for table `transfer_files` */

DROP TABLE IF EXISTS `transfer_files`;

CREATE TABLE `transfer_files` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `remail` varchar(100) DEFAULT NULL,
  `faddr` varchar(100) DEFAULT NULL,
  `taddr` varchar(100) DEFAULT NULL,
  `d1` varchar(100) DEFAULT NULL,
  `block1` text,
  `block2` text,
  `hash1` varchar(100) DEFAULT NULL,
  `hash2` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'waiting',
  `action` varchar(100) DEFAULT 'Safe',
  `attack_time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `transfer_files` */

insert  into `transfer_files`(`id`,`name`,`email`,`fname`,`remail`,`faddr`,`taddr`,`d1`,`block1`,`block2`,`hash1`,`hash2`,`status`,`action`,`attack_time`) values (14,'Fathima','lakshmi@gmail.com','cloud data','cse.takeoff@gmail.com','234, Srinihita womens hostel,','balaji colony,','2021-12-13 18:43:39.685076','ˆ\r<Äè*|tÏ[i§¦»ªd³Ì \"\ró.\ræ\Z©y$&6eº“¿.ù¾†`µF','ÚueQ‰d.ŒÊrs–ãÙþ~2Aà‚Õ,8˜×¥Ü¶„%Xõ3\nPïT’Ÿt{','0a2bbb58652ac0708935695b1e326ab7913583e9','f1766c937ce3e96f5a1a949cafad186042d43a3f','Completed','Safe',NULL),(15,'Fathima','cse.takeoff@gmail.com','AES','lakshmi@gmail.com','abcd','xyz','2022-01-24 11:18:01.535537','ˆ\r<Äè*|tÏ[i§¦»ªd³Ì \"\ró.\ræ\Z©y$&6eº“¿.ù¾†`µF','ÚueQ‰d.ŒÊrs–ãÙþ~2Aà‚Õ,8˜×¥Ü¶„%Xõ3\nPïT’Ÿt{','0a2bbb58652ac0708935695b1e326ab7913583e9','f1766c937ce3e96f5a1a949cafad186042d43a3f','waiting','Unsafe','2022-01-24 17:21:41.921171');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
