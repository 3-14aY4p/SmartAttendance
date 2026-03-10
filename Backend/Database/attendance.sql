-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 09, 2026 at 02:27 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_attendance`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `attendance_id` int(11) NOT NULL,
  `student_id` varchar(20) DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `classes`
--

CREATE TABLE `classes` (
  `class_id` int(11) NOT NULL,
  `class_code` varchar(20) DEFAULT NULL,
  `subject` varchar(100) DEFAULT NULL,
  `instructor` varchar(100) DEFAULT NULL,
  `semester` varchar(20) DEFAULT NULL,
  `school_year` varchar(20) DEFAULT NULL,
  `section` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `classes`
--

INSERT INTO `classes` (`class_id`, `class_code`, `subject`, `instructor`, `semester`, `school_year`, `section`) VALUES
(1, 'ICT-111', 'ICT 111 LAB', 'Mr. C.L. Gimeno', '2nd Sem', '2025-2026', 'BS CS 2-B'),
(2, 'ICT-107', 'ICT 107 LAB', 'M.E.A. Centina', '2nd Sem', '2025-2026', 'BS CS 2-B'),
(3, 'ICT-110', 'ICT 110 LAB', 'Mr. L. Barrios', '2nd Sem', '2025-2026', 'BS CS 2-B'),
(4, 'ICT-112', 'ICT 112 LEC', 'Ms. M. Escriba', '2nd Sem', '2025-2026', 'BS CS 2-B'),
(5, 'ICT-114', 'ICT 114 LAB', 'Mrs. M. Franco', '2nd Sem', '2025-2026', 'BS CS 2-B'),
(6, 'CS-101', 'CS 101 LAB', 'Mrs. J. Calfoforo', '2nd Sem', '2025-2026', 'BS CS 2-B'),
(7, 'PE-4', 'PE 4', 'Prof. J. Marfil', '2nd Sem', '2025-2026', 'BS CS 2-B'),
(8, 'GE-ELEC1', 'GE Elec 1 LEC', 'Dr. R. Torres', '2nd Sem', '2025-2026', 'BS CS 2-B');

-- --------------------------------------------------------

--
-- Table structure for table `enrollments`
--

CREATE TABLE `enrollments` (
  `student_id` varchar(20) NOT NULL,
  `class_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `enrollments`
--

