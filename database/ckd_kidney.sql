-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 03, 2024 at 10:23 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ckd_kidney`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `hospital`
--

CREATE TABLE `hospital` (
  `id` int(11) NOT NULL,
  `doctor` varchar(50) NOT NULL,
  `address` varchar(200) NOT NULL,
  `contact` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hospital`
--

INSERT INTO `hospital` (`id`, `doctor`, `address`, `contact`) VALUES
(1, 'DR. VENI A, MBBS, MD, DM', 'ROCKFORD NEURO CENTRE, NO-35, ACS Villas, 11th Cross', '0431 274 2121'),
(2, 'DR. R. SUNDARARAJAN, MBBS, MD', 'NEUROCENTER, No. A9, 11th Cross West, Thillai Naga', '043 1274 0865'),
(3, 'DR. ARUNRAJ EZHUMALAI, MBBS, MD', 'TIRUCHY NEURO FOUNDATION, 69 D, 8th Cross Rd', '9443023306');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `email`, `uname`, `pass`) VALUES
(1, 'Raj', 'raj@gmail.com', 'raj', '1234'),
(2, 'Dheena', 'dheena@gmail.com', 'dheena', '1234'),
(3, 'Sinduja', 'sindu@gmail.com', 'sindu', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `suggestion`
--

CREATE TABLE `suggestion` (
  `id` int(11) NOT NULL,
  `level` varchar(20) NOT NULL,
  `details` text NOT NULL,
  `doctor` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `fees` varchar(20) NOT NULL,
  `contact` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `suggestion`
--

INSERT INTO `suggestion` (`id`, `level`, `details`, `doctor`, `address`, `fees`, `contact`) VALUES
(1, 'Mild', 'Be active for 30 minutes most days of the week.', '', '', '', ''),
(2, 'Mild', 'Eat healthy Food.', '', '', '', ''),
(3, 'Moderate', 'Drink less alcohol.', '', '', '', ''),
(4, 'Moderate', 'The healthy guidelines for drinking alcohol are: For men: No more than two drinks per day, For women: No more than one drink per day.', '', '', '', ''),
(5, 'Moderate', 'Quit smoking or using tobacco.', '', '', '', ''),
(6, 'Moderate', 'Maintain your BP and Sugar level in normal.', '', '', '', ''),
(7, 'Severe', 'contact nephrologist specialist: ', 'DR. VENI A, MBBS, MD, DM', 'ROCKFORD NEURO CENTRE, NO-35, ACS Villas, 11th Cro', 'Consultation fee - R', 'Contact: 0431 274 2121, 75980 ');
