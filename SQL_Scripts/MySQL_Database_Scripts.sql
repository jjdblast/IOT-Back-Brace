-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 21, 2016 at 12:46 PM
-- Server version: 5.5.50-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `biosensor`
--

CREATE DATABASE IF NOT EXISTS biosensor;

USE biosensor;


-- --------------------------------------------------------

--
-- Table structure for table `Clients`
--

CREATE TABLE IF NOT EXISTS `Clients` (
  `clientID` int(11) NOT NULL AUTO_INCREMENT,
  `clientName` varchar(100) NOT NULL,
  PRIMARY KEY (`clientID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `Clients`
--

INSERT INTO `Clients` (`clientID`, `clientName`) VALUES
(1, 'Widgets R Us');

-- --------------------------------------------------------

--
-- Table structure for table `Devices`
--

CREATE TABLE IF NOT EXISTS `Devices` (
  `deviceID` varchar(50) NOT NULL,
  `deviceTypeID` int(11) NOT NULL,
  `deviceName` varchar(100) NOT NULL,
  `clientID` int(11) NOT NULL,
  `facilityID` int(11) NOT NULL,
  `assignedTo` varchar(150) NOT NULL,
  PRIMARY KEY (`deviceID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Devices`
--

INSERT INTO `Devices` (`deviceID`, `deviceTypeID`, `deviceName`, `clientID`, `facilityID`, `assignedTo`) VALUES
('ac423eb65d4a32', 1, 'Lumbar Brace', 1, 1, 'John Doe');

-- --------------------------------------------------------

--
-- Table structure for table `Facilities`
--

CREATE TABLE IF NOT EXISTS `Facilities` (
  `facilityID` int(11) NOT NULL AUTO_INCREMENT,
  `facilityName` varchar(100) NOT NULL,
  `clientID` int(11) NOT NULL,
  PRIMARY KEY (`facilityID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='Contains facility information' AUTO_INCREMENT=6 ;

--
-- Dumping data for table `Facilities`
--

INSERT INTO `Facilities` (`facilityID`, `facilityName`, `clientID`) VALUES
(1, 'Warehouse #1', 1),
(4, 'Warehouse #2', 1),
(5, 'Distribution Center #1', 1);

-- --------------------------------------------------------

--
-- Table structure for table `MetricTypes`
--

CREATE TABLE IF NOT EXISTS `MetricTypes` (
  `metricTypeID` int(11) NOT NULL AUTO_INCREMENT,
  `metricTypeName` varchar(100) NOT NULL,
  PRIMARY KEY (`metricTypeID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `MetricTypes`
--

INSERT INTO `MetricTypes` (`metricTypeID`, `metricTypeName`) VALUES
(1, 'Heart Rate'),
(2, 'Impact'),
(3, 'Altitude'),
(4, 'Temperature'),
(5, 'Oxygen Levels'),
(6, 'Lumbar Flexion');

-- --------------------------------------------------------

--
-- Table structure for table `Positions`
--

CREATE TABLE IF NOT EXISTS `Positions` (
  `positionID` int(11) NOT NULL,
  `positionName` varchar(50) NOT NULL,
  PRIMARY KEY (`positionID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Maps numeric position ID''s to their corresponding names.';

--
-- Dumping data for table `Positions`
--

INSERT INTO `Positions` (`positionID`, `positionName`) VALUES
(0, 'Upright'),
(1, 'Bending'),
(2, 'Stooping');

-- --------------------------------------------------------

--
-- Table structure for table `SensorReadings`
--

CREATE TABLE IF NOT EXISTS `SensorReadings` (
  `sensorReadingID` int(11) NOT NULL AUTO_INCREMENT,
  `deviceID` varchar(50) NOT NULL,
  `readingTime` datetime NOT NULL,
  `metricTypeID` int(11) NOT NULL,
  `positionID` int(11) DEFAULT NULL,
  `uomID` int(11) NOT NULL,
  `actualYaw` float NOT NULL,
  `actualPitch` float NOT NULL,
  `actualRoll` float NOT NULL,
  `setPointYaw` float NOT NULL,
  `setPointPitch` float NOT NULL,
  `setPointRoll` float NOT NULL,
  `loadDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `readingID` varchar(75) NOT NULL,
  PRIMARY KEY (`sensorReadingID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=77 ;



-- --------------------------------------------------------

--
-- Table structure for table `SensorTrainingReadings`
--

CREATE TABLE IF NOT EXISTS `SensorTrainingReadings` (
  `sensorReadingID` int(11) NOT NULL AUTO_INCREMENT,
  `deviceID` varchar(50) NOT NULL,
  `readingTime` datetime NOT NULL,
  `metricTypeID` int(11) NOT NULL,
  `uomID` int(11) NOT NULL,
  `positionID` int(11) NOT NULL,
  `actualYaw` float NOT NULL,
  `actualPitch` float NOT NULL,
  `actualRoll` float NOT NULL,
  `setPointYaw` float NOT NULL,
  `setPointPitch` float NOT NULL,
  `setPointRoll` float NOT NULL,
  `loadDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sensorReadingID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=64 ;



-- --------------------------------------------------------

--
-- Table structure for table `UnitsOfMeasure`
--

CREATE TABLE IF NOT EXISTS `UnitsOfMeasure` (
  `uomID` int(11) NOT NULL AUTO_INCREMENT,
  `uomName` varchar(50) NOT NULL,
  PRIMARY KEY (`uomID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `UnitsOfMeasure`
--

INSERT INTO `UnitsOfMeasure` (`uomID`, `uomName`) VALUES
(1, 'Degrees Fahrenheit'),
(2, 'Degrees Celsius'),
(3, 'Newtons'),
(4, 'Degree of Movement');

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_SensorReadings`
--
CREATE  VIEW `vw_SensorReadings` 
AS 
select `r`.`deviceID` AS `deviceID`,`r`.`sensorReadingID` AS `sensorReadingID`,`r`.`readingTime` AS `readingTime`,`r`.`loadDate` AS `loadDate`,`r`.`actualPitch` AS `actualPitch`,
`r`.`actualRoll` AS `actualRoll`,`r`.`actualYaw` AS `actualYaw`,`r`.`setPointPitch` AS `setPointPitch`,`r`.`setPointRoll` AS `setPointRoll`,
`r`.`setPointYaw` AS `setPointYaw`,`p`.`positionID` AS `positionID`,`p`.`positionName` AS `positionName`,`d`.`assignedTo` AS `assignedTo`,`
d`.`deviceName` AS `deviceName` 
from ((((`SensorReadings` `r` join `Positions` `p` on((`p`.`positionID` = `r`.`positionID`))) join `Devices` `d` on((`d`.`deviceID` = `r`.`deviceID`))) join `Facilities` `f` on((`f`.`facilityID` = `d`.`facilityID`))) join `Clients` `c` on((`c`.`clientID` = `d`.`clientID`)));

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
