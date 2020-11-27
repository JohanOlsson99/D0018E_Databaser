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
  `Admin_ID` int(11) NOT NULL,
  `Name` VARCHAR(255) NOT NULL,
  `Username` VARCHAR(255) NOT NULL,
  `Email` VARCHAR(255) NOT NULL,
  `Password` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Comments`
--

CREATE TABLE `Comments` (
  `Comments_ID` int(11) NOT NULL,
  `Customer_ID` int(11) DEFAULT NULL,
  `Admin_ID` int(11) DEFAULT NULL,
  `Product_ID` int(11) NOT NULL,
  `Comment` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Customer`
--

CREATE TABLE `Customer` (
  `Customer_ID` int(11) NOT NULL,
  `First_name` VARCHAR(255) NOT NULL,
  `Last_name` VARCHAR(255) NOT NULL,
  `Username` VARCHAR(255) NOT NULL,
  `Email` VARCHAR(255) NOT NULL,
  `Password` VARCHAR(255) NOT NULL,
  `Phone_number` int(11) DEFAULT NULL,
  `Birthday` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Order_details`
--

CREATE TABLE `Order_details` (
  `Order_details_ID` int(11) NOT NULL,
  `Customer_ID` int(11) NOT NULL,
  `status` VARCHAR(255) NOT NULL,
  `date` date NOT NULL,
  `name` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Ordered_products_list`
--

CREATE TABLE `Ordered_products_list` (
  `ordered_products_list_ID` int(11) NOT NULL,
  `Product_ID` int(11) NOT NULL,
  `Order_details_ID` int(11) NOT NULL,
  `Amount_ordered` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Tabellstruktur `Products`
--

CREATE TABLE `Products` (
  `Products_ID` int(11) NOT NULL,
  `Product_name` VARCHAR(255) NOT NULL,
  `Product_price` double(9,2) NOT NULL,
  `Product_description` VARCHAR(255) NOT NULL,
  `Products_left_in_stock` int(11) NOT NULL,
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
  ADD PRIMARY KEY (`Admin_ID`),
  ADD KEY `Username` (`Username`),
  ADD KEY `Email` (`Email`);

--
-- Index för tabell `Comments`
--
ALTER TABLE `Comments`
  ADD PRIMARY KEY (`Comments_ID`),
  ADD KEY `Customer_ID` (`Customer_ID`),
  ADD KEY `Product_ID` (`Product_ID`),
  ADD KEY `Admin_ID` (`Admin_ID`);

--
-- Index för tabell `Customer`
--
ALTER TABLE `Customer`
  ADD PRIMARY KEY (`Customer_ID`),
  ADD KEY `Email` (`Email`),
  ADD KEY `Username` (`Username`);


--
-- Index för tabell `Order_details`
--
ALTER TABLE `Order_details`
  ADD PRIMARY KEY (`Order_details_ID`),
  ADD KEY `Customer_ID` (`Customer_ID`);

--
-- Index för tabell `Ordered_products_list`
--
ALTER TABLE `Ordered_products_list`
  ADD PRIMARY KEY (`ordered_products_list_ID`),
  ADD KEY `Product_ID` (`Product_ID`),
  ADD KEY `Order_details_ID` (`Order_details_ID`);

--
-- Index för tabell `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`Products_ID`);

--
-- Restriktioner för dumpade tabeller
--

--
-- Restriktioner för tabell `Comments`
--
ALTER TABLE `Comments`
  ADD CONSTRAINT `Comments_ibfk_1` FOREIGN KEY (`Customer_ID`) REFERENCES `Customer` (`Customer_ID`),
  ADD CONSTRAINT `Comments_ibfk_2` FOREIGN KEY (`Product_ID`) REFERENCES `Products` (`Products_ID`),
  ADD CONSTRAINT `Comments_ibfk_3` FOREIGN KEY (`Admin_ID`) REFERENCES `Admin` (`Admin_ID`);

--
-- Restriktioner för tabell `Order_details`
--
ALTER TABLE `Order_details`
  ADD CONSTRAINT `Order_details_ibfk_1` FOREIGN KEY (`Customer_ID`) REFERENCES `Customer` (`Customer_ID`);

--
-- Restriktioner för tabell `Ordered products list`
--
ALTER TABLE `Ordered_products_list`
  ADD CONSTRAINT `Ordered_products_list_ibfk_1` FOREIGN KEY (`Product_ID`) REFERENCES `Products` (`Products_ID`),
  ADD CONSTRAINT `Ordered_products_list_ibfk_2` FOREIGN KEY (`Order_details_ID`) REFERENCES `Order_details` (`Order_details_ID`);

ALTER TABLE `Customer`
  ADD CONSTRAINT `Email_unique` UNIQUE KEY (`Email`),
  ADD CONSTRAINT `Username_unique` UNIQUE KEY (`Username`);

ALTER TABLE `Admin`
  ADD CONSTRAINT `Email_unique` UNIQUE KEY (`Email`),
  ADD CONSTRAINT `Username_unique` UNIQUE KEY (`Username`);

INSERT INTO `Admin`(`Admin_ID`, `Name`, `Username`, `Email`, `Password`) VALUES (0, 'Admin', 'Admin', 'Admin@gmail.com', '123');

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