INSERT INTO `enrollments` (`student_id`, `class_id`) VALUES
('2024-0117-I', 4),
('2024-0117-I', 5),
('2024-0117-I', 6),
('2024-0117-I', 7),
('2024-0117-I', 8),
('2024-0139-I', 1),
('2024-0139-I', 2),
('2024-0139-I', 3),
('2024-0139-I', 4),
('2024-0139-I', 5),
('2024-0139-I', 6),
('2024-0139-I', 7),
('2024-0139-I', 8),
('2024-0430-A', 1),
('2024-0430-A', 2),
('2024-0430-A', 3),
('2024-0430-A', 4),
('2024-0430-A', 5),
('2024-0430-A', 6),
('2024-0430-A', 7),
('2024-0430-A', 8),
('2024-0730-I', 4),
('2024-0730-I', 5),
('2024-0730-I', 6),
('2024-0730-I', 7),
('2024-0730-I', 8),
('2024-2082-I', 1),
('2024-2082-I', 2),
('2024-2082-I', 3),
('2024-2082-I', 4),
('2024-2082-I', 5),
('2024-2082-I', 6),
('2024-2082-I', 7),
('2024-2082-I', 8),
('2024-2117-A', 1),
('2024-2117-A', 2),
('2024-2117-A', 3),
('2024-2117-A', 4),
('2024-2117-A', 5),
('2024-2117-A', 6),
('2024-2117-A', 7),
('2024-2117-A', 8),
('2024-2159-A', 1),
('2024-2159-A', 2),
('2024-2159-A', 3),
('2024-2159-A', 4),
('2024-2159-A', 5),
('2024-2159-A', 6),
('2024-2159-A', 7),
('2024-2159-A', 8),
('2024-2219-I', 4),
('2024-2219-I', 5),
('2024-2219-I', 6),
('2024-2219-I', 7),
('2024-2219-I', 8),
('2024-2645-A', 1),
('2024-2645-A', 2),
('2024-2645-A', 3),
('2024-2645-A', 4),
('2024-2645-A', 5),
('2024-2645-A', 6),
('2024-2645-A', 7),
('2024-2645-A', 8),
('2024-2695-I', 4),
('2024-2695-I', 5),
('2024-2695-I', 6),
('2024-2695-I', 7),
('2024-2695-I', 8),
('2024-2780-I', 1),
('2024-2780-I', 2),
('2024-2780-I', 3),
('2024-2780-I', 4),
('2024-2780-I', 5),
('2024-2780-I', 6),
('2024-2780-I', 7),
('2024-2780-I', 8),
('2024-2940-I', 1),
('2024-2940-I', 2),
('2024-2940-I', 3),
('2024-2940-I', 4),
('2024-2940-I', 5),
('2024-2940-I', 6),
('2024-2940-I', 7),
('2024-2940-I', 8),
('2024-3925-A', 1),
('2024-3925-A', 2),
('2024-3925-A', 3),
('2024-3925-A', 4),
('2024-3925-A', 5),
('2024-3925-A', 6),
('2024-3925-A', 7),
('2024-3925-A', 8),
('2024-4103-A', 1),
('2024-4103-A', 2),
('2024-4103-A', 3),
('2024-4103-A', 4),
('2024-4103-A', 5),
('2024-4103-A', 6),
('2024-4103-A', 7),
('2024-4103-A', 8),
('2024-4329-A', 1),
('2024-4329-A', 2),
('2024-4329-A', 3),
('2024-4329-A', 4),
('2024-4329-A', 5),
('2024-4329-A', 6),
('2024-4329-A', 7),
('2024-4329-A', 8),
('2024-4418-A', 4),
('2024-4418-A', 5),
('2024-4418-A', 6),
('2024-4418-A', 7),
('2024-4418-A', 8),
('2024-4502-A', 1),
('2024-4502-A', 2),
('2024-4502-A', 3),
('2024-4502-A', 4),
('2024-4502-A', 5),
('2024-4502-A', 6),
('2024-4502-A', 7),
('2024-4502-A', 8),
('2024-4548-A', 4),
('2024-4548-A', 5),
('2024-4548-A', 6),
('2024-4548-A', 7),
('2024-4548-A', 8),
('2024-4620-I', 4),
('2024-4620-I', 5),
('2024-4620-I', 6),
('2024-4620-I', 7),
('2024-4620-I', 8),
('2024-4720-I', 1),
('2024-4720-I', 2),
('2024-4720-I', 3),
('2024-4720-I', 4),
('2024-4720-I', 5),
('2024-4720-I', 6),
('2024-4720-I', 7),
('2024-4720-I', 8),
('2024-5287-I', 1),
('2024-5287-I', 2),
('2024-5287-I', 3),
('2024-5287-I', 4),
('2024-5287-I', 5),
('2024-5287-I', 6),
('2024-5287-I', 7),
('2024-5287-I', 8),
('2024-5547-A', 1),
('2024-5547-A', 2),
('2024-5547-A', 3),
('2024-5547-A', 4),
('2024-5547-A', 5),
('2024-5547-A', 6),
('2024-5547-A', 7),
('2024-5547-A', 8),
('2024-5926-A', 1),
('2024-5926-A', 2),
('2024-5926-A', 3),
('2024-5926-A', 4),
('2024-5926-A', 5),
('2024-5926-A', 6),
('2024-5926-A', 7),
('2024-5926-A', 8),
('2024-6012-A', 4),
('2024-6012-A', 5),
('2024-6012-A', 6),
('2024-6012-A', 7),
('2024-6012-A', 8),
('2024-6243-I', 1),
('2024-6243-I', 2),
('2024-6243-I', 3),
('2024-6243-I', 4),
('2024-6243-I', 5),
('2024-6243-I', 6),
('2024-6243-I', 7),
('2024-6243-I', 8),
('2024-6325-I', 4),
('2024-6325-I', 5),
('2024-6325-I', 6),
('2024-6325-I', 7),
('2024-6325-I', 8),
('2024-6609-I', 4),
('2024-6609-I', 5),
('2024-6609-I', 6),
('2024-6609-I', 7),
('2024-6609-I', 8),
('2024-7036-I', 1),
('2024-7036-I', 2),
('2024-7036-I', 3),
('2024-7036-I', 4),
('2024-7036-I', 5),
('2024-7036-I', 6),
('2024-7036-I', 7),
('2024-7036-I', 8),
('2024-7089-I', 1),
('2024-7089-I', 2),
('2024-7089-I', 3),
('2024-7089-I', 4),
('2024-7089-I', 5),
('2024-7089-I', 6),
('2024-7089-I', 7),
('2024-7089-I', 8),
('2024-7159-A', 4),
('2024-7159-A', 5),
('2024-7159-A', 6),
('2024-7159-A', 7),
('2024-7159-A', 8),
('2024-7689-A', 1),
('2024-7689-A', 2),
('2024-7689-A', 3),
('2024-7689-A', 4),
('2024-7689-A', 5),
('2024-7689-A', 6),
('2024-7689-A', 7),
('2024-7689-A', 8),
('2024-7956-I', 1),
('2024-7956-I', 2),
('2024-7956-I', 3),
('2024-7956-I', 4),
('2024-7956-I', 5),
('2024-7956-I', 6),
('2024-7956-I', 7),
('2024-7956-I', 8),
('2024-8045-A', 4),
('2024-8045-A', 5),
('2024-8045-A', 6),
('2024-8045-A', 7),
('2024-8045-A', 8),
('2024-8088-A', 4),
('2024-8088-A', 5),
('2024-8088-A', 6),
('2024-8088-A', 7),
('2024-8088-A', 8),
('2024-8224-I', 4),
('2024-8224-I', 5),
('2024-8224-I', 6),
('2024-8224-I', 7),
('2024-8224-I', 8),
('2024-8400-I', 1),
('2024-8400-I', 2),
('2024-8400-I', 3),
('2024-8400-I', 4),
('2024-8400-I', 5),
('2024-8400-I', 6),
('2024-8400-I', 7),
('2024-8400-I', 8),
('2024-8686-A', 1),
('2024-8686-A', 2),
('2024-8686-A', 3),
('2024-8686-A', 4),
('2024-8686-A', 5),
('2024-8686-A', 6),
('2024-8686-A', 7),
('2024-8686-A', 8),
('2024-9527-A', 1),
('2024-9527-A', 2),
('2024-9527-A', 3),
('2024-9527-A', 4),
('2024-9527-A', 5),
('2024-9527-A', 6),
('2024-9527-A', 7),
('2024-9527-A', 8),
('2024-9655-A', 1),
('2024-9655-A', 2),
('2024-9655-A', 3),
('2024-9655-A', 4),
('2024-9655-A', 5),
('2024-9655-A', 6),
('2024-9655-A', 7),
('2024-9655-A', 8);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `student_id` varchar(20) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `course` varchar(50) DEFAULT NULL,
  `year_level` int(11) DEFAULT NULL,
  `section` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `name`, `course`, `year_level`, `section`) VALUES
