CREATE DATABASE IF NOT EXISTS tuners CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE tuners;
--
-- Table structure for table `albums`
--

CREATE TABLE IF NOT EXISTS `albums` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `artist` int(11) DEFAULT NULL,
  `image` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `albums_name_artist` (`name`,`artist`),
  KEY `albums_name` (`name`),
  KEY `albums_artist` (`artist`),
  KEY `albums_image` (`image`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Table structure for table `artists`
--

CREATE TABLE IF NOT EXISTS `artists` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `artists_name` (`name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

UNLOCK TABLES;

--
-- Table structure for table `genres`
--

CREATE TABLE IF NOT EXISTS `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `genres_name` (`name`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Table structure for table `lyrics`
--

CREATE TABLE IF NOT EXISTS `lyrics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lyrics` text COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `images_name` (`path`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
--
-- Table structure for table `tracks`
--

CREATE TABLE IF NOT EXISTS `tracks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` int(11) DEFAULT NULL,
  `artist` int(11) DEFAULT NULL,
  `album` int(11) DEFAULT NULL,
  `genre` int(11) DEFAULT NULL,
  `composer` int(11) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `comment` text COLLATE utf8_bin DEFAULT NULL,
  `tracknumber` int(11) DEFAULT NULL,
  `discnumber` int(11) DEFAULT NULL,
  `bitrate` int(11) DEFAULT NULL,
  `length` int(11) DEFAULT NULL,
  `samplerate` int(11) DEFAULT NULL,
  `filesize` int(11) DEFAULT NULL,
  `filetype` int(11) DEFAULT NULL,
  `bpm` float DEFAULT NULL,
  `createdate` int(11) DEFAULT NULL,
  `modifydate` int(11) DEFAULT NULL,
  `albumgain` float DEFAULT NULL,
  `albumpeakgain` float DEFAULT NULL,
  `trackgain` float DEFAULT NULL,
  `trackpeakgain` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tracks_url` (`url`),
  KEY `tracks_id` (`id`),
  KEY `tracks_artist` (`artist`),
  KEY `tracks_album` (`album`),
  KEY `tracks_genre` (`genre`),
  KEY `tracks_composer` (`composer`),
  KEY `tracks_year` (`year`),
  KEY `tracks_title` (`title`),
  KEY `tracks_discnumber` (`discnumber`),
  KEY `tracks_createdate` (`createdate`),
  KEY `tracks_length` (`length`),
  KEY `tracks_bitrate` (`bitrate`),
  KEY `tracks_filesize` (`filesize`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

