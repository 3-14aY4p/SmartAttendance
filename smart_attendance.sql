-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 24, 2026 at 02:41 AM
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
  `subject_id` varchar(20) DEFAULT NULL,
  `instructor_id` varchar(20) DEFAULT NULL,
  `student_id` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `is_present` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `enrollment`
--

CREATE TABLE `enrollment` (
  `enrollment_id` int(11) NOT NULL,
  `student_id` varchar(20) DEFAULT NULL,
  `semester` varchar(20) DEFAULT NULL,
  `school_year` varchar(20) DEFAULT NULL,
  `course` varchar(20) DEFAULT NULL,
  `year_level` int(11) DEFAULT NULL,
  `section` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `enrollment`
--

INSERT INTO `enrollment` (`enrollment_id`, `student_id`, `semester`, `school_year`, `course`, `year_level`, `section`) VALUES
(1, '2024-5547-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(2, '2024-2117-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(3, '2024-0139-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(4, '2024-9655-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(5, '2024-2940-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(6, '2024-5926-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(7, '2024-2159-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(8, '2024-2082-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(9, '2024-0430-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(10, '2024-8400-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(11, '2024-9527-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(12, '2024-3925-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(13, '2024-7689-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(14, '2024-4720-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(15, '2024-7159-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(16, '2024-7036-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(17, '2024-2695-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(18, '2024-7089-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(19, '2024-2645-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(20, '2024-0117-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(21, '2024-6243-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(22, '2024-4103-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(23, '2024-4418-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(24, '2024-8686-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(25, '2024-0730-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(26, '2024-4502-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(27, '2024-8224-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(28, '2024-2780-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(29, '2024-7956-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(30, '2024-5287-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(31, '2024-4329-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(32, '2024-8088-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(33, '2024-2219-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(34, '2024-4548-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(35, '2024-6012-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(36, '2024-8045-A', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(37, '2024-6325-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(38, '2024-6609-I', '2nd', '2025-2026', 'BSCS', 2, 'B'),
(39, '2024-4620-I', '2nd', '2025-2026', 'BSCS', 2, 'B');

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `instructor_id` int(11) NOT NULL,
  `instructor_name` varchar(130) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`instructor_id`, `instructor_name`) VALUES
(1, 'M. C.L. Gimeno'),
(2, 'Mr. E.A. Centina'),
(3, 'Mrs. M.F. Franco'),
(4, 'Mrs. J. Calfoforo'),
(5, 'Mr. L. Barrios'),
(6, 'Ms. M. Escriba'),
(7, 'Prof. J. Marfil'),
(8, 'Dr. R.A. Torres');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `student_id` varchar(20) NOT NULL,
  `student_name` varchar(130) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`student_id`, `student_name`) VALUES
('2024-0117-I', 'LIZARDO, JOHN LIM'),
('2024-0139-I', 'GEPANAYAO, ALTHEA JENNE SIMPAS'),
('2024-0430-A', 'AGSAMOSAM, JON ALDRICH TENIZO'),
('2024-0730-I', 'PUERTA, JOFEL BLANCO'),
('2024-2082-I', 'YAP, PIA ISABELLA TABUADA'),
('2024-2117-A', 'CALIMBO, QUEEN KIMBERLY CASQUEJO'),
('2024-2159-A', 'VALENZUELA, CHRISHELLE GICOS'),
('2024-2219-I', 'CARGASON, MARIAN JANE SAPELINO'),
('2024-2645-A', 'HECHANOVA, EJ MOVIERA'),
('2024-2695-I', 'DE VERA, MARK EDEZON SA-AVEDRA'),
('2024-2780-I', 'SILAO, JOYETTE CARDORA'),
('2024-2940-I', 'PASCUAL, ANIKA RAFAELLE TUMIBANG'),
('2024-3925-A', 'ASPERA, DUSTIN RAIN JALES'),
('2024-4103-A', 'PELER, JOHN CARLO SODUSTA'),
('2024-4329-A', 'CAGUD, CATHERINE LAMORENO'),
('2024-4418-A', 'PERALES, IAN PAUL CASTEN'),
('2024-4502-A', 'PUSOC, JEFF JAYRON VALLEJO'),
('2024-4548-A', 'MALLORCA, CHARLENE SILLA'),
('2024-4620-I', 'CATANUS, JAHZEL JAY CANTOMAYOR'),
('2024-4720-I', 'CONDE, JUSTIN GUEVARRA'),
('2024-5287-I', 'VESTUIR, CHARLES NEWELL BAGNOL'),
('2024-5547-A', 'BOHOLANO, TRACY MARIE PAGUNSAN'),
('2024-5926-A', 'TORIO, SAMANTHA MEI VANCE'),
('2024-6012-A', 'PASCO, JESHARIE MARIE ANGELES'),
('2024-6243-I', 'NOCA, JAZZ ESCRUPOLO'),
('2024-6325-I', 'CABALONGA, ALEXIS PRINCE CAPILITAN'),
('2024-6609-I', 'CAPAGSITA, JOHN MICHAEL INOCENCIO'),
('2024-7036-I', 'CORONADO, CHARLES NATHANIEL DUBRIA'),
('2024-7089-I', 'GARROVILLO, JUSTINNO SERALE'),
('2024-7159-A', 'CORDERO, RALPH JOSH DETOMAL'),
('2024-7689-A', 'BACTONG, JOHANN CZARDE ASIS'),
('2024-7956-I', 'TIRASOL, JAN SINEAD JORGE'),
('2024-8045-A', 'VINSON, MARIAH REXANNE VILLARDO'),
('2024-8088-I', 'CALERA, ELYSSA DANIELLE PUNSALAN'),
('2024-8224-I', 'REY, NIÑO RONALD DAVIV VILLANUEVA'),
('2024-8400-I', 'ALIMEN, LAWRENCE JOHN ALIMEN'),
('2024-8686-A', 'PISTOLANTE, TRISTAN DICEN'),
('2024-9527-A', 'ANGELES, JETHRO ZYRON RUEGO'),
('2024-9655-A', 'MORALLOS, JANAH LOUISSE ALBONIAN');

-- --------------------------------------------------------

--
-- Table structure for table `subject`
--

CREATE TABLE `subject` (
  `subject_id` varchar(20) NOT NULL,
  `subject_title` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subject`
--

INSERT INTO `subject` (`subject_id`, `subject_title`) VALUES
('CS-101', 'DATA SCIENCE 1 (DATA SCIENCE TOOLS AND R PROGRAMMING)'),
('GE-ELEC-1', 'ENVIRONMENTAL SCIENCE'),
('ICT-107', 'DATA STRUCTURES AND ALGORITHMS'),
('ICT-110', 'APPLICATIONS DEVELOPMENT AND EMERGING TECHNOLOGIES'),
('ICT-111', 'OBJECT ORIENTED PROGRAMMING'),
('ICT-112', 'OPERATING SYSTEMS'),
('ICT-114', 'SOFTWARE ENGINEERING 1'),
('PE-4', 'PATHFIT 4 - CHOICE OF DANCE, SPORTS, MARTIAL ARTS, GROUP EXERCISE, OUTDOOR AND ADVENTURE ACTIVITIES');

-- --------------------------------------------------------

--
-- Table structure for table `subjects_enrolled`
--

CREATE TABLE `subjects_enrolled` (
  `id` int(11) NOT NULL,
  `subject_id` varchar(20) DEFAULT NULL,
  `instructor_id` int(11) DEFAULT NULL,
  `sched_start` time DEFAULT NULL,
  `sched_end` time DEFAULT NULL,
  `weekly_slot` varchar(20) DEFAULT NULL,
  `session_label` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subjects_enrolled`
--

INSERT INTO `subjects_enrolled` (`id`, `subject_id`, `instructor_id`, `sched_start`, `sched_end`, `weekly_slot`, `session_label`) VALUES
(1, 'ICT-111', 1, '07:30:00', '09:00:00', 'Monday', 'Lab Session'),
(3, 'ICT-111', 1, '13:30:00', '15:00:00', 'Monday', 'Lecture Session'),
(4, 'PE-4', 7, '15:30:00', '17:00:00', 'Monday', 'Regular Class'),
(5, 'ICT-111', 1, '07:30:00', '09:00:00', 'Tuesday', 'Lab Session'),
(6, 'ICT-107', 2, '09:30:00', '10:00:00', 'Tuesday', 'Lab Session'),
(7, 'ICT-114', 3, '11:00:00', '12:00:00', 'Tuesday', 'Lecture Session'),
(8, 'CS-101', 4, '13:00:00', '14:30:00', 'Tuesday', 'Lecture Session'),
(9, 'ICT-107', 2, '15:30:00', '16:30:00', 'Tuesday', 'Lab Session'),
(11, 'ICT-112', 6, '10:00:00', '11:30:00', 'Wednesday', 'Lecture Session'),
(12, 'ICT-110', 5, '14:00:00', '15:00:00', 'Wednesday', 'Lab Session'),
(13, 'ICT-114', 3, '07:30:00', '09:00:00', 'Thursday', 'Lab Session'),
(14, 'CS-101', 4, '14:00:00', '15:00:00', 'Thursday', 'Lab Session'),
(15, 'GE-ELEC-1', 8, '16:30:00', '17:30:00', 'Thursday', 'Lecture Session'),
(16, 'ICT-114', 3, '07:30:00', '09:00:00', 'Friday', 'Lab Session');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`attendance_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD PRIMARY KEY (`enrollment_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`instructor_id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`);

--
-- Indexes for table `subject`
--
ALTER TABLE `subject`
  ADD PRIMARY KEY (`subject_id`);

--
-- Indexes for table `subjects_enrolled`
--
ALTER TABLE `subjects_enrolled`
  ADD PRIMARY KEY (`id`),
  ADD KEY `subject_id` (`subject_id`),
  ADD KEY `instructor_id` (`instructor_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `attendance_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `enrollment`
--
ALTER TABLE `enrollment`
  MODIFY `enrollment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `instructor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `subjects_enrolled`
--
ALTER TABLE `subjects_enrolled`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`);

--
-- Constraints for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`);

--
-- Constraints for table `subjects_enrolled`
--
ALTER TABLE `subjects_enrolled`
  ADD CONSTRAINT `subjects_enrolled_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`),
  ADD CONSTRAINT `subjects_enrolled_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