('2024-0117-I', 'John Lizardo', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-0139-I', 'Althea Jenne Gepanayao', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-0430-A', 'Jon Aldrich Agsamosam', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-0730-I', 'Jofel Puerta', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-2082-I', 'Pia Isabella Yap', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-2117-A', 'Queen Kimberly Calimbo', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-2159-A', 'Chrishelle Valenzuela', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-2219-I', 'Marian Jane Cargason', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-2645-A', 'EJ Hechanova', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-2695-I', 'Mark Edizon De Vera', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-2780-I', 'Joyette Silao', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-2940-I', 'Anika Rafaelle Pascual', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-3925-A', 'Dustin Rain Aspera', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-4103-A', 'John Carlos Peler', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-4329-A', 'Catherine Cagud', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-4418-A', 'Ian Paul Perales', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-4502-A', 'Jeff Jayron Pusoc', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-4548-A', 'Charlene Mallorca', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-4620-I', 'Jahzel Jay Catanus', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-4720-I', 'Justin Conde', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-5287-I', 'Charles Newell Vestuir', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-5547-A', 'Tracy Marie Boholano', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-5926-A', 'Samantha Mei Torio', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-6012-A', 'Jesharie Marie Pasco', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-6243-I', 'Jazz Noca', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-6325-I', 'Alexis Prince Cabalonga', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-6609-I', 'John Michael Capagsita', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-7036-I', 'Charles Nathaniel Coronado', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-7089-I', 'Justin Garrovillo', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-7159-A', 'Ralph Josh Cordero', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-7689-A', 'Johann Czar Bactong', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-7956-I', 'Jan Sinead Tirasol', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-8045-A', 'Mariah Rexanne Vinson', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-8088-A', 'Elyssa Danielle Calera', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-8224-I', 'Nino Ronald Daviv Rey', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-8400-I', 'Lawrence John Alimen', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-8686-A', 'Tristan Pistolante', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-9527-A', 'Jethro Zyron Angeles', 'Bachelor of Science Major in Computer Science', 2, 'B'),
('2024-9655-A', 'Janah Louisse Morallos', 'Bachelor of Science Major in Computer Science', 2, 'B');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`attendance_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `class_id` (`class_id`);

--
-- Indexes for table `classes`
--
ALTER TABLE `classes`
  ADD PRIMARY KEY (`class_id`);

--
-- Indexes for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD PRIMARY KEY (`student_id`,`class_id`),
  ADD KEY `class_id` (`class_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `attendance_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `classes`
--
ALTER TABLE `classes`
  MODIFY `class_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  ADD CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`);

--
-- Constraints for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  ADD CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
