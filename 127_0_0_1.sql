-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Sep 02, 2025 at 11:33 AM
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
-- Database: `650112230051_car`
--
CREATE DATABASE IF NOT EXISTS `650112230051_car` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `650112230051_car`;

-- --------------------------------------------------------

--
-- Table structure for table `cars`
--

CREATE TABLE `cars` (
  `car_id` int(11) NOT NULL COMMENT 'รหัสประจำตัวรถ ใช้แยกแต่ละคัน',
  `brand` varchar(50) NOT NULL COMMENT 'ยี่ห้อของรถ เช่น Toyota, Honda',
  `model` varchar(50) NOT NULL COMMENT 'รุ่นของรถ เช่น Camry, Civic',
  `production_year` year(4) NOT NULL COMMENT 'ปีที่ผลิตรถ เช่น 2022',
  `color` varchar(20) DEFAULT NULL COMMENT 'สีของรถ เช่น ขาว, ดำ, แดง',
  `engine_type` enum('เบนซิน','ดีเซล','ไฟฟ้า','ไฮบริด') NOT NULL COMMENT 'ประเภทของเครื่องยนต์ เช่น เบนซินหรือไฟฟ้า',
  `engine_size` decimal(3,1) DEFAULT NULL COMMENT 'ขนาดของเครื่องยนต์ หน่วยเป็นลิตร เช่น 1.5, 2.0',
  `price` decimal(10,2) DEFAULT NULL COMMENT 'ราคาขายของรถ หน่วยบาท เช่น 1500000.00',
  `created_date` date DEFAULT curdate() COMMENT 'วันที่เพิ่มข้อมูลลงในระบบ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cars`
--

INSERT INTO `cars` (`car_id`, `brand`, `model`, `production_year`, `color`, `engine_type`, `engine_size`, `price`, `created_date`) VALUES
(3, 'Toyota', 'Camry', '2021', 'Black', 'เบนซิน', 2.5, 1500000.00, '2025-01-07'),
(4, 'Honda', 'Civic', '2020', 'White', 'ดีเซล', 1.8, 1200000.00, '2025-01-07'),
(5, 'Nissan', 'Almera', '2022', 'Blue', 'ไฮบริด', 1.5, 1000000.00, '2025-01-07'),
(6, 'Mitsubishi', 'Pajero', '2019', 'Red', 'เบนซิน', 3.2, 1800000.00, '2025-01-07'),
(7, 'Tesla', 'Model 3', '2023', 'Silver', 'ไฟฟ้า', 0.0, 2500000.00, '2025-01-07');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL COMMENT 'รหัสลูกค้า',
  `first_name` varchar(50) NOT NULL COMMENT 'ชื่อจริง',
  `last_name` varchar(50) NOT NULL COMMENT 'นามสกุล',
  `phone_number` varchar(15) NOT NULL COMMENT 'เบอร์โทรศัพท์',
  `email` varchar(100) DEFAULT NULL COMMENT 'อีเมลลูกค้า',
  `address` text DEFAULT NULL COMMENT 'ที่อยู่ลูกค้า',
  `license_number` varchar(20) NOT NULL COMMENT 'เลขใบขับขี่',
  `license_expiry` date NOT NULL COMMENT 'วันหมดอายุของใบขับขี่'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `first_name`, `last_name`, `phone_number`, `email`, `address`, `license_number`, `license_expiry`) VALUES
(1, 'John', 'Doe', '0812345678', 'john.doe@example.com', '123 Main Street, Bangkok', 'A1234567', '2025-12-31'),
(2, 'Jane', 'Smith', '0812345679', 'jane.smith@example.com', '456 Central Ave, Chiang Mai', 'B2345678', '2026-08-15'),
(3, 'Peter', 'Parker', '0812345680', 'peter.parker@example.com', '789 Riverside Rd, Phuket', 'C3456789', '2024-05-20'),
(4, 'Bruce', 'Wayne', '0812345681', 'bruce.wayne@example.com', '101 Gotham Lane, Pattaya', 'D4567890', '2027-03-10'),
(5, 'Clark', 'Kent', '0812345682', 'clark.kent@example.com', '102 Metropolis Blvd, Bangkok', 'E5678901', '2025-07-01');

-- --------------------------------------------------------

--
-- Table structure for table `maintenance`
--

CREATE TABLE `maintenance` (
  `maintenance_id` int(11) NOT NULL COMMENT 'รหัสการบำรุงรักษา',
  `car_id` int(11) NOT NULL COMMENT 'รหัสรถที่บำรุงรักษา',
  `maintenance_date` date NOT NULL COMMENT 'วันที่บำรุงรักษา',
  `description` text DEFAULT NULL COMMENT 'รายละเอียดการบำรุงรักษา',
  `cost` decimal(10,2) DEFAULT NULL COMMENT 'ค่าใช้จ่ายการบำรุงรักษา'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `maintenance`
--

INSERT INTO `maintenance` (`maintenance_id`, `car_id`, `maintenance_date`, `description`, `cost`) VALUES
(16, 3, '2025-01-01', 'เปลี่ยนยางใหม่', 8000.00),
(17, 3, '2025-01-03', 'ซ่อมเครื่องยนต์', 15000.00),
(18, 4, '2025-01-05', 'ตรวจเช็กระยะ 50,000 กม.', 3000.00),
(19, 5, '2025-01-06', 'เปลี่ยนแบตเตอรี่', 10000.00),
(20, 6, '2025-01-07', 'เปลี่ยนกรองอากาศ', 1200.00),
(21, 7, '2025-01-09', 'ซ่อมเครื่องยนต์', 5000.00);

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL COMMENT 'รหัสการชำระเงิน',
  `rental_id` int(11) NOT NULL COMMENT 'รหัสการเช่าที่ชำระเงิน',
  `payment_date` date NOT NULL COMMENT 'วันที่ชำระเงิน',
  `amount` decimal(10,2) NOT NULL COMMENT 'จำนวนเงินที่ชำระ',
  `payment_method` enum('cash','credit_card','bank_transfer') NOT NULL COMMENT 'วิธีการชำระเงิน'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `rental_id`, `payment_date`, `amount`, `payment_method`) VALUES
(11, 6, '2025-01-01', 7500.00, 'credit_card'),
(12, 7, '2025-01-02', 5200.00, 'bank_transfer'),
(13, 8, '2025-01-04', 10800.00, 'cash'),
(14, 9, '2025-01-01', 2500.00, 'credit_card'),
(15, 10, '2025-01-03', 1200.00, 'cash');

-- --------------------------------------------------------

--
-- Table structure for table `rentals`
--

CREATE TABLE `rentals` (
  `rental_id` int(11) NOT NULL COMMENT 'รหัสการเช่า',
  `car_id` int(11) NOT NULL COMMENT 'รหัสรถที่ถูกเช่า',
  `customer_id` int(11) NOT NULL COMMENT 'รหัสลูกค้าที่เช่า',
  `rental_start_date` date NOT NULL COMMENT 'วันที่เริ่มเช่า',
  `rental_end_date` date DEFAULT NULL COMMENT 'วันที่สิ้นสุดการเช่า',
  `total_price` decimal(10,2) DEFAULT NULL COMMENT 'ราคารวมสำหรับการเช่า',
  `status` enum('ongoing','completed','cancelled') DEFAULT 'ongoing' COMMENT 'สถานะการเช่า'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `rentals`
--

INSERT INTO `rentals` (`rental_id`, `car_id`, `customer_id`, `rental_start_date`, `rental_end_date`, `total_price`, `status`) VALUES
(6, 6, 1, '2025-01-01', '2025-01-05', 7500.00, 'completed'),
(7, 7, 2, '2025-01-02', '2025-01-06', 5200.00, 'completed'),
(8, 3, 3, '2025-01-03', NULL, NULL, 'ongoing'),
(9, 4, 4, '2025-01-04', '2025-01-10', 10800.00, 'completed'),
(10, 5, 5, '2025-01-01', '2025-01-02', 2500.00, 'completed');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `role_id` int(11) NOT NULL COMMENT 'รหัสระดับสิทธิ',
  `role_name` varchar(50) NOT NULL COMMENT 'ชื่อระดับสิทธิ เช่น admin, staff, customer',
  `description` text DEFAULT NULL COMMENT 'คำอธิบายเกี่ยวกับสิทธิของบทบาทนี้'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`, `description`) VALUES
(1, 'Admin', 'ผู้ดูแลระบบ มีสิทธิในการจัดการทั้งหมด'),
(2, 'Manager', 'ผู้จัดการสามารถเข้าถึงข้อมูลและการตั้งค่าบางอย่าง'),
(3, 'Employee', 'พนักงานสามารถเข้าถึงข้อมูลที่เกี่ยวข้องกับงานของตน'),
(4, 'Customer', 'ลูกค้าสามารถเข้าถึงบริการและสินค้าที่มีอยู่'),
(5, 'Guest', 'ผู้เยี่ยมชมที่สามารถเข้าถึงข้อมูลเบื้องต้น');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL COMMENT 'รหัสประจำตัวผู้ใช้',
  `username` varchar(50) NOT NULL COMMENT 'ชื่อผู้ใช้ (Username)',
  `password_hash` varchar(255) NOT NULL COMMENT 'รหัสผ่านที่ถูกเข้ารหัส',
  `first_name` varchar(50) NOT NULL COMMENT 'ชื่อจริงของผู้ใช้',
  `last_name` varchar(50) NOT NULL COMMENT 'นามสกุลของผู้ใช้',
  `email` varchar(100) NOT NULL COMMENT 'อีเมลของผู้ใช้',
  `role_id` int(11) NOT NULL COMMENT 'รหัสระดับสิทธิ',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT 'วันที่สร้างบัญชี',
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'วันที่แก้ไขข้อมูลล่าสุด'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`, `first_name`, `last_name`, `email`, `role_id`, `created_at`, `updated_at`) VALUES
(1, 'admin_user', 'hashedpassword123', 'John', 'Doe', 'admin@example.com', 1, '2025-01-07 07:24:54', '2025-01-07 07:24:54'),
(2, 'manager_user', 'hashedpassword456', 'Jane', 'Smith', 'manager@example.com', 2, '2025-01-07 07:24:54', '2025-01-07 07:24:54'),
(3, 'employee_user', 'hashedpassword789', 'Michael', 'Johnson', 'employee@example.com', 3, '2025-01-07 07:24:54', '2025-01-07 07:24:54'),
(4, 'customer_user', 'hashedpassword101', 'Emily', 'Davis', 'customer@example.com', 4, '2025-01-07 07:24:54', '2025-01-07 07:24:54'),
(5, 'guest_user', 'hashedpassword112', 'William', 'Brown', 'guest@example.com', 5, '2025-01-07 07:24:54', '2025-01-07 07:24:54');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`car_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`);

--
-- Indexes for table `maintenance`
--
ALTER TABLE `maintenance`
  ADD PRIMARY KEY (`maintenance_id`),
  ADD KEY `car_id` (`car_id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `rental_id` (`rental_id`);

--
-- Indexes for table `rentals`
--
ALTER TABLE `rentals`
  ADD PRIMARY KEY (`rental_id`),
  ADD KEY `car_id` (`car_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`),
  ADD UNIQUE KEY `role_name` (`role_name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cars`
--
ALTER TABLE `cars`
  MODIFY `car_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'รหัสประจำตัวรถ ใช้แยกแต่ละคัน', AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'รหัสลูกค้า', AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `maintenance`
--
ALTER TABLE `maintenance`
  MODIFY `maintenance_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'รหัสการบำรุงรักษา', AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'รหัสการชำระเงิน', AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `rentals`
--
ALTER TABLE `rentals`
  MODIFY `rental_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'รหัสการเช่า', AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'รหัสระดับสิทธิ', AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'รหัสประจำตัวผู้ใช้', AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `maintenance`
--
ALTER TABLE `maintenance`
  ADD CONSTRAINT `maintenance_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`);

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`rental_id`) REFERENCES `rentals` (`rental_id`);

--
-- Constraints for table `rentals`
--
ALTER TABLE `rentals`
  ADD CONSTRAINT `rentals_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`car_id`),
  ADD CONSTRAINT `rentals_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`);
--
-- Database: `dormitorymanagement`
--
CREATE DATABASE IF NOT EXISTS `dormitorymanagement` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `dormitorymanagement`;
--
-- Database: `dorm_mang`
--
CREATE DATABASE IF NOT EXISTS `dorm_mang` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `dorm_mang`;

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `rental_id` int(11) NOT NULL,
  `payment_date` date NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_method` enum('cash','bank_transfer','credit_card') DEFAULT NULL,
  `status` enum('pending','completed','failed') DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `rental_id`, `payment_date`, `amount`, `payment_method`, `status`) VALUES
(1, 1, '2025-01-01', 5000.00, 'bank_transfer', 'completed'),
(2, 1, '2025-02-01', 5000.00, 'cash', 'completed'),
(3, 3, '2024-11-01', 5000.00, 'credit_card', 'completed'),
(4, 5, '2024-12-20', 7500.00, 'bank_transfer', 'completed'),
(5, 2, '2024-12-15', 12000.00, 'cash', 'completed');

-- --------------------------------------------------------

--
-- Table structure for table `rentals`
--

CREATE TABLE `rentals` (
  `rental_id` int(11) NOT NULL,
  `tenant_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('active','terminated') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `rentals`
--

INSERT INTO `rentals` (`rental_id`, `tenant_id`, `room_id`, `start_date`, `end_date`, `status`) VALUES
(1, 1, 2, '2025-01-01', NULL, 'active'),
(2, 2, 5, '2024-12-15', '2025-01-15', 'terminated'),
(3, 3, 1, '2024-11-01', NULL, 'active'),
(5, 5, 3, '2024-12-20', NULL, 'active'),
(6, 1, 2, '2025-01-01', NULL, 'active');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `room_id` int(11) NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `room_type` varchar(20) DEFAULT NULL,
  `monthly_rent` decimal(10,2) DEFAULT NULL,
  `status` enum('available','occupied','maintenance') DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`room_id`, `room_number`, `room_type`, `monthly_rent`, `status`) VALUES
(1, 'A101', 'single', 5000.00, 'available'),
(2, 'A102', 'single', 5000.00, 'occupied'),
(3, 'B201', 'double', 7500.00, 'available'),
(4, 'B202', 'double', 7500.00, 'maintenance'),
(5, 'C301', 'suite', 12000.00, 'occupied');

-- --------------------------------------------------------

--
-- Table structure for table `tenants`
--

CREATE TABLE `tenants` (
  `tenant_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `id_card_number` varchar(20) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `address` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tenants`
--

INSERT INTO `tenants` (`tenant_id`, `first_name`, `last_name`, `phone_number`, `email`, `id_card_number`, `date_of_birth`, `address`) VALUES
(1, 'John', 'Doe', '0812345678', 'john.doe@example.com', '1234567890123', '1990-01-15', '123 Main Street, City A'),
(2, 'Jane', 'Smith', '0823456789', 'jane.smith@example.com', '9876543210987', '1992-02-20', '456 Elm Street, City B'),
(3, 'Michael', 'Brown', '0834567890', 'michael.brown@example.com', '6543219876543', '1988-05-10', '789 Pine Avenue, City C'),
(4, 'Emily', 'Davis', '0845678901', 'emily.davis@example.com', '3219876543210', '1995-09-25', '101 Oak Lane, City D'),
(5, 'Daniel', 'Wilson', '0856789012', 'daniel.wilson@example.com', '5432109876543', '1993-07-18', '202 Birch Drive, City E'),
(6, 'Anjola', 'Senbanjo', '0943585977', '123@gmail.com', '12457896324', '2005-07-08', 'Buriram Rajabhat University');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `rental_id` (`rental_id`);

--
-- Indexes for table `rentals`
--
ALTER TABLE `rentals`
  ADD PRIMARY KEY (`rental_id`),
  ADD KEY `tenant_id` (`tenant_id`),
  ADD KEY `room_id` (`room_id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`room_id`),
  ADD UNIQUE KEY `room_number` (`room_number`);

