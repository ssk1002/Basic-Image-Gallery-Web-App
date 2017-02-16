-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 16, 2017 at 05:14 AM
-- Server version: 5.6.28
-- PHP Version: 7.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `image-gallery`
--

-- --------------------------------------------------------

--
-- Table structure for table `pictures`
--

CREATE TABLE `pictures` (
  `username` varchar(20) NOT NULL,
  `fpath` varchar(100) NOT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `caption` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pictures`
--

INSERT INTO `pictures` (`username`, `fpath`, `time`, `caption`) VALUES
('user1', './static/images/car.jpeg', '2017-02-15 16:33:27', 'Cool Car I found!!!'),
('user1', './static/images/bird.jpeg', '2017-02-15 16:33:47', 'Fly Birdie :)'),
('user1', './static/images/flower.jpeg', '2017-02-15 16:34:02', 'Nice Flower'),
('user1', './static/images/bridge1.jpg', '2017-02-15 16:34:16', 'Bridge and the City'),
('user2', './static/images/cat.jpeg', '2017-02-15 16:37:40', 'Kool Kat ;)'),
('user2', './static/images/road.jpg', '2017-02-15 16:37:51', 'Journey'),
('user2', './static/images/astronaut.jpg', '2017-02-15 16:38:06', 'Space baby'),
('user2', './static/images/sunset.jpeg', '2017-02-15 16:38:28', 'Goodnight'),
('user3', './static/images/lion.jpg', '2017-02-15 16:39:15', 'Roar'),
('user3', './static/images/balloon.jpg', '2017-02-15 16:39:33', '#artsy'),
('user3', './static/images/bridge.jpeg', '2017-02-15 16:39:54', 'Smokey :)'),
('user3', './static/images/city.jpg', '2017-02-15 16:40:08', 'City lights'),
('user3', './static/images/moon.jpeg', '2017-02-15 16:40:32', 'Is the Moon Cheese?');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(20) NOT NULL,
  `password` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `password`) VALUES
('user1', '202cb962ac59075b964b07152d234b70'),
('user2', '289dff07669d7a23de0ef88d2f7129e7'),
('user3', 'd81f9c1be2e08964bf9f24b15f0e4900');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pictures`
--
ALTER TABLE `pictures`
  ADD PRIMARY KEY (`username`,`time`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);
