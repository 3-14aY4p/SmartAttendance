SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;

CREATE TABLE `subject` (
  `subject_id` varchar(20) NOT NULL,
  `subject_title` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`subject_id`)
);

CREATE TABLE `instructor` (
  `instructor_id` varchar(20) NOT NULL,
  `instructor_name` varchar(130) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`instructor_id`)
);

CREATE TABLE `student` (
  `student_id` varchar(20) NOT NULL,
  `first_name` varchar(75) DEFAULT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` enum('male', 'female') DEFAULT NULL,
  PRIMARY KEY (`student_id`)
);

CREATE TABLE `course` (
  `course_id` varchar(10) NOT NULL,
  `course_title` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
);

CREATE TABLE `block` (
  `block_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` varchar(10) DEFAULT NULL,
  `year_level` int(1) DEFAULT NULL,
  `section` char(1) DEFAULT NULL,
  `school_year` varchar(10) DEFAULT NULL,
  `semester` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`block_id`),
  FOREIGN KEY (`course_id`) REFERENCES `course`(`course_id`)
);

CREATE TABLE `class` (
  `class_id` int(11),
  `subject_id` varchar(20),
  `instructor_id` varchar(20),
  `block_id` int(11),
  PRIMARY KEY (`class_id`),
  FOREIGN KEY (`subject_id`) REFERENCES `subject`(`subject_id`),
  FOREIGN KEY (`instructor_id`) REFERENCES `instructor`(`instructor_id`),
  FOREIGN KEY (`block_id`) REFERENCES `block`(`block_id`)
);

CREATE TABLE `enrollment` (
  `enrollment_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) DEFAULT NULL,
  `block_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`enrollment_id`),
  FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`),
  FOREIGN KEY (`block_id`) REFERENCES `block`(`block_id`)
);

CREATE TABLE `subject_enrollment` (
  `enrollment_id` int(11) NOT NULL,
  `subject_id` varchar(20) NOT NULL,
  `instructor_id` varchar(20) NOT NULL,
  PRIMARY KEY (`enrollment_id`, `subject_id`),
  FOREIGN KEY (`enrollment_id`) REFERENCES `enrollment`(`enrollment_id`),
  FOREIGN KEY (`subject_id`) REFERENCES `subject`(`subject_id`),
  FOREIGN KEY (`instructor_id`) REFERENCES `instructor`(`instructor_id`)
);

CREATE TABLE `schedule` (
  `schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_id` int(11) DEFAULT NULL,
  `sched_start` time DEFAULT NULL,
  `sched_end` time DEFAULT NULL,
  `day_of_week` enum('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday') DEFAULT NULL,
  PRIMARY KEY (`schedule_id`),
  FOREIGN KEY (`class_id`) REFERENCES `class`(`class_id`)
);

CREATE TABLE `attendance` (
  `attendance_id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_id` varchar(20) DEFAULT NULL,
  `instructor_id` varchar(20) DEFAULT NULL,
  `student_id` varchar(20) DEFAULT NULL,
  `date` date DEFAULT curdate(),
  `time` time DEFAULT curtime(),
  `session_type` enum('regular', 'makeup') DEFAULT NULL,
  `session_start` time DEFAULT NULL,
  `session_end` time DEFAULT NULL,
  `status` enum('on time', 'late', 'absent') DEFAULT 'absent',
  PRIMARY KEY (`attendance_id`),
  FOREIGN KEY (`subject_id`) REFERENCES `subject`(`subject_id`),
  FOREIGN KEY (`instructor_id`) REFERENCES `instructor`(`instructor_id`),
  FOREIGN KEY (`student_id`) REFERENCES `student`(`student_id`)
);

COMMIT;