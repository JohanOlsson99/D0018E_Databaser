-- phpMyAdmin SQL Dump
-- version 4.7.1
-- https://www.phpmyadmin.net/
--
-- Värd: 127.0.0.1:3306
-- Tid vid skapande: 12 nov 2020 kl 11:58
-- Serverversion: 5.7.18-log
-- PHP-version: 7.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Databas: `db990715`
--

-- --------------------------------------------------------

--
-- Tabellstruktur `Admin`
--

CREATE TABLE `Admin` (
  `Admin ID` int(11) NOT NULL,
  `Name` linestring NOT NULL,
  `Username` linestring NOT NULL,
  `Email` linestring NOT NULL,
  `Password` linestring NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Comments`
--

CREATE TABLE `Comments` (
  `Comments ID` int(11) NOT NULL,
  `Customer ID` int(11) DEFAULT NULL,
  `Admin ID` int(11) DEFAULT NULL,
  `Product ID` int(11) NOT NULL,
  `Comment` linestring NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Customer`
--

CREATE TABLE `Customer` (
  `Customer ID` int(11) NOT NULL,
  `First name` linestring NOT NULL,
  `Last name` linestring NOT NULL,
  `Username` linestring NOT NULL,
  `Email` linestring NOT NULL,
  `Password` linestring NOT NULL,
  `Phone number` int(11) DEFAULT NULL,
  `Birthday` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Order details`
--

CREATE TABLE `Order details` (
  `Order-details ID` int(11) NOT NULL,
  `Customer ID` int(11) NOT NULL,
  `status` linestring NOT NULL,
  `date` date NOT NULL,
  `name` linestring NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Ordered products list`
--

CREATE TABLE `Ordered products list` (
  `ordered-products-list ID` int(11) NOT NULL,
  `Product ID` int(11) NOT NULL,
  `Order-details ID` int(11) NOT NULL,
  `Amount ordered` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Products`
--

CREATE TABLE `Products` (
  `Products ID` int(11) NOT NULL,
  `Product name` linestring NOT NULL,
  `Product price` double NOT NULL,
  `Product description` linestring NOT NULL,
  `Products left in stock` int(11) NOT NULL,
  `Rating` int(11) DEFAULT NULL,
  `HowManyHaveRated` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

--
-- Index för dumpade tabeller
--

--
-- Index för tabell `Admin`
--
ALTER TABLE `Admin`
  ADD PRIMARY KEY (`Admin ID`);

--
-- Index för tabell `Comments`
--
ALTER TABLE `Comments`
  ADD PRIMARY KEY (`Comments ID`),
  ADD KEY `Customer ID` (`Customer ID`),
  ADD KEY `Product ID` (`Product ID`),
  ADD KEY `Admin ID` (`Admin ID`);

--
-- Index för tabell `Customer`
--
ALTER TABLE `Customer`
  ADD PRIMARY KEY (`Customer ID`);

--
-- Index för tabell `Order details`
--
ALTER TABLE `Order details`
  ADD PRIMARY KEY (`Order-details ID`),
  ADD KEY `Customer ID` (`Customer ID`);

--
-- Index för tabell `Ordered products list`
--
ALTER TABLE `Ordered products list`
  ADD PRIMARY KEY (`ordered-products-list ID`),
  ADD KEY `Product ID` (`Product ID`),
  ADD KEY `Order-details ID` (`Order-details ID`);

--
-- Index för tabell `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`Products ID`);

--
-- Restriktioner för dumpade tabeller
--

--
-- Restriktioner för tabell `Comments`
--
ALTER TABLE `Comments`
  ADD CONSTRAINT `Comments_ibfk_1` FOREIGN KEY (`Customer ID`) REFERENCES `Customer` (`Customer ID`),
  ADD CONSTRAINT `Comments_ibfk_2` FOREIGN KEY (`Product ID`) REFERENCES `Products` (`Products ID`),
  ADD CONSTRAINT `Comments_ibfk_3` FOREIGN KEY (`Admin ID`) REFERENCES `Admin` (`Admin ID`);

--
-- Restriktioner för tabell `Order details`
--
ALTER TABLE `Order details`
  ADD CONSTRAINT `Order details_ibfk_1` FOREIGN KEY (`Customer ID`) REFERENCES `Customer` (`Customer ID`);

--
-- Restriktioner för tabell `Ordered products list`
--
ALTER TABLE `Ordered products list`
  ADD CONSTRAINT `Ordered products list_ibfk_1` FOREIGN KEY (`Product ID`) REFERENCES `Products` (`Products ID`),
  ADD CONSTRAINT `Ordered products list_ibfk_2` FOREIGN KEY (`Order-details ID`) REFERENCES `Order details` (`Order-details ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