--
-- Indexes for table `tenants`
--
ALTER TABLE `tenants`
  ADD PRIMARY KEY (`tenant_id`),
  ADD UNIQUE KEY `id_card_number` (`id_card_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `rentals`
--
ALTER TABLE `rentals`
  MODIFY `rental_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
  MODIFY `room_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tenants`
--
ALTER TABLE `tenants`
  MODIFY `tenant_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`rental_id`) REFERENCES `rentals` (`rental_id`);

--
-- Constraints for table `rentals`
--
ALTER TABLE `rentals`
  ADD CONSTRAINT `rentals_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`),
  ADD CONSTRAINT `rentals_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`);
--
-- Database: `housedb`
--
CREATE DATABASE IF NOT EXISTS `housedb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `housedb`;

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `role` enum('admin','super_admin') NOT NULL DEFAULT 'admin',
  `status` enum('active','inactive') NOT NULL DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `password`, `email`, `first_name`, `last_name`, `role`, `status`, `created_at`) VALUES
(2, 'admin', 'pbkdf2:sha256:1000000$gMIaCEf0O65ZPJlR$4c53575086414002210195a13fdd1b6e213e9effbfba1a8d86538618a1b01966', 'admin@example.com', 'Admin', 'User2', 'super_admin', 'active', '2025-04-05 08:59:04'),
(3, 'enny1', 'pbkdf2:sha256:260000$lNspGLyAMgXy86kf$68ec880c9d0a98c7955ad474ea6461c46ffab8120daf67c70bee113206090eec', 'enianjola@gmail.com', 'enny', 'Sen', 'admin', 'active', '2025-04-05 10:54:54');

-- --------------------------------------------------------

--
-- Table structure for table `admin_log`
--

CREATE TABLE `admin_log` (
  `id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `action_type` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin_log`
--

INSERT INTO `admin_log` (`id`, `admin_id`, `action_type`, `created_at`) VALUES
(1, 2, 'logout', '2025-04-05 14:14:10'),
(2, 3, 'login', '2025-04-05 14:14:48'),
(3, 2, 'login', '2025-04-05 14:15:16'),
(4, 2, 'login', '2025-04-06 09:10:33'),
(5, 2, 'login', '2025-04-06 09:10:36'),
(6, 2, 'login', '2025-04-07 09:53:27'),
(7, 2, 'login', '2025-04-07 11:18:51'),
(8, 3, 'login', '2025-04-07 12:00:46'),
(9, 3, 'login', '2025-04-07 12:12:25'),
(10, 3, 'login', '2025-04-08 04:10:24'),
(11, 3, 'login', '2025-04-08 04:10:37'),
(12, 3, 'logout', '2025-04-08 04:10:41'),
(13, 2, 'login', '2025-04-08 04:10:51'),
(14, 2, 'login', '2025-04-08 04:11:05'),
(15, 2, 'logout', '2025-04-08 04:18:24'),
(16, 2, 'login', '2025-04-08 04:18:34'),
(17, 2, 'logout', '2025-04-08 04:18:40'),
(18, 3, 'login', '2025-04-08 04:18:49'),
(19, 3, 'login', '2025-04-08 04:24:54'),
(20, 2, 'login', '2025-04-08 05:09:35'),
(21, 2, 'logout', '2025-04-08 05:18:53'),
(22, 2, 'login', '2025-04-08 05:19:08'),
(23, 2, 'login', '2025-04-09 05:01:55'),
(24, 3, 'login', '2025-04-09 05:06:21'),
(25, 3, 'logout', '2025-04-09 05:15:43'),
(26, 2, 'login', '2025-04-09 05:15:51'),
(27, 2, 'logout', '2025-04-09 05:19:08'),
(28, 2, 'login', '2025-04-09 05:19:17'),
(29, 2, 'logout', '2025-04-09 05:22:14'),
(30, 2, 'login', '2025-04-09 05:22:33'),
(31, 3, 'login', '2025-04-09 05:22:56'),
(32, 3, 'logout', '2025-04-09 05:23:00'),
(33, 2, 'login', '2025-04-09 05:23:08'),
(34, 2, 'logout', '2025-04-09 05:24:40'),
(35, 2, 'login', '2025-04-09 05:24:56'),
(36, 2, 'logout', '2025-04-09 05:27:30'),
(37, 2, 'login', '2025-04-09 05:27:38'),
(38, 2, 'logout', '2025-04-09 05:30:17'),
(39, 2, 'login', '2025-04-09 05:30:24'),
(40, 2, 'logout', '2025-04-09 05:33:15'),
(41, 2, 'login', '2025-04-09 05:33:23'),
(42, 2, 'logout', '2025-04-09 05:45:28'),
(43, 2, 'login', '2025-04-09 05:45:37'),
(44, 2, 'logout', '2025-04-09 05:49:40'),
(45, 2, 'login', '2025-04-09 05:50:06'),
(46, 2, 'logout', '2025-04-09 05:50:11'),
(47, 3, 'login', '2025-04-09 05:50:20'),
(48, 3, 'logout', '2025-04-09 05:54:53'),
(49, 2, 'login', '2025-04-09 05:55:01'),
(50, 2, 'logout', '2025-04-09 05:56:22'),
(51, 2, 'login', '2025-04-09 05:56:30'),
(52, 2, 'logout', '2025-04-09 05:59:26'),
(53, 2, 'login', '2025-04-09 05:59:34'),
(54, 2, 'logout', '2025-04-09 06:01:51'),
(55, 2, 'login', '2025-04-09 06:02:01'),
(56, 2, 'logout', '2025-04-09 06:03:14'),
(57, 3, 'login', '2025-04-09 06:03:35'),
(58, 3, 'logout', '2025-04-09 06:03:46'),
(59, 2, 'login', '2025-04-09 06:05:14'),
(60, 2, 'logout', '2025-04-09 06:10:48'),
(61, 3, 'login', '2025-04-09 06:10:55'),
(62, 3, 'login', '2025-04-09 07:22:41'),
(63, 3, 'logout', '2025-04-09 07:39:35'),
(64, 2, 'login', '2025-04-09 07:39:47'),
(65, 2, 'logout', '2025-04-09 08:31:14'),
(66, 2, 'login', '2025-04-09 08:31:23'),
(67, 2, 'login', '2025-04-09 09:50:00'),
(68, 2, 'logout', '2025-04-09 09:56:42'),
(69, 3, 'login', '2025-04-09 09:57:07'),
(70, 2, 'login', '2025-04-10 08:03:42'),
(71, 2, 'logout', '2025-04-10 08:05:38'),
(72, 3, 'login', '2025-04-10 08:05:46'),
(73, 3, 'logout', '2025-04-10 08:10:59'),
(74, 3, 'login', '2025-04-10 08:11:06'),
(75, 3, 'login', '2025-04-10 08:26:17'),
(76, 3, 'login', '2025-04-10 10:11:14'),
(77, 3, 'login', '2025-04-10 10:31:32'),
(78, 3, 'logout', '2025-04-10 10:33:38'),
(79, 3, 'login', '2025-04-10 10:34:48'),
(80, 3, 'login', '2025-04-10 11:08:54'),
(81, 2, 'login', '2025-04-10 12:53:14'),
(82, 2, 'logout', '2025-04-10 12:59:24'),
(83, 2, 'login', '2025-04-10 12:59:32'),
(84, 2, 'logout', '2025-04-10 12:59:38'),
(85, 3, 'login', '2025-04-10 13:10:31'),
(86, 3, 'logout', '2025-04-10 13:23:16'),
(87, 3, 'login', '2025-04-10 13:23:23'),
(88, 2, 'login', '2025-04-27 12:35:01'),
(89, 2, 'login', '2025-05-20 06:03:53'),
(90, 2, 'logout', '2025-05-20 06:22:09'),
(91, 3, 'login', '2025-05-20 06:22:16'),
(92, 3, 'login', '2025-05-20 06:27:17'),
(93, 2, 'login', '2025-05-20 06:28:01'),
(94, 2, 'login', '2025-05-22 09:12:00');

-- --------------------------------------------------------

--
-- Table structure for table `house`
--

CREATE TABLE `house` (
  `h_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `t_id` int(11) NOT NULL,
  `h_title` varchar(100) NOT NULL,
  `h_description` text DEFAULT NULL,
  `h_image` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `bedrooms` int(11) NOT NULL,
  `bathrooms` int(11) NOT NULL,
  `living_area` decimal(10,2) NOT NULL,
  `parking_space` tinyint(1) DEFAULT 0,
  `no_of_floors` int(11) NOT NULL,
  `features` blob DEFAULT NULL,
  `a_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `house_type`
--

CREATE TABLE `house_type` (
  `t_id` int(11) NOT NULL,
  `t_name` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `a_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `house_type`
--

INSERT INTO `house_type` (`t_id`, `t_name`, `description`, `a_id`, `created_at`, `updated_at`) VALUES
(1, '3 ห้องนอน', 'บ้านขนาด 3 ห้องนอน', 2, '2025-05-20 06:28:09', '2025-05-20 06:28:09'),
(2, '4 ห้องนอน', 'บ้านขนาด 4 ห้องนอน', 2, '2025-05-20 06:28:09', '2025-05-20 06:28:09');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `p_id` int(11) NOT NULL,
  `p_name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `a_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`p_id`, `p_name`, `description`, `address`, `a_id`, `created_at`, `updated_at`) VALUES
(1, 'โครงการขอนแก่น', NULL, 'ขอนแก่น', 2, '2025-05-20 06:28:09', '2025-05-20 06:28:09'),
(2, 'โครงการบุรีรัมย์', NULL, 'บุรีรัมย์', 2, '2025-05-20 06:28:09', '2025-05-20 06:28:09'),
(3, 'โครงการกาฬสินธุ์', NULL, 'กาฬสินธุ์', 2, '2025-05-20 06:28:09', '2025-05-20 06:28:09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `admin_log`
--
ALTER TABLE `admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `house`
--
ALTER TABLE `house`
  ADD PRIMARY KEY (`h_id`),
  ADD KEY `p_id` (`p_id`),
  ADD KEY `t_id` (`t_id`),
  ADD KEY `a_id` (`a_id`);

--
-- Indexes for table `house_type`
--
ALTER TABLE `house_type`
  ADD PRIMARY KEY (`t_id`),
  ADD KEY `a_id` (`a_id`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`p_id`),
  ADD KEY `a_id` (`a_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `admin_log`
--
ALTER TABLE `admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- AUTO_INCREMENT for table `house`
--
ALTER TABLE `house`
  MODIFY `h_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `house_type`
--
ALTER TABLE `house_type`
  MODIFY `t_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin_log`
--
ALTER TABLE `admin_log`
  ADD CONSTRAINT `admin_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`);

--
-- Constraints for table `house`
--
ALTER TABLE `house`
  ADD CONSTRAINT `house_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `projects` (`p_id`),
  ADD CONSTRAINT `house_ibfk_2` FOREIGN KEY (`t_id`) REFERENCES `house_type` (`t_id`),
  ADD CONSTRAINT `house_ibfk_3` FOREIGN KEY (`a_id`) REFERENCES `admins` (`id`);

--
-- Constraints for table `house_type`
--
ALTER TABLE `house_type`
  ADD CONSTRAINT `house_type_ibfk_1` FOREIGN KEY (`a_id`) REFERENCES `admins` (`id`);

--
-- Constraints for table `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`a_id`) REFERENCES `admins` (`id`);
--
-- Database: `movies_db`
--
CREATE DATABASE IF NOT EXISTS `movies_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `movies_db`;

-- --------------------------------------------------------

--
-- Table structure for table `audit_log`
--

CREATE TABLE `audit_log` (
  `log_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `ip_address` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `success` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `audit_log`
--

INSERT INTO `audit_log` (`log_id`, `user_id`, `action`, `ip_address`, `timestamp`, `success`) VALUES
(1, 1, 'Logged in', '192.168.1.1', '2025-02-12 00:18:24', 1),
(2, 2, 'Changed password', '192.168.1.2', '2025-02-12 00:18:24', 1),
(3, 3, 'Failed login attempt', '192.168.1.3', '2025-02-12 00:18:24', 0),
(4, 4, 'Viewed movie details', '192.168.1.4', '2025-02-12 00:18:24', 1),
(5, 5, 'Added new movie', '192.168.1.5', '2025-02-12 00:18:24', 1),
(6, 6, 'Logged out', '192.168.1.6', '2025-02-12 00:18:24', 1),
(7, 7, 'Deleted movie', '192.168.1.7', '2025-02-12 00:18:24', 1),
(8, 8, 'Updated user role', '192.168.1.8', '2025-02-12 00:18:24', 1),
(9, 9, 'Failed login attempt', '192.168.1.9', '2025-02-12 00:18:24', 0),
(10, 10, 'Viewed report', '192.168.1.10', '2025-02-12 00:18:24', 1),
(11, 11, 'Changed user settings', '192.168.1.11', '2025-02-12 00:18:24', 1),
(12, 12, 'Failed login attempt', '192.168.1.12', '2025-02-12 00:18:24', 0),
(13, 13, 'Logged in', '192.168.1.13', '2025-02-12 00:18:24', 1),
(14, 14, 'Logged out', '192.168.1.14', '2025-02-12 00:18:24', 1),
(15, 15, 'Updated profile', '192.168.1.15', '2025-02-12 00:18:24', 1),
(16, 16, 'Deleted report', '192.168.1.16', '2025-02-12 00:18:24', 1),
(17, 17, 'Created new user', '192.168.1.17', '2025-02-12 00:18:24', 1),
(18, 18, 'Changed password', '192.168.1.18', '2025-02-12 00:18:24', 1),
(19, 19, 'Failed login attempt', '192.168.1.19', '2025-02-12 00:18:24', 0),
(20, 20, 'Logged in', '192.168.1.20', '2025-02-12 00:18:24', 1);

-- --------------------------------------------------------

--
-- Table structure for table `genres`
--

CREATE TABLE `genres` (
  `genre_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `genres`
--

INSERT INTO `genres` (`genre_id`, `name`, `description`, `created_at`) VALUES
(1, 'Action', 'Movies with high energy, physical stunts, and intense sequences.', '2025-02-12 17:03:18'),
(2, 'Adventure', 'Movies that take viewers on exciting journeys or explorations.', '2025-02-12 17:03:18'),
(3, 'Animation', 'Movies that use animated graphics, CGI, or hand-drawn images.', '2025-02-12 17:03:18'),
(4, 'Biography', 'Movies based on the life stories of real people.', '2025-02-12 17:03:18'),
(5, 'Comedy', 'Movies designed to make audiences laugh with humor and satire.', '2025-02-12 17:03:18'),
(6, 'Crime', 'Movies focusing on criminal activities, investigations, and law enforcement.', '2025-02-12 17:03:18'),
(7, 'Documentary', 'Non-fiction films that explore real events and people.', '2025-02-12 17:03:18'),
(8, 'Drama', 'Movies with serious, emotional, or thought-provoking storytelling.', '2025-02-12 17:03:18'),
(9, 'Family', 'Movies suitable for audiences of all ages, often focusing on family themes.', '2025-02-12 17:03:18'),
(10, 'Fantasy', 'Movies set in magical worlds with mythical creatures and supernatural elements.', '2025-02-12 17:03:18'),
(11, 'History', 'Movies based on historical events and real-life occurrences.', '2025-02-12 17:03:18'),
(12, 'Horror', 'Movies designed to scare and thrill audiences with suspense and fear.', '2025-02-12 17:03:18'),
(13, 'Music', 'Movies centered around musical performances and themes.', '2025-02-12 17:03:18'),
(14, 'Musical', 'Movies that combine storytelling with song and dance performances.', '2025-02-12 17:03:18'),
(15, 'Mystery', 'Movies that involve solving puzzles, crimes, or uncovering secrets.', '2025-02-12 17:03:18'),
(16, 'Romance', 'Movies that focus on love stories and relationships.', '2025-02-12 17:03:18'),
(17, 'Sci-Fi', 'Movies with futuristic, scientific, and technological themes.', '2025-02-12 17:03:18'),
(18, 'Sport', 'Movies about athletes, competitions, and sports events.', '2025-02-12 17:03:18'),
(19, 'Superhero', 'Movies featuring powerful heroes and villains with extraordinary abilities.', '2025-02-12 17:03:18'),
(20, 'Thriller', 'Movies full of suspense, tension, and unexpected twists.', '2025-02-12 17:03:18'),
(21, 'War', 'Movies depicting battles, military conflicts, and wartime experiences.', '2025-02-12 17:03:18'),
(22, 'Western', 'Movies set in the American Old West with cowboys and outlaws.', '2025-02-12 17:03:18'),
(23, 'Noir', 'Dark-themed crime films with a gritty, moody aesthetic.', '2025-02-12 17:03:18'),
(24, 'Psychological', 'Movies exploring the human mind, mental states, and perception.', '2025-02-12 17:03:18'),
(25, 'Survival', 'Movies focusing on human endurance and survival against extreme conditions.', '2025-02-12 17:03:18'),
(26, 'Dark Comedy', 'Movies combining humor with dark or controversial themes.', '2025-02-12 17:03:18'),
(27, 'Cyberpunk', 'Sci-Fi movies with high-tech and dystopian futuristic settings.', '2025-02-12 17:03:18'),
(28, 'Epic', 'Movies with grand-scale storytelling, historical or fantasy-based.', '2025-02-12 17:03:18'),
(29, 'Post-Apocalyptic', 'Movies set in worlds after catastrophic events.', '2025-02-12 17:03:18'),
(30, 'Experimental', 'Movies that challenge conventional storytelling and filmmaking techniques.', '2025-02-12 17:03:18');

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE `movies` (
  `movie_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `release_date` date DEFAULT NULL,
  `duration` int(11) NOT NULL,
  `genre` int(11) DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT NULL,
  `poster_image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movies`
--

INSERT INTO `movies` (`movie_id`, `title`, `description`, `release_date`, `duration`, `genre`, `rating`, `poster_image`, `created_at`, `updated_at`) VALUES
(1, 'Inception', 'A thief who enters dreams to steal secrets is given a task to plant an idea.', '2010-07-16', 149, 7, 8.80, 'assets/img/movies/67ada3b719d9e.jpg', '2025-02-12 07:05:31', '2025-03-05 10:40:04'),
(2, 'The Dark Knight', 'Batman faces off against the Joker, a criminal mastermind causing chaos in Gotham.', '2008-07-18', 152, 9, 9.00, 'assets/img/movies/67ada3d3203fe.jpg', '2025-02-12 07:05:31', '2025-03-05 10:39:52'),
(3, 'Interstellar', 'A team of explorers travel through a wormhole in search of a new home for humanity.', '2014-11-07', 169, 13, 8.60, 'assets/img/movies/67ada3f4deeec.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(4, 'The Matrix', 'A hacker discovers the world he lives in is a simulated reality and joins a rebellion.', '1999-03-31', 136, 14, 8.70, 'assets/img/movies/67ada40b939e6.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(5, 'Titanic', 'A love story unfolds on the ill-fated Titanic voyage.', '1997-12-19', 195, 28, 7.90, 'assets/img/movies/67ada426ae6dc.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(6, 'The Godfather', 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.', '1972-03-24', 175, 12, 9.20, 'assets/img/movies/67ada4393b6e5.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(7, 'Forrest Gump', 'The story of a man with a low IQ who accomplishes incredible things.', '1994-07-06', 142, 9, 8.80, 'assets/img/movies/67ada448ad6d2.jpg', '2025-02-12 07:05:31', '2025-03-05 10:51:42'),
(8, 'Pulp Fiction', 'Interwoven stories of crime and redemption in Los Angeles.', '1994-10-14', 154, 11, 8.90, 'assets/img/movies/67ada45a7d0d7.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(9, 'Avatar', 'A paraplegic Marine explores an alien planet and joins its native inhabitants in battle.', '2009-12-18', 162, 15, 7.90, 'assets/img/movies/67ada46843ac2.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(10, 'The Shawshank Redemption', 'A man wrongly convicted of murder finds hope and friendship in prison.', '1994-09-23', 142, 1, 9.30, 'assets/img/movies/67ada49d592a4.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(11, 'The Lord of the Rings: The Fellowship of the Ring', 'A young hobbit sets out on a journey to destroy a powerful ring.', '2001-12-19', 178, 25, 8.80, 'assets/img/movies/67ada4b49fe27.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(12, 'The Lord of the Rings: The Two Towers', 'The journey continues as the fellowship faces greater threats.', '2002-12-18', 179, 11, 8.70, 'assets/img/movies/67ada4c172f07.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(13, 'The Lord of the Rings: The Return of the King', 'The final battle for Middle-earth unfolds.', '2003-12-17', 201, 26, 9.00, 'assets/img/movies/67ada4d67b7cf.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(14, 'Star Wars: A New Hope', 'A young farm boy becomes a hero in a battle against the Galactic Empire.', '1977-05-25', 121, 5, 8.60, 'assets/img/movies/67ada4e2a6b6a.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(15, 'Star Wars: The Empire Strikes Back', 'The rebels face setbacks as Darth Vader intensifies his pursuit.', '1980-05-21', 124, 8, 8.70, 'assets/img/movies/67ada4f28332c.jpg', '2025-02-12 07:05:31', '2025-03-05 10:34:01'),
(16, 'Star Wars: Return of the Jedi', 'Luke Skywalker confronts Darth Vader in a final showdown.', '1983-05-25', 131, 25, 8.30, 'assets/img/movies/67ada5033976f.jpg', '2025-02-12 07:05:31', '2025-03-05 13:34:34'),
(17, 'The Avengers', 'Earth’s mightiest heroes come together to stop an alien invasion.', '2012-04-25', 143, 1, 8.00, 'assets/img/movies/67ada51194184.jpg', '2025-02-12 07:05:31', '2025-03-05 11:34:05'),
(18, 'Avengers: Infinity War', 'The Avengers fight to stop Thanos from collecting the Infinity Stones.', '2018-04-27', 149, 1, 8.40, 'assets/img/movies/67ada52c36e66.jpg', '2025-02-12 07:05:31', '2025-03-05 13:34:48'),
(19, 'Avengers: Endgame', 'The Avengers assemble for one final battle to undo the snap.', '2019-04-26', 181, 1, 8.40, 'assets/img/movies/67ada53ed9967.jpg', '2025-02-12 07:05:31', '2025-03-05 13:34:58'),
(20, 'Joker', 'The origin story of Gotham’s infamous villain, Arthur Fleck.', '2019-10-04', 122, 26, 8.40, 'assets/img/movies/67ada54db2b39.jpg', '2025-02-12 07:05:31', '2025-03-05 11:32:16'),
(24, 'Ride Or Die', 'All the lights flashing by Got no breaks now\r\nGuess I’m feeling alive cus you’re here now\r\nWe’re a beautiful mess in the city\r\nAnd you so damn pretty\r\nYeah you so damn pretty', '2025-01-10', 306, 25, 9.90, 'assets/img/movies/movie_67ace306470f5.jpg', '2025-02-12 18:05:58', '2025-03-05 13:35:33'),
(29, 'ERht[o34ht', 'ad;lshgqo[34h', '2025-03-21', 145, 28, 7.40, 'assets/img/movies/67c855d29c7ed.jpg', '2025-03-05 11:46:35', '2025-03-05 13:46:58'),
(30, 's6rlo87;dr', 'dy8[f98][', '2025-02-24', 100, 13, 7.70, 'assets/img/movies/67c85602d6349.jpg', '2025-03-05 11:51:23', '2025-03-05 13:47:46');

-- --------------------------------------------------------

--
-- Table structure for table `movie_genres`
--

CREATE TABLE `movie_genres` (
  `movie_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `movie_keywords`
--

CREATE TABLE `movie_keywords` (
  `keyword_id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `keyword` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movie_keywords`
--

INSERT INTO `movie_keywords` (`keyword_id`, `movie_id`, `keyword`) VALUES
(1, 1, 'dreams'),
(2, 1, 'mind-bending'),
(3, 1, 'heist'),
(4, 2, 'superhero'),
(5, 2, 'joker'),
(6, 2, 'batman'),
(7, 3, 'space'),
(8, 3, 'time travel'),
(9, 3, 'black hole'),
(10, 4, 'virtual reality'),
(11, 4, 'artificial intelligence'),
(12, 4, 'cyberpunk'),
(13, 5, 'romance'),
(14, 5, 'shipwreck'),
(15, 5, 'historical'),
(16, 6, 'mafia'),
(17, 6, 'crime'),
(18, 6, 'family'),
(19, 7, 'life journey'),
(20, 7, 'vietnam war'),
(21, 7, 'drama'),
(22, 8, 'crime'),
(23, 8, 'dark humor'),
(24, 8, 'violence'),
(25, 9, 'alien planet'),
(26, 9, 'war'),
(27, 9, 'sci-fi'),
(28, 10, 'prison'),
(29, 10, 'hope'),
(30, 10, 'friendship'),
(31, 11, 'fantasy'),
(32, 11, 'magic'),
(33, 11, 'adventure'),
(34, 12, 'epic battle'),
(35, 12, 'friendship'),
(36, 12, 'middle-earth'),
(37, 13, 'final battle'),
(38, 13, 'heroism'),
(39, 13, 'redemption'),
(40, 14, 'space battle'),
(41, 14, 'rebellion'),
(42, 14, 'lightsaber'),
(43, 15, 'dark side'),
(44, 15, 'empire'),
(45, 15, 'force'),
(46, 16, 'jedi'),
(47, 16, 'redemption'),
(48, 16, 'final battle'),
(49, 17, 'superhero'),
(50, 17, 'teamwork'),
(51, 17, 'alien invasion'),
(52, 18, 'infinity stones'),
(53, 18, 'thanos'),
(54, 18, 'battle'),
(55, 19, 'time travel'),
(56, 19, 'revenge'),
(57, 19, 'final fight'),
(58, 20, 'villain origin'),
(59, 20, 'joker'),
(60, 20, 'psychological thriller');

-- --------------------------------------------------------

--
-- Table structure for table `movie_streaming`
--

CREATE TABLE `movie_streaming` (
  `movie_id` int(11) NOT NULL,
  `platform_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movie_streaming`
--

INSERT INTO `movie_streaming` (`movie_id`, `platform_id`) VALUES
(1, 1),
(1, 2),
(1, 6),
(2, 2),
(3, 3),
(4, 4),
(5, 1),
(5, 5),
(6, 6),
(7, 3),
(7, 4),
(8, 2),
(9, 1),
(9, 5),
(29, 4),
(29, 5),
(30, 4),
(30, 5);

-- --------------------------------------------------------

--
-- Table structure for table `password_reset`
--

CREATE TABLE `password_reset` (
  `reset_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `reset_token` varchar(255) NOT NULL,
  `expires_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `report_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `report_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`report_data`)),
  `generated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`report_id`, `user_id`, `report_data`, `generated_at`) VALUES
(1, 1, '{\"type\": \"movie_performance\", \"movie_id\": 5, \"views\": 3000000, \"likes\": 250000, \"dislikes\": 10000}', '2025-02-12 00:17:25'),
(2, 2, '{\"type\": \"user_activity\", \"actions\": {\"comments\": 15, \"likes\": 120, \"shares\": 5}}', '2025-02-12 00:17:25'),
(3, 3, '{\"type\": \"system_error\", \"error_code\": \"500\", \"message\": \"Internal Server Error\"}', '2025-02-12 00:17:25'),
(4, 4, '{\"type\": \"movie_performance\", \"movie_id\": 10, \"views\": 4000000, \"likes\": 350000, \"dislikes\": 15000}', '2025-02-12 00:17:25'),
(5, 5, '{\"type\": \"user_activity\", \"actions\": {\"comments\": 5, \"likes\": 60, \"shares\": 2}}', '2025-02-12 00:17:25'),
(6, 6, '{\"type\": \"content_report\", \"reported_movie\": 8, \"reason\": \"Inappropriate content\"}', '2025-02-12 00:17:25'),
(7, 7, '{\"type\": \"system_error\", \"error_code\": \"404\", \"message\": \"Movie not found\"}', '2025-02-12 00:17:25'),
(8, 8, '{\"type\": \"user_activity\", \"actions\": {\"comments\": 25, \"likes\": 200, \"shares\": 8}}', '2025-02-12 00:17:25'),
(9, 9, '{\"type\": \"movie_performance\", \"movie_id\": 15, \"views\": 2400000, \"likes\": 200000, \"dislikes\": 8500}', '2025-02-12 00:17:25'),
(10, 10, '{\"type\": \"content_report\", \"reported_movie\": 3, \"reason\": \"Copyright violation\"}', '2025-02-12 00:17:25');

-- --------------------------------------------------------

--
-- Table structure for table `statistics`
--

CREATE TABLE `statistics` (
  `stat_id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `views_count` int(11) DEFAULT 0,
  `likes_count` int(11) DEFAULT 0,
  `dislikes_count` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `statistics`
--

INSERT INTO `statistics` (`stat_id`, `movie_id`, `views_count`, `likes_count`, `dislikes_count`, `created_at`) VALUES
(1, 1, 1500001, 120000, 5000, '2025-02-12 07:16:09'),
(2, 2, 2200000, 180000, 7000, '2025-02-12 07:16:09'),
(3, 3, 1800000, 140000, 6000, '2025-02-12 07:16:09'),
(4, 4, 2500000, 210000, 8000, '2025-02-12 07:16:09'),
(5, 5, 3000000, 250000, 10000, '2025-02-12 07:16:09'),
(6, 6, 2800000, 230000, 9000, '2025-02-12 07:16:09'),
(7, 7, 2000000, 170000, 7000, '2025-02-12 07:16:09'),
(8, 8, 1700000, 150000, 6000, '2025-02-12 07:16:09'),
(9, 9, 3500000, 300000, 12000, '2025-02-12 07:16:09'),
(10, 10, 4000000, 350000, 15000, '2025-02-12 07:16:09'),
(11, 11, 3100000, 270000, 11000, '2025-02-12 07:16:09'),
(12, 12, 2600000, 220000, 9000, '2025-02-12 07:16:09'),
(13, 13, 3300000, 290000, 13000, '2025-02-12 07:16:09'),
(14, 14, 2900000, 250000, 10000, '2025-02-12 07:16:09'),
(15, 15, 2400000, 200000, 8500, '2025-02-12 07:16:09'),
(16, 16, 2700000, 230000, 9500, '2025-02-12 07:16:09'),
(17, 17, 3800000, 320000, 14000, '2025-02-12 07:16:09'),
(18, 18, 4200000, 370000, 16000, '2025-02-12 07:16:09'),
(19, 19, 3900000, 340000, 15000, '2025-02-12 07:16:09'),
(20, 20, 3100000, 280000, 12000, '2025-02-12 07:16:09'),
(21, 24, 6, 0, 0, '2025-02-13 02:34:59'),
(22, 24, 1, 0, 0, '2025-02-13 03:08:26');

-- --------------------------------------------------------

--
-- Table structure for table `streaming_platforms`
--

CREATE TABLE `streaming_platforms` (
  `platform_id` int(11) NOT NULL,
  `platform_name` varchar(100) NOT NULL,
  `logo` varchar(255) NOT NULL,
  `link` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `streaming_platforms`
--

INSERT INTO `streaming_platforms` (`platform_id`, `platform_name`, `logo`, `link`) VALUES
(1, 'Netflix', 'assets\\logo\\netflix.png', 'https://www.netflix.com/'),
(2, 'Disney+', 'assets\\logo\\disney+.png', 'https://www.hotstar.com/'),
(3, 'Amazon Prime', 'assets\\logo\\amezonprime.png', 'https://www.primevideo.com/'),
(4, 'HBO Max', 'assets\\logo\\hbomax.png', 'https://play.max.com/'),
(5, 'Hulu', 'assets\\logo\\hulu.png', 'https://www.hulu.com/'),
(6, 'Apple TV+', 'assets\\logo\\apple.png', 'https://tv.apple.com/');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `role` enum('admin','editor','viewer') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `email`, `first_name`, `last_name`, `profile_picture`, `created_at`, `last_login`, `status`, `role`) VALUES
(1, 'admin_user', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'admin@example.com', 'John', 'Doe', 'assets/img/profiles/profile_1_67b20da329bf0.jpg', '2025-02-16 12:00:55', NULL, 'active', 'admin'),
(2, 'editor_user', '$2y$10$HhM5z.h.jUJldYglMuYvYOU7A9wwT06LqZbCXj1g.LLCOvwt5321S', 'editor@example.com', 'Editor', 'User', 'path/to/profile_picture.jpg', '2025-02-16 12:00:55', NULL, 'active', 'editor'),
(3, 'viewer_user', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'viewer@example.com', 'Viewer', 'User', 'assets/img/profile/user.jpg', '2025-02-16 12:00:55', NULL, 'active', 'viewer'),
(4, 'admin', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'admin@bru.ac.th', 'anjy', 'sen', 'path/to/profile_picture.jpg', '2025-02-16 14:43:56', NULL, 'active', 'admin'),
(7, 'admin1', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'admin1@bru.ac.th', 'anjy', 'sen', 'path/to/profile_picture.jpg', '2025-02-16 14:44:54', NULL, 'active', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`role_id`, `role_name`, `description`) VALUES
(1, 'Admin', 'Has full access to all system features and settings.'),
(2, 'Editor', 'Can create, edit, and delete content, but has limited access to system settings.'),
(3, 'Viewer', 'Can view content but cannot make any changes.');

-- --------------------------------------------------------

--
-- Table structure for table `user_role_assignment`
--

CREATE TABLE `user_role_assignment` (
  `assignment_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `user_role_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_role_assignment`
--

INSERT INTO `user_role_assignment` (`assignment_id`, `user_id`, `role_id`, `user_role_id`) VALUES
(1, 1, 1, 101),
(2, 2, 2, 102),
(3, 3, 3, 103);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `genres`
--
ALTER TABLE `genres`
  ADD PRIMARY KEY (`genre_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`movie_id`),
  ADD KEY `fk_movie_genre` (`genre`);

--
-- Indexes for table `movie_genres`
--
ALTER TABLE `movie_genres`
  ADD PRIMARY KEY (`movie_id`,`genre_id`),
  ADD KEY `genre_id` (`genre_id`);

--
-- Indexes for table `movie_keywords`
--
ALTER TABLE `movie_keywords`
  ADD PRIMARY KEY (`keyword_id`),
  ADD KEY `movie_id` (`movie_id`);

--
-- Indexes for table `movie_streaming`
--
ALTER TABLE `movie_streaming`
  ADD PRIMARY KEY (`movie_id`,`platform_id`),
  ADD KEY `fk_movie_streaming_platform` (`platform_id`);

--
-- Indexes for table `statistics`
--
ALTER TABLE `statistics`
  ADD PRIMARY KEY (`stat_id`),
  ADD KEY `movie_id` (`movie_id`);

--
-- Indexes for table `streaming_platforms`
--
ALTER TABLE `streaming_platforms`
  ADD PRIMARY KEY (`platform_id`),
  ADD UNIQUE KEY `platform_name` (`platform_name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `user_role_assignment`
--
ALTER TABLE `user_role_assignment`
  ADD PRIMARY KEY (`assignment_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `genres`
--
ALTER TABLE `genres`
  MODIFY `genre_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT for table `movies`
--
ALTER TABLE `movies`
  MODIFY `movie_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `movie_keywords`
--
ALTER TABLE `movie_keywords`
  MODIFY `keyword_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `statistics`
--
ALTER TABLE `statistics`
  MODIFY `stat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `streaming_platforms`
--
ALTER TABLE `streaming_platforms`
  MODIFY `platform_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user_roles`
--
ALTER TABLE `user_roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user_role_assignment`
--
ALTER TABLE `user_role_assignment`
  MODIFY `assignment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `movies`
--
ALTER TABLE `movies`
  ADD CONSTRAINT `fk_movie_genre` FOREIGN KEY (`genre`) REFERENCES `genres` (`genre_id`);

--
-- Constraints for table `movie_genres`
--
ALTER TABLE `movie_genres`
  ADD CONSTRAINT `movie_genres_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `movie_genres_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`genre_id`) ON DELETE CASCADE;

--
-- Constraints for table `movie_keywords`
--
ALTER TABLE `movie_keywords`
  ADD CONSTRAINT `movie_keywords_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`);

--
-- Constraints for table `movie_streaming`
--
ALTER TABLE `movie_streaming`
  ADD CONSTRAINT `fk_movie_streaming_platform` FOREIGN KEY (`platform_id`) REFERENCES `streaming_platforms` (`platform_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `movie_streaming_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `movie_streaming_ibfk_2` FOREIGN KEY (`platform_id`) REFERENCES `streaming_platforms` (`platform_id`) ON DELETE CASCADE;

--
-- Constraints for table `statistics`
--
ALTER TABLE `statistics`
  ADD CONSTRAINT `statistics_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`);

--
-- Constraints for table `user_role_assignment`
--
ALTER TABLE `user_role_assignment`
  ADD CONSTRAINT `user_role_assignment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;
--
-- Database: `movies_db2`
--
CREATE DATABASE IF NOT EXISTS `movies_db2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `movies_db2`;

-- --------------------------------------------------------

--
-- Table structure for table `audit_log`
--

CREATE TABLE `audit_log` (
  `log_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `ip_address` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `success` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `audit_log`
--

INSERT INTO `audit_log` (`log_id`, `user_id`, `action`, `ip_address`, `timestamp`, `success`) VALUES
(1, 1, 'Logged in', '192.168.1.1', '2025-02-12 07:18:24', 1),
(2, 2, 'Changed password', '192.168.1.2', '2025-02-12 07:18:24', 1),
(3, 3, 'Failed login attempt', '192.168.1.3', '2025-02-12 07:18:24', 0),
(4, 4, 'Viewed movie details', '192.168.1.4', '2025-02-12 07:18:24', 1),
(5, 5, 'Added new movie', '192.168.1.5', '2025-02-12 07:18:24', 1),
(6, 6, 'Logged out', '192.168.1.6', '2025-02-12 07:18:24', 1),
(7, 7, 'Deleted movie', '192.168.1.7', '2025-02-12 07:18:24', 1),
(8, 8, 'Updated user role', '192.168.1.8', '2025-02-12 07:18:24', 1),
(9, 9, 'Failed login attempt', '192.168.1.9', '2025-02-12 07:18:24', 0),
(10, 10, 'Viewed report', '192.168.1.10', '2025-02-12 07:18:24', 1),
(11, 11, 'Changed user settings', '192.168.1.11', '2025-02-12 07:18:24', 1),
(12, 12, 'Failed login attempt', '192.168.1.12', '2025-02-12 07:18:24', 0),
(13, 13, 'Logged in', '192.168.1.13', '2025-02-12 07:18:24', 1),
(14, 14, 'Logged out', '192.168.1.14', '2025-02-12 07:18:24', 1),
(15, 15, 'Updated profile', '192.168.1.15', '2025-02-12 07:18:24', 1),
(16, 16, 'Deleted report', '192.168.1.16', '2025-02-12 07:18:24', 1),
(17, 17, 'Created new user', '192.168.1.17', '2025-02-12 07:18:24', 1),
(18, 18, 'Changed password', '192.168.1.18', '2025-02-12 07:18:24', 1),
(19, 19, 'Failed login attempt', '192.168.1.19', '2025-02-12 07:18:24', 0),
(20, 20, 'Logged in', '192.168.1.20', '2025-02-12 07:18:24', 1);

-- --------------------------------------------------------

--
-- Table structure for table `genres`
--

CREATE TABLE `genres` (
  `genre_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `genres`
--

INSERT INTO `genres` (`genre_id`, `name`, `description`, `created_at`) VALUES
(1, 'Action', 'Movies with high energy, physical stunts, and intense sequences.', '2025-02-12 17:03:18'),
(2, 'Adventure', 'Movies that take viewers on exciting journeys or explorations.', '2025-02-12 17:03:18'),
(3, 'Animation', 'Movies that use animated graphics, CGI, or hand-drawn images.', '2025-02-12 17:03:18'),
(4, 'Biography', 'Movies based on the life stories of real people.', '2025-02-12 17:03:18'),
(5, 'Comedy', 'Movies designed to make audiences laugh with humor and satire.', '2025-02-12 17:03:18'),
(6, 'Crime', 'Movies focusing on criminal activities, investigations, and law enforcement.', '2025-02-12 17:03:18'),
(7, 'Documentary', 'Non-fiction films that explore real events and people.', '2025-02-12 17:03:18'),
(8, 'Drama', 'Movies with serious, emotional, or thought-provoking storytelling.', '2025-02-12 17:03:18'),
(9, 'Family', 'Movies suitable for audiences of all ages, often focusing on family themes.', '2025-02-12 17:03:18'),
(10, 'Fantasy', 'Movies set in magical worlds with mythical creatures and supernatural elements.', '2025-02-12 17:03:18'),
(11, 'History', 'Movies based on historical events and real-life occurrences.', '2025-02-12 17:03:18'),
(12, 'Horror', 'Movies designed to scare and thrill audiences with suspense and fear.', '2025-02-12 17:03:18'),
(13, 'Music', 'Movies centered around musical performances and themes.', '2025-02-12 17:03:18'),
(14, 'Musical', 'Movies that combine storytelling with song and dance performances.', '2025-02-12 17:03:18'),
(15, 'Mystery', 'Movies that involve solving puzzles, crimes, or uncovering secrets.', '2025-02-12 17:03:18'),
(16, 'Romance', 'Movies that focus on love stories and relationships.', '2025-02-12 17:03:18'),
(17, 'Sci-Fi', 'Movies with futuristic, scientific, and technological themes.', '2025-02-12 17:03:18'),
(18, 'Sport', 'Movies about athletes, competitions, and sports events.', '2025-02-12 17:03:18'),
(19, 'Superhero', 'Movies featuring powerful heroes and villains with extraordinary abilities.', '2025-02-12 17:03:18'),
(20, 'Thriller', 'Movies full of suspense, tension, and unexpected twists.', '2025-02-12 17:03:18'),
(21, 'War', 'Movies depicting battles, military conflicts, and wartime experiences.', '2025-02-12 17:03:18'),
(22, 'Western', 'Movies set in the American Old West with cowboys and outlaws.', '2025-02-12 17:03:18'),
(23, 'Noir', 'Dark-themed crime films with a gritty, moody aesthetic.', '2025-02-12 17:03:18'),
(24, 'Psychological', 'Movies exploring the human mind, mental states, and perception.', '2025-02-12 17:03:18'),
(25, 'Survival', 'Movies focusing on human endurance and survival against extreme conditions.', '2025-02-12 17:03:18'),
(26, 'Dark Comedy', 'Movies combining humor with dark or controversial themes.', '2025-02-12 17:03:18'),
(27, 'Cyberpunk', 'Sci-Fi movies with high-tech and dystopian futuristic settings.', '2025-02-12 17:03:18'),
(28, 'Epic', 'Movies with grand-scale storytelling, historical or fantasy-based.', '2025-02-12 17:03:18'),
(29, 'Post-Apocalyptic', 'Movies set in worlds after catastrophic events.', '2025-02-12 17:03:18'),
(30, 'Experimental', 'Movies that challenge conventional storytelling and filmmaking techniques.', '2025-02-12 17:03:18');

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE `movies` (
  `movie_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `release_date` date DEFAULT NULL,
  `duration` int(11) NOT NULL,
  `genre` int(11) DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT NULL,
  `poster_image` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movies`
--

INSERT INTO `movies` (`movie_id`, `title`, `description`, `release_date`, `duration`, `genre`, `rating`, `poster_image`, `created_at`, `updated_at`) VALUES
(1, 'Inception', 'A thief who enters dreams to steal secrets is given a task to plant an idea.', '2010-07-16', 148, 4, 8.80, 'assets/img/movies/67ada3b719d9e.jpg', '2025-02-12 07:05:31', '2025-02-13 19:11:53'),
(2, 'The Dark Knight', 'Batman faces off against the Joker, a criminal mastermind causing chaos in Gotham.', '2008-07-18', 152, 13, 9.00, 'assets/img/movies/67ada3d3203fe.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(3, 'Interstellar', 'A team of explorers travel through a wormhole in search of a new home for humanity.', '2014-11-07', 169, 13, 8.60, 'assets/img/movies/67ada3f4deeec.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(4, 'The Matrix', 'A hacker discovers the world he lives in is a simulated reality and joins a rebellion.', '1999-03-31', 136, 14, 8.70, 'assets/img/movies/67ada40b939e6.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(5, 'Titanic', 'A love story unfolds on the ill-fated Titanic voyage.', '1997-12-19', 195, 28, 7.90, 'assets/img/movies/67ada426ae6dc.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(6, 'The Godfather', 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.', '1972-03-24', 175, 12, 9.20, 'assets/img/movies/67ada4393b6e5.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(7, 'Forrest Gump', 'The story of a man with a low IQ who accomplishes incredible things.', '1994-07-06', 142, 14, 8.80, 'assets/img/movies/67ada448ad6d2.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(8, 'Pulp Fiction', 'Interwoven stories of crime and redemption in Los Angeles.', '1994-10-14', 154, 11, 8.90, 'assets/img/movies/67ada45a7d0d7.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(9, 'Avatar', 'A paraplegic Marine explores an alien planet and joins its native inhabitants in battle.', '2009-12-18', 162, 15, 7.90, 'assets/img/movies/67ada46843ac2.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(10, 'The Shawshank Redemption', 'A man wrongly convicted of murder finds hope and friendship in prison.', '1994-09-23', 142, 1, 9.30, 'assets/img/movies/67ada49d592a4.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(11, 'The Lord of the Rings: The Fellowship of the Ring', 'A young hobbit sets out on a journey to destroy a powerful ring.', '2001-12-19', 178, 25, 8.80, 'assets/img/movies/67ada4b49fe27.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(12, 'The Lord of the Rings: The Two Towers', 'The journey continues as the fellowship faces greater threats.', '2002-12-18', 179, 11, 8.70, 'assets/img/movies/67ada4c172f07.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(13, 'The Lord of the Rings: The Return of the King', 'The final battle for Middle-earth unfolds.', '2003-12-17', 201, 26, 9.00, 'assets/img/movies/67ada4d67b7cf.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(14, 'Star Wars: A New Hope', 'A young farm boy becomes a hero in a battle against the Galactic Empire.', '1977-05-25', 121, 5, 8.60, 'assets/img/movies/67ada4e2a6b6a.jpg', '2025-02-12 07:05:31', '2025-02-13 19:35:03'),
(15, 'Star Wars: The Empire Strikes Back', 'The rebels face setbacks as Darth Vader intensifies his pursuit.', '1980-05-21', 124, NULL, 8.70, 'assets/img/movies/67ada4f28332c.jpg', '2025-02-12 07:05:31', '2025-02-13 07:53:22'),
(16, 'Star Wars: Return of the Jedi', 'Luke Skywalker confronts Darth Vader in a final showdown.', '1983-05-25', 131, NULL, 8.30, 'assets/img/movies/67ada5033976f.jpg', '2025-02-12 07:05:31', '2025-02-13 07:53:39'),
(17, 'The Avengers', 'Earth’s mightiest heroes come together to stop an alien invasion.', '2012-04-25', 143, NULL, 8.00, 'assets/img/movies/67ada51194184.jpg', '2025-02-12 07:05:31', '2025-02-13 07:53:53'),
(18, 'Avengers: Infinity War', 'The Avengers fight to stop Thanos from collecting the Infinity Stones.', '2018-04-27', 149, NULL, 8.40, 'assets/img/movies/67ada52c36e66.jpg', '2025-02-12 07:05:31', '2025-02-13 07:54:20'),
(19, 'Avengers: Endgame', 'The Avengers assemble for one final battle to undo the snap.', '2019-04-26', 181, NULL, 8.40, 'assets/img/movies/67ada53ed9967.jpg', '2025-02-12 07:05:31', '2025-02-13 07:54:38'),
(20, 'Joker', 'The origin story of Gotham’s infamous villain, Arthur Fleck.', '2019-10-04', 122, NULL, 8.40, 'assets/img/movies/67ada54db2b39.jpg', '2025-02-12 07:05:31', '2025-02-13 07:54:53'),
(24, 'Ride Or Die', 'All the lights flashing by Got no breaks now\r\nGuess I’m feeling alive cus you’re here now\r\nWe’re a beautiful mess in the city\r\nAnd you so damn pretty\r\nYeah you so damn pretty', '2025-01-10', 306, NULL, 9.99, 'assets/img/movies/movie_67ace306470f5.jpg', '2025-02-12 18:05:58', '2025-02-12 18:05:58');

-- --------------------------------------------------------

--
-- Table structure for table `movie_genres`
--

CREATE TABLE `movie_genres` (
  `movie_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `movie_keywords`
--

CREATE TABLE `movie_keywords` (
  `keyword_id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `keyword` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movie_keywords`
--

INSERT INTO `movie_keywords` (`keyword_id`, `movie_id`, `keyword`) VALUES
(1, 1, 'dreams'),
(2, 1, 'mind-bending'),
(3, 1, 'heist'),
(4, 2, 'superhero'),
(5, 2, 'joker'),
(6, 2, 'batman'),
(7, 3, 'space'),
(8, 3, 'time travel'),
(9, 3, 'black hole'),
(10, 4, 'virtual reality'),
(11, 4, 'artificial intelligence'),
(12, 4, 'cyberpunk'),
(13, 5, 'romance'),
(14, 5, 'shipwreck'),
(15, 5, 'historical'),
(16, 6, 'mafia'),
(17, 6, 'crime'),
(18, 6, 'family'),
(19, 7, 'life journey'),
(20, 7, 'vietnam war'),
(21, 7, 'drama'),
(22, 8, 'crime'),
(23, 8, 'dark humor'),
(24, 8, 'violence'),
(25, 9, 'alien planet'),
(26, 9, 'war'),
(27, 9, 'sci-fi'),
(28, 10, 'prison'),
(29, 10, 'hope'),
(30, 10, 'friendship'),
(31, 11, 'fantasy'),
(32, 11, 'magic'),
(33, 11, 'adventure'),
(34, 12, 'epic battle'),
(35, 12, 'friendship'),
(36, 12, 'middle-earth'),
(37, 13, 'final battle'),
(38, 13, 'heroism'),
(39, 13, 'redemption'),
(40, 14, 'space battle'),
(41, 14, 'rebellion'),
(42, 14, 'lightsaber'),
(43, 15, 'dark side'),
(44, 15, 'empire'),
(45, 15, 'force'),
(46, 16, 'jedi'),
(47, 16, 'redemption'),
(48, 16, 'final battle'),
(49, 17, 'superhero'),
(50, 17, 'teamwork'),
(51, 17, 'alien invasion'),
(52, 18, 'infinity stones'),
(53, 18, 'thanos'),
(54, 18, 'battle'),
(55, 19, 'time travel'),
(56, 19, 'revenge'),
(57, 19, 'final fight'),
(58, 20, 'villain origin'),
(59, 20, 'joker'),
(60, 20, 'psychological thriller');

-- --------------------------------------------------------

--
-- Table structure for table `movie_streaming`
--

CREATE TABLE `movie_streaming` (
  `movie_id` int(11) NOT NULL,
  `platform_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movie_streaming`
--

INSERT INTO `movie_streaming` (`movie_id`, `platform_id`) VALUES
(1, 1),
(1, 2),
(1, 6),
(2, 2),
(3, 3),
(4, 4),
(5, 1),
(5, 5),
(6, 6),
(7, 3),
(7, 4),
(8, 2),
(9, 1),
(9, 5);

-- --------------------------------------------------------

--
-- Table structure for table `password_reset`
--

CREATE TABLE `password_reset` (
  `reset_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `reset_token` varchar(255) NOT NULL,
  `expires_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `report_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `report_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`report_data`)),
  `generated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`report_id`, `user_id`, `report_data`, `generated_at`) VALUES
(1, 1, '{\"type\": \"movie_performance\", \"movie_id\": 5, \"views\": 3000000, \"likes\": 250000, \"dislikes\": 10000}', '2025-02-12 07:17:25'),
(2, 2, '{\"type\": \"user_activity\", \"actions\": {\"comments\": 15, \"likes\": 120, \"shares\": 5}}', '2025-02-12 07:17:25'),
(3, 3, '{\"type\": \"system_error\", \"error_code\": \"500\", \"message\": \"Internal Server Error\"}', '2025-02-12 07:17:25'),
(4, 4, '{\"type\": \"movie_performance\", \"movie_id\": 10, \"views\": 4000000, \"likes\": 350000, \"dislikes\": 15000}', '2025-02-12 07:17:25'),
(5, 5, '{\"type\": \"user_activity\", \"actions\": {\"comments\": 5, \"likes\": 60, \"shares\": 2}}', '2025-02-12 07:17:25'),
(6, 6, '{\"type\": \"content_report\", \"reported_movie\": 8, \"reason\": \"Inappropriate content\"}', '2025-02-12 07:17:25'),
(7, 7, '{\"type\": \"system_error\", \"error_code\": \"404\", \"message\": \"Movie not found\"}', '2025-02-12 07:17:25'),
(8, 8, '{\"type\": \"user_activity\", \"actions\": {\"comments\": 25, \"likes\": 200, \"shares\": 8}}', '2025-02-12 07:17:25'),
(9, 9, '{\"type\": \"movie_performance\", \"movie_id\": 15, \"views\": 2400000, \"likes\": 200000, \"dislikes\": 8500}', '2025-02-12 07:17:25'),
(10, 10, '{\"type\": \"content_report\", \"reported_movie\": 3, \"reason\": \"Copyright violation\"}', '2025-02-12 07:17:25');

-- --------------------------------------------------------

--
-- Table structure for table `statistics`
--

CREATE TABLE `statistics` (
  `stat_id` int(11) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `views_count` int(11) DEFAULT 0,
  `likes_count` int(11) DEFAULT 0,
  `dislikes_count` int(11) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `statistics`
--

INSERT INTO `statistics` (`stat_id`, `movie_id`, `views_count`, `likes_count`, `dislikes_count`, `created_at`) VALUES
(1, 1, 1500001, 120000, 5000, '2025-02-12 07:16:09'),
(2, 2, 2200000, 180000, 7000, '2025-02-12 07:16:09'),
(3, 3, 1800000, 140000, 6000, '2025-02-12 07:16:09'),
(4, 4, 2500000, 210000, 8000, '2025-02-12 07:16:09'),
(5, 5, 3000000, 250000, 10000, '2025-02-12 07:16:09'),
(6, 6, 2800000, 230000, 9000, '2025-02-12 07:16:09'),
(7, 7, 2000000, 170000, 7000, '2025-02-12 07:16:09'),
(8, 8, 1700000, 150000, 6000, '2025-02-12 07:16:09'),
(9, 9, 3500000, 300000, 12000, '2025-02-12 07:16:09'),
(10, 10, 4000000, 350000, 15000, '2025-02-12 07:16:09'),
(11, 11, 3100000, 270000, 11000, '2025-02-12 07:16:09'),
(12, 12, 2600000, 220000, 9000, '2025-02-12 07:16:09'),
(13, 13, 3300000, 290000, 13000, '2025-02-12 07:16:09'),
(14, 14, 2900000, 250000, 10000, '2025-02-12 07:16:09'),
(15, 15, 2400000, 200000, 8500, '2025-02-12 07:16:09'),
(16, 16, 2700000, 230000, 9500, '2025-02-12 07:16:09'),
(17, 17, 3800000, 320000, 14000, '2025-02-12 07:16:09'),
(18, 18, 4200000, 370000, 16000, '2025-02-12 07:16:09'),
(19, 19, 3900000, 340000, 15000, '2025-02-12 07:16:09'),
(20, 20, 3100000, 280000, 12000, '2025-02-12 07:16:09'),
(21, 24, 6, 0, 0, '2025-02-13 02:34:59'),
(22, 24, 1, 0, 0, '2025-02-13 03:08:26');

-- --------------------------------------------------------

--
-- Table structure for table `streaming_platforms`
--

CREATE TABLE `streaming_platforms` (
  `platform_id` int(11) NOT NULL,
  `platform_name` varchar(100) NOT NULL,
  `logo` varchar(255) NOT NULL,
  `link` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `streaming_platforms`
--

INSERT INTO `streaming_platforms` (`platform_id`, `platform_name`, `logo`, `link`) VALUES
(1, 'Netflix', 'assets\\logo\\netflix.png', 'https://www.netflix.com/'),
(2, 'Disney+', 'assets\\logo\\disney+.png', 'https://www.hotstar.com/'),
(3, 'Amazon Prime', 'assets\\logo\\amezonprime.png', 'https://www.primevideo.com/'),
(4, 'HBO Max', 'assets\\logo\\hbomax.png', 'https://play.max.com/'),
(5, 'Hulu', 'assets\\logo\\hulu.png', 'https://www.hulu.com/'),
(6, 'Apple TV+', 'assets\\logo\\apple.png', 'https://tv.apple.com/');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `status` enum('active','inactive','banned') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password_hash`, `first_name`, `last_name`, `profile_picture`, `created_at`, `last_login`, `status`) VALUES
(1, 'john_doe', 'john.doe@example.com', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'John', 'Doe', 'profile1.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(2, 'jane_smith', 'jane.smith@example.com', 'hashedpassword2', 'Jane', 'Smith', 'profile2.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'inactive'),
(3, 'mike_jones', 'mike.jones@example.com', 'hashedpassword3', 'Mike', 'Jones', 'profile3.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(4, 'susan_brown', 'susan.brown@example.com', 'hashedpassword4', 'Susan', 'Brown', 'profile4.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'banned'),
(5, 'james_white', 'james.white@example.com', 'hashedpassword5', 'James', 'White', 'profile5.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(6, 'emily_clark', 'emily.clark@example.com', 'hashedpassword6', 'Emily', 'Clark', 'profile6.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'inactive'),
(7, 'daniel_martin', 'daniel.martin@example.com', 'hashedpassword7', 'Daniel', 'Martin', 'profile7.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(8, 'laura_lewis', 'laura.lewis@example.com', 'hashedpassword8', 'Laura', 'Lewis', 'profile8.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'inactive'),
(9, 'robert_moore', 'robert.moore@example.com', 'hashedpassword9', 'Robert', 'Moore', 'profile9.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(10, 'charlotte_taylor', 'charlotte.taylor@example.com', 'hashedpassword10', 'Charlotte', 'Taylor', 'profile10.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'banned'),
(11, 'oliver_harris', 'oliver.harris@example.com', 'hashedpassword11', 'Oliver', 'Harris', 'profile11.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(12, 'sophie_wilson', 'sophie.wilson@example.com', 'hashedpassword12', 'Sophie', 'Wilson', 'profile12.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'inactive'),
(13, 'benjamin_scott', 'benjamin.scott@example.com', 'hashedpassword13', 'Benjamin', 'Scott', 'profile13.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(14, 'lucy_king', 'lucy.king@example.com', 'hashedpassword14', 'Lucy', 'King', 'profile14.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'inactive'),
(15, 'william_turner', 'william.turner@example.com', 'hashedpassword15', 'William', 'Turner', 'profile15.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(16, 'isabella_green', 'isabella.green@example.com', 'hashedpassword16', 'Isabella', 'Green', 'profile16.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'banned'),
(17, 'henry_adams', 'henry.adams@example.com', 'hashedpassword17', 'Henry', 'Adams', 'profile17.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(18, 'olivia_baker', 'olivia.baker@example.com', 'hashedpassword18', 'Olivia', 'Baker', 'profile18.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'inactive'),
(19, 'jack_evans', 'jack.evans@example.com', 'hashedpassword19', 'Jack', 'Evans', 'profile19.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'active'),
(20, 'mia_davis', 'mia.davis@example.com', 'hashedpassword20', 'Mia', 'Davis', 'profile20.jpg', '2025-02-12 06:52:46', '2025-02-12 06:52:46', 'inactive'),
(41, 'kyn', '650112230050@bru.ac.th', '$2y$10$AYPVbOdKo4Dm2hbzj6diWepybnnIvZxj//4nqTSZW3E26m2gnymPq', 'Kynthia', 'Satur', 'assets/img/profile/SaveClip.App_466483870_1189272478834021_1126070000555791768_n.jpg', '2025-02-12 16:09:36', '2025-02-13 15:46:01', 'active'),
(42, 'k', '123@bru.ac.th', '$2y$10$zF4vvY20bDec0yFBzJJsnOkW3Jlk86ycZDdFibo0xNfaKLsHX2OQC', 'Lala', 'Sarah', 'assets/img/profiles/profile_42_67ad82b997e6f.jpg', '2025-02-12 18:18:34', '2025-02-13 21:38:46', 'active'),
(43, 'Yo', '1234@bru.ac.th', '$2y$10$V6ujO5TnjVvaKPOnhQhlY.G4tfL.scryqo3S3kf//i5zN.M8nWwIm', 'Lala', 'Sarah', NULL, '2025-02-13 05:35:38', NULL, 'active'),
(44, 'kynn', '1@bru.ac.th', '$2y$10$43P18cPm391oYNyiatYbTOKD56IF2ayS29QXV5yYx3ZuJJaTT9Lki', 'kk', 'satur', NULL, '2025-02-13 08:06:40', NULL, 'active'),
(45, 'Jakah', '12@bru.ac.th', '$2y$10$aYAJkxNe/EdloApMnBeDh.ehEJkql2GGyZGym887DLTYN8veODhO6', 'Jakah', 'Levron', NULL, '2025-02-13 20:37:47', '2025-02-13 21:37:07', 'active'),
(46, 'Jake', '124@bru.ac.th', '$2y$10$3K1NeuiD57RWxFszWRfPFuebd.R6c1.Avz8ibkr5tTpgZZFnJUqoe', 'Jake', 'Levron', NULL, '2025-02-13 21:13:53', '2025-02-13 21:17:00', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE `user_roles` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`role_id`, `role_name`, `description`) VALUES
(1, 'Admin', 'Has full access to all system features and settings.'),
(2, 'Editor', 'Can create, edit, and delete content, but has limited access to system settings.'),
(3, 'Viewer', 'Can view content but cannot make any changes.');

-- --------------------------------------------------------

--
-- Table structure for table `user_role_assignment`
--

CREATE TABLE `user_role_assignment` (
  `user_role_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `assigned_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_role_assignment`
--

INSERT INTO `user_role_assignment` (`user_role_id`, `user_id`, `role_id`, `assigned_at`) VALUES
(1, 1, 1, '2025-02-12 07:14:44'),
(2, 2, 2, '2025-02-12 07:14:44'),
(3, 3, 3, '2025-02-12 07:14:44'),
(4, 4, 2, '2025-02-12 07:14:44'),
(5, 5, 3, '2025-02-12 07:14:44'),
(6, 6, 1, '2025-02-12 07:14:44'),
(7, 7, 3, '2025-02-12 07:14:44'),
(8, 8, 2, '2025-02-12 07:14:44'),
(9, 9, 3, '2025-02-12 07:14:44'),
(10, 10, 1, '2025-02-12 07:14:44'),
(11, 11, 3, '2025-02-12 07:14:44'),
(12, 12, 2, '2025-02-12 07:14:44'),
(13, 13, 2, '2025-02-12 07:14:44'),
(14, 14, 1, '2025-02-12 07:14:44'),
(15, 15, 3, '2025-02-12 07:14:44'),
(16, 16, 2, '2025-02-12 07:14:44'),
(17, 17, 3, '2025-02-12 07:14:44'),
(18, 18, 1, '2025-02-12 07:14:44'),
(19, 19, 2, '2025-02-12 07:14:44'),
(20, 20, 3, '2025-02-12 07:14:44'),
(21, 41, 1, '2025-02-12 16:09:36'),
(22, 42, 1, '2025-02-12 18:18:34'),
(23, 43, 1, '2025-02-13 05:35:38');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `audit_log`
--
ALTER TABLE `audit_log`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `genres`
--
ALTER TABLE `genres`
  ADD PRIMARY KEY (`genre_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`movie_id`),
  ADD KEY `fk_movie_genre` (`genre`);

--
-- Indexes for table `movie_genres`
--
ALTER TABLE `movie_genres`
  ADD PRIMARY KEY (`movie_id`,`genre_id`),
  ADD KEY `genre_id` (`genre_id`);

--
-- Indexes for table `movie_keywords`
--
ALTER TABLE `movie_keywords`
  ADD PRIMARY KEY (`keyword_id`),
  ADD KEY `movie_id` (`movie_id`);

--
-- Indexes for table `movie_streaming`
--
ALTER TABLE `movie_streaming`
  ADD PRIMARY KEY (`movie_id`,`platform_id`),
  ADD KEY `fk_movie_streaming_platform` (`platform_id`);

--
-- Indexes for table `password_reset`
--
ALTER TABLE `password_reset`
  ADD PRIMARY KEY (`reset_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `statistics`
--
ALTER TABLE `statistics`
  ADD PRIMARY KEY (`stat_id`),
  ADD KEY `movie_id` (`movie_id`);

--
-- Indexes for table `streaming_platforms`
--
ALTER TABLE `streaming_platforms`
  ADD PRIMARY KEY (`platform_id`),
  ADD UNIQUE KEY `platform_name` (`platform_name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `user_role_assignment`
--
ALTER TABLE `user_role_assignment`
  ADD PRIMARY KEY (`user_role_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `audit_log`
--
ALTER TABLE `audit_log`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `genres`
--
ALTER TABLE `genres`
  MODIFY `genre_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT for table `movies`
--
ALTER TABLE `movies`
  MODIFY `movie_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `movie_keywords`
--
ALTER TABLE `movie_keywords`
  MODIFY `keyword_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `password_reset`
--
ALTER TABLE `password_reset`
  MODIFY `reset_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `statistics`
--
ALTER TABLE `statistics`
  MODIFY `stat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `streaming_platforms`
--
ALTER TABLE `streaming_platforms`
  MODIFY `platform_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `user_roles`
--
ALTER TABLE `user_roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user_role_assignment`
--
ALTER TABLE `user_role_assignment`
  MODIFY `user_role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `audit_log`
--
ALTER TABLE `audit_log`
  ADD CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `movies`
--
ALTER TABLE `movies`
  ADD CONSTRAINT `fk_movie_genre` FOREIGN KEY (`genre`) REFERENCES `genres` (`genre_id`);

--
-- Constraints for table `movie_genres`
--
ALTER TABLE `movie_genres`
  ADD CONSTRAINT `movie_genres_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `movie_genres_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`genre_id`) ON DELETE CASCADE;

--
-- Constraints for table `movie_keywords`
--
ALTER TABLE `movie_keywords`
  ADD CONSTRAINT `movie_keywords_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`);

--
-- Constraints for table `movie_streaming`
--
ALTER TABLE `movie_streaming`
  ADD CONSTRAINT `fk_movie_streaming_platform` FOREIGN KEY (`platform_id`) REFERENCES `streaming_platforms` (`platform_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `movie_streaming_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `movie_streaming_ibfk_2` FOREIGN KEY (`platform_id`) REFERENCES `streaming_platforms` (`platform_id`) ON DELETE CASCADE;

--
-- Constraints for table `password_reset`
--
ALTER TABLE `password_reset`
  ADD CONSTRAINT `password_reset_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `statistics`
--
ALTER TABLE `statistics`
  ADD CONSTRAINT `statistics_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`);

--
-- Constraints for table `user_role_assignment`
--
ALTER TABLE `user_role_assignment`
  ADD CONSTRAINT `user_role_assignment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `user_role_assignment_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `user_roles` (`role_id`);
--
-- Database: `phpmyadmin`
--
CREATE DATABASE IF NOT EXISTS `phpmyadmin` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE `phpmyadmin`;

-- --------------------------------------------------------

--
-- Table structure for table `pma__bookmark`
--

CREATE TABLE `pma__bookmark` (
  `id` int(10) UNSIGNED NOT NULL,
  `dbase` varchar(255) NOT NULL DEFAULT '',
  `user` varchar(255) NOT NULL DEFAULT '',
  `label` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `query` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Bookmarks';

-- --------------------------------------------------------

--
-- Table structure for table `pma__central_columns`
--

CREATE TABLE `pma__central_columns` (
  `db_name` varchar(64) NOT NULL,
  `col_name` varchar(64) NOT NULL,
  `col_type` varchar(64) NOT NULL,
  `col_length` text DEFAULT NULL,
  `col_collation` varchar(64) NOT NULL,
  `col_isNull` tinyint(1) NOT NULL,
  `col_extra` varchar(255) DEFAULT '',
  `col_default` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Central list of columns';

-- --------------------------------------------------------

--
-- Table structure for table `pma__column_info`
--

CREATE TABLE `pma__column_info` (
  `id` int(5) UNSIGNED NOT NULL,
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `column_name` varchar(64) NOT NULL DEFAULT '',
  `comment` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `mimetype` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `transformation` varchar(255) NOT NULL DEFAULT '',
  `transformation_options` varchar(255) NOT NULL DEFAULT '',
  `input_transformation` varchar(255) NOT NULL DEFAULT '',
  `input_transformation_options` varchar(255) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Column information for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__designer_settings`
--

CREATE TABLE `pma__designer_settings` (
  `username` varchar(64) NOT NULL,
  `settings_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Settings related to Designer';

-- --------------------------------------------------------

--
-- Table structure for table `pma__export_templates`
--

CREATE TABLE `pma__export_templates` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL,
  `export_type` varchar(10) NOT NULL,
  `template_name` varchar(64) NOT NULL,
  `template_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved export templates';

-- --------------------------------------------------------

--
-- Table structure for table `pma__favorite`
--

CREATE TABLE `pma__favorite` (
  `username` varchar(64) NOT NULL,
  `tables` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Favorite tables';

-- --------------------------------------------------------

--
-- Table structure for table `pma__history`
--

CREATE TABLE `pma__history` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL DEFAULT '',
  `db` varchar(64) NOT NULL DEFAULT '',
  `table` varchar(64) NOT NULL DEFAULT '',
  `timevalue` timestamp NOT NULL DEFAULT current_timestamp(),
  `sqlquery` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='SQL history for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__navigationhiding`
--

CREATE TABLE `pma__navigationhiding` (
  `username` varchar(64) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `item_type` varchar(64) NOT NULL,
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Hidden items of navigation tree';

-- --------------------------------------------------------

--
-- Table structure for table `pma__pdf_pages`
--

CREATE TABLE `pma__pdf_pages` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `page_nr` int(10) UNSIGNED NOT NULL,
  `page_descr` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='PDF relation pages for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__recent`
--

CREATE TABLE `pma__recent` (
  `username` varchar(64) NOT NULL,
  `tables` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Recently accessed tables';

--
-- Dumping data for table `pma__recent`
--

INSERT INTO `pma__recent` (`username`, `tables`) VALUES
('root', '[{\"db\":\"projectdb\",\"table\":\"house_views\"},{\"db\":\"projectdb\",\"table\":\"house\"},{\"db\":\"projectdb\",\"table\":\"house_images\"},{\"db\":\"projectdb\",\"table\":\"house_features\"},{\"db\":\"projectdb\",\"table\":\"house_type\"},{\"db\":\"projectdb\",\"table\":\"project\"},{\"db\":\"projectdb\",\"table\":\"admins\"}]');

-- --------------------------------------------------------

--
-- Table structure for table `pma__relation`
--

CREATE TABLE `pma__relation` (
  `master_db` varchar(64) NOT NULL DEFAULT '',
  `master_table` varchar(64) NOT NULL DEFAULT '',
  `master_field` varchar(64) NOT NULL DEFAULT '',
  `foreign_db` varchar(64) NOT NULL DEFAULT '',
  `foreign_table` varchar(64) NOT NULL DEFAULT '',
  `foreign_field` varchar(64) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Relation table';

-- --------------------------------------------------------

--
-- Table structure for table `pma__savedsearches`
--

CREATE TABLE `pma__savedsearches` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL DEFAULT '',
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `search_name` varchar(64) NOT NULL DEFAULT '',
  `search_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved searches';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_coords`
--

CREATE TABLE `pma__table_coords` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `pdf_page_number` int(11) NOT NULL DEFAULT 0,
  `x` float UNSIGNED NOT NULL DEFAULT 0,
  `y` float UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table coordinates for phpMyAdmin PDF output';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_info`
--

CREATE TABLE `pma__table_info` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `display_field` varchar(64) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table information for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_uiprefs`
--

CREATE TABLE `pma__table_uiprefs` (
  `username` varchar(64) NOT NULL,
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL,
  `prefs` text NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Tables'' UI preferences';

-- --------------------------------------------------------

--
-- Table structure for table `pma__tracking`
--

CREATE TABLE `pma__tracking` (
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL,
  `version` int(10) UNSIGNED NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  `schema_snapshot` text NOT NULL,
  `schema_sql` text DEFAULT NULL,
  `data_sql` longtext DEFAULT NULL,
  `tracking` set('UPDATE','REPLACE','INSERT','DELETE','TRUNCATE','CREATE DATABASE','ALTER DATABASE','DROP DATABASE','CREATE TABLE','ALTER TABLE','RENAME TABLE','DROP TABLE','CREATE INDEX','DROP INDEX','CREATE VIEW','ALTER VIEW','DROP VIEW') DEFAULT NULL,
  `tracking_active` int(1) UNSIGNED NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Database changes tracking for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__userconfig`
--

CREATE TABLE `pma__userconfig` (
  `username` varchar(64) NOT NULL,
  `timevalue` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `config_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User preferences storage for phpMyAdmin';

--
-- Dumping data for table `pma__userconfig`
--

INSERT INTO `pma__userconfig` (`username`, `timevalue`, `config_data`) VALUES
('root', '2025-08-26 16:41:15', '{\"Console\\/Mode\":\"collapse\",\"NavigationWidth\":246}');

-- --------------------------------------------------------

--
-- Table structure for table `pma__usergroups`
--

CREATE TABLE `pma__usergroups` (
  `usergroup` varchar(64) NOT NULL,
  `tab` varchar(64) NOT NULL,
  `allowed` enum('Y','N') NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User groups with configured menu items';

-- --------------------------------------------------------

--
-- Table structure for table `pma__users`
--

CREATE TABLE `pma__users` (
  `username` varchar(64) NOT NULL,
  `usergroup` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Users and their assignments to user groups';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pma__central_columns`
--
ALTER TABLE `pma__central_columns`
  ADD PRIMARY KEY (`db_name`,`col_name`);

--
-- Indexes for table `pma__column_info`
--
ALTER TABLE `pma__column_info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `db_name` (`db_name`,`table_name`,`column_name`);

--
-- Indexes for table `pma__designer_settings`
--
ALTER TABLE `pma__designer_settings`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_user_type_template` (`username`,`export_type`,`template_name`);

--
-- Indexes for table `pma__favorite`
--
ALTER TABLE `pma__favorite`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__history`
--
ALTER TABLE `pma__history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`,`db`,`table`,`timevalue`);

--
-- Indexes for table `pma__navigationhiding`
--
ALTER TABLE `pma__navigationhiding`
  ADD PRIMARY KEY (`username`,`item_name`,`item_type`,`db_name`,`table_name`);

--
-- Indexes for table `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  ADD PRIMARY KEY (`page_nr`),
  ADD KEY `db_name` (`db_name`);

--
-- Indexes for table `pma__recent`
--
ALTER TABLE `pma__recent`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__relation`
--
ALTER TABLE `pma__relation`
  ADD PRIMARY KEY (`master_db`,`master_table`,`master_field`),
  ADD KEY `foreign_field` (`foreign_db`,`foreign_table`);

--
-- Indexes for table `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_savedsearches_username_dbname` (`username`,`db_name`,`search_name`);

--
-- Indexes for table `pma__table_coords`
--
ALTER TABLE `pma__table_coords`
  ADD PRIMARY KEY (`db_name`,`table_name`,`pdf_page_number`);

--
-- Indexes for table `pma__table_info`
--
ALTER TABLE `pma__table_info`
  ADD PRIMARY KEY (`db_name`,`table_name`);

--
-- Indexes for table `pma__table_uiprefs`
--
ALTER TABLE `pma__table_uiprefs`
  ADD PRIMARY KEY (`username`,`db_name`,`table_name`);

--
-- Indexes for table `pma__tracking`
--
ALTER TABLE `pma__tracking`
  ADD PRIMARY KEY (`db_name`,`table_name`,`version`);

--
-- Indexes for table `pma__userconfig`
--
ALTER TABLE `pma__userconfig`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__usergroups`
--
ALTER TABLE `pma__usergroups`
  ADD PRIMARY KEY (`usergroup`,`tab`,`allowed`);

--
-- Indexes for table `pma__users`
--
ALTER TABLE `pma__users`
  ADD PRIMARY KEY (`username`,`usergroup`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__column_info`
--
ALTER TABLE `pma__column_info`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__history`
--
ALTER TABLE `pma__history`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  MODIFY `page_nr` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- Database: `projectdb`
--
CREATE DATABASE IF NOT EXISTS `projectdb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `projectdb`;

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `status` enum('active','inactive') NOT NULL DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `role` varchar(20) NOT NULL DEFAULT 'admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `password`, `email`, `first_name`, `last_name`, `status`, `created_at`, `role`) VALUES
(2, 'admin', 'pbkdf2:sha256:100000', 'admin@example.com', 'Admin', 'User2', 'inactive', '2025-04-05 08:59:04', 'admin'),
(3, 'enny1', 'scrypt:32768:8:1$ezZG8MVHsj7D20Bm$5562e0a4786aa155ac8df9892dcba8e7e788a2e47f9c56f4de6fe7ef75f0009d3a6c4766c9b1263c96a0ced16deb69d86b54c42df5882f119b3c1ad3c6f89ff2', 'enianjola@gmail.com', 'enny', 'Sena', 'active', '2025-04-05 10:54:54', 'admin'),
(4, 'mike', 'scrypt:32768:8:1$DFupAB3T9Um7lewm$dc99d456001393507fa7b4d15e2235747fd3ebbcebb5bc4924852086674090a209d17a7ee77b0792832297a7cf43c7a9efd74a12b42e96f9a706eeb831c30afb', 'st25364@bru.ac.th', 'oladele', 'senbanjo', 'active', '2025-05-22 10:21:07', 'superadmin'),
(6, 'faii', 'scrypt:32768:8:1$0jMnosWKMZMA7jQ3$2b6b3b72af5f18b8fc7cef48f592d4c1393cf119d8bcd45a10e794647c8ab93caa4b532fd3169f30b76d6ac0e94f48fa769dfc6e3f911aeef454a3178eb63530', 'baanthai.buriram@gmail.com', 'faidat', 'OJO', 'inactive', '2025-08-11 12:04:58', 'admin'),
(7, 'testadmin', 'scrypt:32768:8:1$WJttknxt8PPDnxkl$cb3cefb65397e625b6c7c9a07b8a5e0ad7e9189361f4d64ca48e6012b22cd3c33c7e75eee1f0c81a0d63194ada445f47fbda9d8faca152f92957ffcfc8358cae', 'test@example.com', 'Test1', 'Admin', 'active', '2025-08-14 10:59:11', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `house`
--

CREATE TABLE `house` (
  `h_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `t_id` int(11) DEFAULT NULL,
  `h_title` varchar(255) NOT NULL,
  `h_description` text DEFAULT NULL,
  `price` decimal(12,2) DEFAULT NULL,
  `bedrooms` int(11) DEFAULT NULL,
  `bathrooms` int(11) DEFAULT NULL,
  `living_area` decimal(10,2) DEFAULT NULL,
  `parking_space` int(11) DEFAULT NULL,
  `no_of_floors` int(11) DEFAULT NULL,
  `a_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` varchar(50) DEFAULT 'Available',
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `f_id` int(11) DEFAULT NULL,
  `view_count` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `house`
--

INSERT INTO `house` (`h_id`, `p_id`, `t_id`, `h_title`, `h_description`, `price`, `bedrooms`, `bathrooms`, `living_area`, `parking_space`, `no_of_floors`, `a_id`, `created_at`, `updated_at`, `status`, `latitude`, `longitude`, `f_id`, `view_count`) VALUES
(12, 2, 5, 'BAANTHAI BURIRAM 5 SIZE M', 'โครงการบ้านไท บ้านเดี่ยวชั้นเดียว แบบบ้านสไตล์โมเดิร์น\r\nเหมาะกับคนรุ่นใหม่ วัยทำงาน ต้องการความเงียบสงบกับราคาบ้านที่เอื้อมถึง\r\nพร้อมสิ่งอำนวย เพราะอยู่ในโซนเทศบาลตำบลอิสาณ\r\nใกล้ร้านสะดวกซื้อมากมาย CJ Mall , 7-11\r\nใกล้ห้างสรรพสินค้าชั้นนำ โรบินสัน บิ๊กซี แม็กโคร ทวีกิจซุเปอร์เซ็นเตอร์', 1800000.00, 3, 2, 100.00, 1, 2, NULL, '2025-08-18 11:37:01', '2025-08-22 12:17:25', 'available', 14.9982500, 103.0700600, 4, 5),
(13, 2, 5, 'BAANTHAI BURIRAM 5 SIZE L', 'โครงการบ้านไท บ้านเดี่ยวชั้นเดียว แบบบ้านสไตล์โมเดิร์น\r\nเหมาะกับคนรุ่นใหม่ วัยทำงาน ต้องการความเงียบสงบกับราคาบ้านที่เอื้อมถึง\r\nพร้อมสิ่งอำนวย เพราะอยู่ในโซนเทศบาลตำบลอิสาณ\r\nใกล้ร้านสะดวกซื้อมากมาย CJ Mall , 7-11\r\nใกล้ห้างสรรพสินค้าชั้นนำ โรบินสัน บิ๊กซี แม็กโคร ทวีกิจซุเปอร์เซ็นเตอร์', 1950000.00, 3, 2, 120.00, 2, 1, NULL, '2025-08-18 12:20:21', '2025-09-02 07:23:44', 'available', 14.9982500, 103.0700600, 4, 3),
(14, 2, 5, 'BAANTHAI BURIRAM 5 SIZE S', 'โครงการบ้านไท บ้านเดี่ยวชั้นเดียว แบบบ้านสไตล์โมเดิร์น\r\nเหมาะกับคนรุ่นใหม่ วัยทำงาน ต้องการความเงียบสงบกับราคาบ้านที่เอื้อมถึง\r\nพร้อมสิ่งอำนวย เพราะอยู่ในโซนเทศบาลตำบลอิสาณ\r\nใกล้ร้านสะดวกซื้อมากมาย CJ Mall , 7-11\r\nใกล้ห้างสรรพสินค้าชั้นนำ โรบินสัน บิ๊กซี แม็กโคร ทวีกิจซุเปอร์เซ็นเตอร์', 1000000.00, 2, 1, 80.00, 1, 1, NULL, '2025-08-18 14:18:57', '2025-08-25 06:12:50', 'available', 14.9982500, 103.0700600, NULL, 1),
(15, 2, 5, 'BAANTHAI BURIRAM TYPE A', 'โครงการบ้านไท 4 แยกกระสัง โซนโรบินสันบ้านบัว\r\nพิกัด: สี่แยกกระสัง ตรงข้ามโกลบอลเฮ้าส์\r\n3 ห้องนอน 2 ห้องน้ำ 1 ห้องครัว ที่จอดรถ 1 คัน\r\nพร้อมพื้นที่รอบบ้าน\r\nจองทำเล รับไปเลย Promotions ส่งท้ายปี\r\nส่วนลดจสูงสุด 200,000 บาท\r\nของแถมเลือกได้ มีหลายรายการ\r\nที่นี่ที่เดียว บ้านสวยราคาไม่ถึง 2 ล้าน\r\nเช็คเครดิตก่อน ยื่นฟรี ไม่มีค่าใช้จ่าย\r\nรู้ก่อน วางแผนก่อน เตรียมตัวได้เร็ว\r\nกู้ได้ทุกอาชีพดันให้ทุกเคส ช่วยวางแผนทุกขั้นตอน ติดตามผลการยื่นกู้ให้ฟรี\r\n', 1690000.00, 3, 2, 100.00, 1, 1, NULL, '2025-08-19 08:26:24', '2025-09-01 06:08:21', 'available', 14.9982500, 103.0700600, 4, 3),
(16, 2, 1, 'BAANTHAI BURIRAM TYPE B', 'โครงการบ้านไท 4 แยกกระสัง โซนโรบินสันบ้านบัว\r\nพิกัด: สี่แยกกระสัง ตรงข้ามโกลบอลเฮ้าส์\r\n3 ห้องนอน 2 ห้องน้ำ 1 ห้องครัว ที่จอดรถ 1 คัน\r\nพร้อมพื้นที่รอบบ้าน\r\nจองทำเล รับไปเลย Promotions ส่งท้ายปี\r\nส่วนลดจสูงสุด 200,000 บาท\r\nของแถมเลือกได้ มีหลายรายการ\r\nที่นี่ที่เดียว บ้านสวยราคาไม่ถึง 2 ล้าน\r\nเช็คเครดิตก่อน ยื่นฟรี ไม่มีค่าใช้จ่าย\r\nรู้ก่อน วางแผนก่อน เตรียมตัวได้เร็ว\r\nกู้ได้ทุกอาชีพดันให้ทุกเคส ช่วยวางแผนทุกขั้นตอน ติดตามผลการยื่นกู้ให้ฟรี', 1990000.00, 3, 2, 100.00, 2, 2, NULL, '2025-08-19 08:48:07', '2025-09-01 06:03:31', 'available', 14.9982500, 103.0700600, 4, 4),
(17, 6, 5, 'CASA MALIWAN บ้านชั้นเดี่ยว', 'คาซ่า มะลิวัลย์ เป็นโครงการบ้านเดี่ยวที่ออกแบบอย่างเรียบหรู สไตล์โมเดิร์น โอบล้อมด้วยบรรยากาศสงบและเป็นส่วนตัว เหมาะสำหรับครอบครัวที่ต้องการบ้านคุณภาพในราคาที่เข้าถึงได้\r\nบ้านเดี่ยวชั้นเดียว: 3 ห้องนอน 2 ห้องน้ำ ที่จอดรถ 1 คัน\r\nบ้านเดี่ยวสองชั้น: 3 ห้องนอน 2 ห้องน้ำ ที่จอดรถ 2 คัน\r\nจำนวนยูนิตรวม: 36 หลัง\r\nราคาเริ่มต้นเพียง 1.79 ล้านบาท\r\n\r\nสิ่งอำนวยความสะดวกภายในโครงการ\r\nสวนหย่อมส่วนกลาง\r\nระบบรักษาความปลอดภัย 24 ชั่วโมง พร้อมกล้อง CCTV\r\n\r\nทำเลที่ตั้ง\r\nโครงการตั้งอยู่ใกล้สิ่งอำนวยความสะดวกในเมือง ไม่ว่าจะเป็นห้างสรรพสินค้า โรงเรียน มหาวิทยาลัย และโรงพยาบาล เดินทางสะดวกด้วยถนนมะลิวัลย์\r\nคาซ่า มะลิวัลย์ ขอนแก่น — บ้านที่ลงตัวทั้งดีไซน์ ราคา และคุณภาพชีวิต', 1790000.00, 3, 2, 100.00, 1, 1, NULL, '2025-08-19 09:13:58', '2025-08-19 09:19:12', 'available', 16.2810100, 102.4343200, 4, 0),
(18, 6, 1, 'CASA MALIWAN SIZE M', 'คาซ่า มะลิวัลย์ เป็นโครงการบ้านเดี่ยวที่ออกแบบอย่างเรียบหรู สไตล์โมเดิร์น โอบล้อมด้วยบรรยากาศสงบและเป็นส่วนตัว เหมาะสำหรับครอบครัวที่ต้องการบ้าน\r\n\r\nคุณภาพในราคาที่เข้าถึงได้\r\nบ้านเดี่ยวชั้นเดียว: 3 ห้องนอน 2 ห้องน้ำ ที่จอดรถ 1 คัน\r\nบ้านเดี่ยวสองชั้น: 3 ห้องนอน 2 ห้องน้ำ ที่จอดรถ 2 คัน\r\nจำนวนยูนิตรวม: 36 หลัง\r\nราคาเริ่มต้นเพียง 1.79 ล้านบาท\r\n\r\nสิ่งอำนวยความสะดวกภายในโครงการ\r\nสวนหย่อมส่วนกลาง\r\nระบบรักษาความปลอดภัย 24 ชั่วโมง พร้อมกล้อง CCTV\r\n\r\nทำเลที่ตั้ง\r\nโครงการตั้งอยู่ใกล้สิ่งอำนวยความสะดวกในเมือง ไม่ว่าจะเป็นห้างสรรพสินค้า โรงเรียน มหาวิทยาลัย และโรงพยาบาล เดินทางสะดวกด้วยถนนมะลิวัลย์\r\n\r\nคาซ่า มะลิวัลย์ ขอนแก่น — บ้านที่ลงตัวทั้งดีไซน์ ราคา และคุณภาพชีวิต', 2590000.00, 3, 2, 100.00, 2, 2, NULL, '2025-08-19 09:26:39', '2025-08-25 06:12:42', 'available', 16.2810100, 102.4343200, 4, 2),
(19, 6, 1, 'CASA MALIWAN SIZE L', 'คาซ่า มะลิวัลย์ เป็นโครงการบ้านเดี่ยวที่ออกแบบอย่างเรียบหรู สไตล์โมเดิร์น โอบล้อมด้วยบรรยากาศสงบและเป็นส่วนตัว เหมาะสำหรับครอบครัวที่ต้องการบ้าน\r\n\r\nคุณภาพในราคาที่เข้าถึงได้\r\nบ้านเดี่ยวชั้นเดียว: 3 ห้องนอน 2 ห้องน้ำ ที่จอดรถ 1 คัน\r\nบ้านเดี่ยวสองชั้น: 3 ห้องนอน 2 ห้องน้ำ ที่จอดรถ 2 คัน\r\nจำนวนยูนิตรวม: 36 หลัง\r\nราคาเริ่มต้นเพียง 1.79 ล้านบาท\r\n\r\nสิ่งอำนวยความสะดวกภายในโครงการ\r\nสวนหย่อมส่วนกลาง\r\nระบบรักษาความปลอดภัย 24 ชั่วโมง พร้อมกล้อง CCTV\r\n\r\nทำเลที่ตั้ง\r\nโครงการตั้งอยู่ใกล้สิ่งอำนวยความสะดวกในเมือง ไม่ว่าจะเป็นห้างสรรพสินค้า โรงเรียน มหาวิทยาลัย และโรงพยาบาล เดินทางสะดวกด้วยถนนมะลิวัลย์\r\n\r\nคาซ่า มะลิวัลย์ ขอนแก่น — บ้านที่ลงตัวทั้งดีไซน์ ราคา และคุณภาพชีวิต', 2990000.00, 4, 3, 100.00, 3, 2, NULL, '2025-08-19 09:41:27', '2025-08-28 05:39:32', 'available', 16.2810100, 102.4343200, 3, 5),
(20, 3, 5, 'LAVILLA KALASIN ชั้นเดี่ยว', 'ลา วิลล่า กาฬสินธุ์ (La Villa Kalasin)\r\nลา วิลล่า กาฬสินธุ์ เป็นโครงการบ้านเดี่ยวดีไซน์ทันสมัย ฟังก์ชันครบ ตอบโจทย์ทั้งครอบครัวขนาดเล็กและใหญ่ ตั้งอยู่บนทำเลศักยภาพใกล้ใจกลางเมืองกาฬสินธุ์ เดินทางสะดวกและรายล้อมด้วยสิ่งอำนวยความสะดวกครบครัน\r\n\r\nบ้านเดี่ยวชั้นเดียว: 3 ห้องนอน 2 ห้องน้ำ พื้นที่ใช้สอยประมาณ 120 ตร.ม.\r\nบ้านเดี่ยวสองชั้น: 4 ห้องนอน 2 ห้องน้ำ\r\nจำนวนยูนิตรวม: 34 หลัง บนพื้นที่โครงการประมาณ 5 ไร่ 2 งาน 88 ตร.ว.\r\nราคาเริ่มต้นเพียง 1.55 ล้านบาท (บ้านชั้นเดียว) และ 2.19 ล้านบาท (บ้านสองชั้น)\r\n\r\nสิ่งอำนวยความสะดวกภายในโครงการ\r\nสวนสาธารณะสำหรับพักผ่อน\r\nระบบรักษาความปลอดภัยตลอด 24 ชั่วโมง พร้อมเจ้าหน้าที่\r\n\r\nทำเลที่ตั้ง\r\nโครงการตั้งอยู่ใกล้ใจกลางเมืองกาฬสินธุ์ ใกล้โรงพยาบาลกาฬสินธุ์, บิ๊กซี, เทสโก้โลตัส และสถานที่สำคัญอื่น ๆ เดินทางสะดวกสบาย', 1550000.00, 3, 2, 120.00, 1, 1, NULL, '2025-08-19 09:52:57', '2025-08-27 08:25:04', 'available', 16.2510000, 103.3240100, 4, 9),
(21, 3, 1, 'LA VILLA KALASIN สองชั้น', 'ลา วิลล่า กาฬสินธุ์ เป็นโครงการบ้านเดี่ยวดีไซน์ทันสมัย ฟังก์ชันครบ ตอบโจทย์ทั้งครอบครัวขนาดเล็กและใหญ่ ตั้งอยู่บนทำเลศักยภาพใกล้ใจกลางเมืองกาฬสินธุ์ เดินทางสะดวกและรายล้อมด้วยสิ่งอำนวยความสะดวกครบครัน\r\n\r\nบ้านเดี่ยวชั้นเดียว: 3 ห้องนอน 2 ห้องน้ำ พื้นที่ใช้สอยประมาณ 120 ตร.ม.\r\nบ้านเดี่ยวสองชั้น: 4 ห้องนอน 2 ห้องน้ำ\r\nจำนวนยูนิตรวม: 34 หลัง บนพื้นที่โครงการประมาณ 5 ไร่ 2 งาน 88 ตร.ว.\r\nราคาเริ่มต้นเพียง 1.55 ล้านบาท (บ้านชั้นเดียว) และ 2.19 ล้านบาท (บ้านสองชั้น)\r\n\r\nสิ่งอำนวยความสะดวกภายในโครงการ\r\nสวนสาธารณะสำหรับพักผ่อน\r\nระบบรักษาความปลอดภัยตลอด 24 ชั่วโมง พร้อมเจ้าหน้าที่\r\n\r\nทำเลที่ตั้ง\r\nโครงการตั้งอยู่ใกล้ใจกลางเมืองกาฬสินธุ์ ใกล้โรงพยาบาลกาฬสินธุ์, บิ๊กซี, เทสโก้โลตัส และสถานที่สำคัญอื่น ๆ เดินทางสะดวกสบาย', 2190000.00, 4, 2, 100.00, 2, 2, NULL, '2025-08-19 10:00:11', '2025-09-01 06:35:19', 'available', 0.0000000, 0.0000000, 3, 8),
(22, 6, 1, 'LAVILLA NONGLOUP', 'ลาวิลล่าหนองหลุบ LA VILLA\r\nโครงการใหม่ บ้านเดี่ยว 2 ชั้นเมืองขอนแก่น ใกล้สนามบิน\r\nเดินทางสะดวก บ้านน่าอยู่\r\nพื้นที่กว้างขวาง อากาศดี๊ดี\r\nผ่อนสบายๆ ราคาที่คุณเอื้อมถึงจ้า\r\n3 ห้องนอน\r\n3 ห้องน้ำ\r\nที่จอดรถ 2 คัน\r\nพื้นที่ 50 ตรว.', 3090000.00, 3, 3, 153.00, 2, 2, NULL, '2025-08-19 11:17:51', '2025-09-02 07:21:43', 'available', 16.2751300, 102.4537400, 4, 21);

-- --------------------------------------------------------

--
-- Table structure for table `house_features`
--

CREATE TABLE `house_features` (
  `f_id` int(11) NOT NULL,
  `f_name` varchar(100) NOT NULL,
  `f_description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `f_image` varchar(255) DEFAULT NULL,
  `a_id` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `house_features`
--

INSERT INTO `house_features` (`f_id`, `f_name`, `f_description`, `created_at`, `f_image`, `a_id`, `updated_at`) VALUES
(3, '4 ห้องนอน', 'Beautifully landscaped garden area.', '2025-05-26 08:42:59', 'pexels-pixabay-271624.jpg', 4, '2025-07-01 09:50:13'),
(4, '3 ห้องนอน', 'บ้านสวยมากก', '2025-05-27 04:12:50', 'pexels-jvdm-1454806.jpg', 4, '2025-07-22 09:54:43'),
(8, '2 ห้องนอน', 'yess', '2025-08-19 09:33:44', '4.jpg', 4, '2025-08-21 11:14:24');

-- --------------------------------------------------------

--
-- Table structure for table `house_images`
--

CREATE TABLE `house_images` (
  `id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_main` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `house_images`
--

INSERT INTO `house_images` (`id`, `house_id`, `image_url`, `created_at`, `is_main`) VALUES
(19, 12, 'uploads/baan_1_1755517021.png', '2025-08-18 11:37:01', 1),
(20, 12, 'uploads/1755518128_baan_2.png', '2025-08-18 11:55:28', 0),
(21, 12, 'uploads/1755518128_site_plan.png', '2025-08-18 11:55:28', 0),
(22, 13, 'uploads/baan_1_l_1755519621.png', '2025-08-18 12:20:21', 1),
(23, 13, 'uploads/baan_2_l_1755519621.png', '2025-08-18 12:20:21', 0),
(24, 13, 'uploads/inside_1_1755519621.png', '2025-08-18 12:20:21', 0),
(25, 13, 'uploads/inside_2_1755519621.png', '2025-08-18 12:20:21', 0),
(26, 13, 'uploads/1755519688_site_plan.png', '2025-08-18 12:21:28', 0),
(27, 14, 'uploads/baan_s_1_1755526737.png', '2025-08-18 14:18:57', 1),
(28, 14, 'uploads/baan_s_2_1755526737.png', '2025-08-18 14:18:57', 0),
(29, 14, 'uploads/inside_s1_1755526737.png', '2025-08-18 14:18:57', 0),
(30, 14, 'uploads/inside_s2_1755526737.png', '2025-08-18 14:18:57', 0),
(31, 14, 'uploads/inside_s3_1755526737.png', '2025-08-18 14:18:57', 0),
(32, 14, 'uploads/site_plan_1755526737.png', '2025-08-18 14:18:57', 0),
(37, 15, 'uploads/baan_4s_type_a_2_1755591984.png', '2025-08-19 08:26:24', 1),
(39, 15, 'uploads/1755592530_453725804_950206476909187_3039174782847369027_n.png', '2025-08-19 08:35:30', 0),
(40, 15, 'uploads/1755592530_475383873_1069696478293519_9211460356204302597_n.png', '2025-08-19 08:35:30', 0),
(41, 15, 'uploads/1755592530_AJtDgRGFrv.png', '2025-08-19 08:35:30', 0),
(42, 15, 'uploads/1755592530_baan_4s_type_a_2.png', '2025-08-19 08:35:30', 0),
(43, 15, 'uploads/1755592530_image.png', '2025-08-19 08:35:30', 0),
(44, 16, 'uploads/27499_1_1755593287.png', '2025-08-19 08:48:07', 1),
(45, 16, 'uploads/27500_1_1755593287.png', '2025-08-19 08:48:07', 0),
(46, 16, 'uploads/27501_1_1755593287.png', '2025-08-19 08:48:07', 0),
(47, 16, 'uploads/27503_1_1755593287.png', '2025-08-19 08:48:07', 0),
(49, 16, 'uploads/1755593318_65857241_902151243453171_2866983385539018752_n.png', '2025-08-19 08:48:38', 0),
(50, 16, 'uploads/1755593318_image_1.png', '2025-08-19 08:48:38', 0),
(51, 16, 'uploads/1755593318_image_2.png', '2025-08-19 08:48:38', 0),
(53, 17, 'uploads/637569091994375841-House1_cover2_1755594838.png', '2025-08-19 09:13:58', 0),
(54, 17, 'uploads/637569092158834293-House1_plan_1755594838.png', '2025-08-19 09:13:58', 0),
(55, 17, 'uploads/LINE_ALBUM___2_1755594838.png', '2025-08-19 09:13:58', 1),
(59, 18, 'uploads/ca196e2b8adceb2c0049beb686db27d2_1755595599.png', '2025-08-19 09:26:39', 1),
(60, 18, 'uploads/1755595732_2e206a2dfc5e8f6c3798204f23d3ece5.png', '2025-08-19 09:28:52', 0),
(61, 18, 'uploads/1755595732_6543f25a293413f0e882bc774c091a73.png', '2025-08-19 09:28:52', 0),
(64, 19, 'uploads/sm23hpc5ytoy5bvrc7wbez1em67ywfjnwkchycdnax0zle1wujl6lacnmsyynytw39nrwmvw213q50czm00zb0jb2ov9pj98j7r6x8v42qix8y2tk6lq3cbdxcbdm4ow.jpg_1755596487.png', '2025-08-19 09:41:27', 1),
(65, 19, 'uploads/1755596546_637569094995476388-CS_MLW_HouseB_cover.jpg.png', '2025-08-19 09:42:26', 0),
(66, 19, 'uploads/1755596546_637569095297626576-CS_MLW_HouseB_img.png', '2025-08-19 09:42:26', 0),
(68, 20, 'uploads/LINE_ALBUM___2_1755597177.png', '2025-08-19 09:52:57', 1),
(69, 20, 'uploads/1755597292_637569092158834293-House1_plan.png', '2025-08-19 09:54:52', 0),
(70, 21, 'uploads/100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png', '2025-08-19 10:00:11', 1),
(71, 21, 'uploads/1755597642_image_1.png', '2025-08-19 10:00:42', 0),
(72, 21, 'uploads/1755597642_image_2.png', '2025-08-19 10:00:42', 0),
(73, 22, 'uploads/v6FEQR4Ihf5bzbiiLYvlPKdcOwnxSYb3uENlOPb2_1755602271.jpg', '2025-08-19 11:17:51', 1),
(84, 22, 'uploads/1755602325_LINE_ALBUM____12_2.png', '2025-08-19 11:18:45', 0),
(85, 22, 'uploads/1755602435_LINE_ALBUM____7_1.png', '2025-08-19 11:20:35', 0),
(86, 22, 'uploads/1755602451_LINE_ALBUM____3_1.png', '2025-08-19 11:20:51', 0),
(87, 22, 'uploads/1755602451_LINE_ALBUM____6_2.png', '2025-08-19 11:20:51', 0),
(88, 22, 'uploads/1755602469_0a0430c98224718512f072b32c752840.png', '2025-08-19 11:21:09', 0),
(89, 22, 'uploads/1755602469_eyJidWNrZXQiOiJuYXlvby1wcm9kdWN0aW9uIiwia2V5IjoiYXR0YWNobWVudHMvcG9zdHMvMzAyOTAvZ2FsbGVyeS83NGZjMTRjZTA2N2JiNmE4ZWJmYWFjZGM1NGU4NDc3ZC5qcGVnIiwiZWRpdHMiOnsicmVzaXplIjp7IndpZHRoIjoxM.png', '2025-08-19 11:21:09', 0),
(90, 22, 'uploads/1755602479_1080x1080-03-1.png', '2025-08-19 11:21:19', 0),
(91, 22, 'uploads/1755602479_1920x1080.png', '2025-08-19 11:21:19', 0);

-- --------------------------------------------------------

--
-- Table structure for table `house_type`
--

CREATE TABLE `house_type` (
  `t_id` int(11) NOT NULL,
  `t_name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `a_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `t_image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `house_type`
--

INSERT INTO `house_type` (`t_id`, `t_name`, `description`, `a_id`, `created_at`, `updated_at`, `t_image`) VALUES
(1, 'บ้านสองชั้น', 'A stand-alone house not attached to any other house.', 1, '2025-05-22 08:59:04', '2025-08-21 13:43:28', '3jqkFhc82HKiL2NfFmY5M5TnlMFWbSb5YqQlxOvj.jpg'),
(5, 'บ้านชั้นเดียว', 'สวยจริงงง', NULL, '2025-05-28 04:16:30', '2025-08-28 05:35:36', 'baan_1.png');

-- --------------------------------------------------------

--
-- Table structure for table `house_views`
--

CREATE TABLE `house_views` (
  `id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `house_views`
--

INSERT INTO `house_views` (`id`, `house_id`, `ip_address`, `created_at`) VALUES
(2, 21, '127.0.0.1', '2025-08-22 11:12:22'),
(3, 21, '127.0.0.1', '2025-08-22 11:13:39'),
(4, 21, '127.0.0.1', '2025-08-22 11:15:22'),
(5, 21, '127.0.0.1', '2025-08-22 11:15:32'),
(6, 12, '127.0.0.1', '2025-08-22 11:15:41'),
(9, 21, '127.0.0.1', '2025-08-22 11:17:43'),
(10, 12, '127.0.0.1', '2025-08-22 11:20:15'),
(11, 19, '127.0.0.1', '2025-08-22 11:39:09'),
(12, 12, '127.0.0.1', '2025-08-22 12:10:13'),
(13, 12, '127.0.0.1', '2025-08-22 12:17:23'),
(14, 12, '127.0.0.1', '2025-08-22 12:17:25'),
(15, 22, '127.0.0.1', '2025-08-22 14:05:18'),
(16, 18, '127.0.0.1', '2025-08-22 16:43:55'),
(17, 16, '127.0.0.1', '2025-08-22 16:44:04'),
(18, 13, '127.0.0.1', '2025-08-23 02:03:48'),
(19, 19, '127.0.0.1', '2025-08-23 02:04:25'),
(20, 22, '127.0.0.1', '2025-08-23 06:27:31'),
(21, 22, '127.0.0.1', '2025-08-23 06:37:06'),
(22, 22, '127.0.0.1', '2025-08-23 06:49:59'),
(23, 22, '127.0.0.1', '2025-08-23 06:50:14'),
(24, 22, '127.0.0.1', '2025-08-23 07:13:31'),
(25, 22, '127.0.0.1', '2025-08-25 06:12:17'),
(26, 16, '127.0.0.1', '2025-08-25 06:12:34'),
(27, 18, '127.0.0.1', '2025-08-25 06:12:42'),
(28, 14, '127.0.0.1', '2025-08-25 06:12:50'),
(29, 15, '127.0.0.1', '2025-08-26 12:28:32'),
(30, 19, '127.0.0.1', '2025-08-26 12:57:16'),
(31, 22, '127.0.0.1', '2025-08-27 07:10:09'),
(32, 22, '127.0.0.1', '2025-08-27 07:17:36'),
(33, 20, '127.0.0.1', '2025-08-27 07:18:18'),
(34, 20, '127.0.0.1', '2025-08-27 07:22:41'),
(35, 20, '127.0.0.1', '2025-08-27 07:23:30'),
(36, 22, '127.0.0.1', '2025-08-27 07:24:23'),
(37, 22, '127.0.0.1', '2025-08-27 07:28:50'),
(38, 22, '127.0.0.1', '2025-08-27 07:29:35'),
(39, 22, '127.0.0.1', '2025-08-27 07:30:57'),
(40, 22, '127.0.0.1', '2025-08-27 07:31:43'),
(41, 22, '127.0.0.1', '2025-08-27 07:33:19'),
(42, 22, '127.0.0.1', '2025-08-27 07:34:41'),
(43, 22, '127.0.0.1', '2025-08-27 07:36:03'),
(44, 22, '127.0.0.1', '2025-08-27 07:39:43'),
(45, 19, '127.0.0.1', '2025-08-27 07:45:23'),
(46, 21, '127.0.0.1', '2025-08-27 08:13:39'),
(47, 20, '127.0.0.1', '2025-08-27 08:15:34'),
(48, 20, '127.0.0.1', '2025-08-27 08:23:41'),
(49, 20, '127.0.0.1', '2025-08-27 08:23:56'),
(50, 20, '127.0.0.1', '2025-08-27 08:24:22'),
(51, 20, '127.0.0.1', '2025-08-27 08:24:40'),
(52, 20, '127.0.0.1', '2025-08-27 08:25:04'),
(53, 16, '127.0.0.1', '2025-08-28 05:22:40'),
(54, 15, '127.0.0.1', '2025-08-28 05:23:52'),
(55, 21, '127.0.0.1', '2025-08-28 05:25:46'),
(56, 19, '127.0.0.1', '2025-08-28 05:39:32'),
(57, 16, '127.0.0.1', '2025-09-01 06:03:31'),
(58, 15, '127.0.0.1', '2025-09-01 06:08:21'),
(59, 13, '127.0.0.1', '2025-09-01 06:08:59'),
(60, 21, '127.0.0.1', '2025-09-01 06:35:19'),
(61, 22, '127.0.0.1', '2025-09-02 06:53:07'),
(62, 22, '127.0.0.1', '2025-09-02 06:54:24'),
(63, 22, '127.0.0.1', '2025-09-02 07:21:43'),
(64, 13, '127.0.0.1', '2025-09-02 07:23:44');

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

CREATE TABLE `project` (
  `p_id` int(11) NOT NULL,
  `p_name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `a_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `p_image` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `project`
--

INSERT INTO `project` (`p_id`, `p_name`, `description`, `a_id`, `created_at`, `updated_at`, `p_image`, `address`) VALUES
(2, 'บุรีรัมย์', 'Luxury condos in the heart of the city.', 4, '2025-05-22 08:59:21', '2025-08-21 13:44:40', 'OIP_1.webp', 'ในมือง บุรีรัมย์'),
(3, 'กาฬสินธุ์', 'Eco-friendly homes with large green spaces.', 4, '2025-05-22 08:59:21', '2025-08-26 11:35:17', 'istockphoto-1270000116-612x612_1.jpg', 'ในมือง กาฬสินธุ์'),
(6, 'ขอนแก่น', 'โปรโมชั่นจากโครงการ', 6, '2025-05-28 05:05:07', '2025-08-27 07:08:15', 'Khon-Kaen-1.jpg', 'ในเมือง ขอนแก่น');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `house`
--
ALTER TABLE `house`
  ADD PRIMARY KEY (`h_id`),
  ADD KEY `house_ibfk_1` (`t_id`),
  ADD KEY `f_id` (`f_id`);

--
-- Indexes for table `house_features`
--
ALTER TABLE `house_features`
  ADD PRIMARY KEY (`f_id`);

--
-- Indexes for table `house_images`
--
ALTER TABLE `house_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `house_id` (`house_id`);

--
-- Indexes for table `house_type`
--
ALTER TABLE `house_type`
  ADD PRIMARY KEY (`t_id`);

--
-- Indexes for table `house_views`
--
ALTER TABLE `house_views`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_house_views_created_at` (`created_at`),
  ADD KEY `idx_house_views_house_id` (`house_id`);

--
-- Indexes for table `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`p_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `house`
--
ALTER TABLE `house`
  MODIFY `h_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `house_features`
--
ALTER TABLE `house_features`
  MODIFY `f_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `house_images`
--
ALTER TABLE `house_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- AUTO_INCREMENT for table `house_type`
--
ALTER TABLE `house_type`
  MODIFY `t_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `house_views`
--
ALTER TABLE `house_views`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `project`
--
ALTER TABLE `project`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `house`
--
ALTER TABLE `house`
  ADD CONSTRAINT `house_ibfk_1` FOREIGN KEY (`t_id`) REFERENCES `house_type` (`t_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `house_ibfk_2` FOREIGN KEY (`f_id`) REFERENCES `house_features` (`f_id`) ON DELETE SET NULL;

--
-- Constraints for table `house_images`
--
ALTER TABLE `house_images`
  ADD CONSTRAINT `house_images_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `house` (`h_id`) ON DELETE CASCADE;

--
-- Constraints for table `house_views`
--
ALTER TABLE `house_views`
  ADD CONSTRAINT `fk_house_views_house` FOREIGN KEY (`house_id`) REFERENCES `house` (`h_id`) ON DELETE CASCADE;
--
-- Database: `test`
--
CREATE DATABASE IF NOT EXISTS `test` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `test`;
--
-- Database: `users`
--
CREATE DATABASE IF NOT EXISTS `users` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `users`;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `firstname`, `lastname`, `password`, `email`, `role`) VALUES
(1, 'admin', '', '', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'admin@rbru.ac.th', 1),
(2, 'student', '', '', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'student@rbru.ac.th', 2),
(3, 'advisor', '', '', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'advisor@rbru.ac.th', 3),
(4, 'mentor', '', '', '$2y$10$jh7/b3y49bCM9nWbL1YaP.FSTr1Hjw/74vChB1T6AL78WyIZ2lAYi', 'mentor@rbru.ac.th', 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
