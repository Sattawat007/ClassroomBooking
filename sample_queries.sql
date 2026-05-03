-- ============================================================
-- Classroom Booking System - SQL Query Examples
-- ตัวอย่าง SQL Queries สำหรับงบนทั่วไป
-- ============================================================


-- ==================== 1. SELECT Queries ====================

-- 1.1 ดึงข้อมูลการจองทั้งหมดพร้อมรายละเอียด (JOIN)
SELECT 
    b.booking_id,
    u.name AS 'ชื่อผู้ใช้',
    u.email AS 'อีเมล',
    r.room_name AS 'ชื่อห้อง',
    r.capacity AS 'ความจุ',
    ts.start_time AS 'เวลาเริ่ม',
    ts.end_time AS 'เวลาสิ้นสุด',
    b.date AS 'วันที่จอง'
FROM Bookings b
JOIN Users u ON b.user_id = u.user_id
JOIN Rooms r ON b.room_id = r.room_id
JOIN TimeSlots ts ON b.timeslot_id = ts.timeslot_id
ORDER BY b.date, ts.start_time;


-- 1.2 ดึงข้อมูลผู้ใช้พร้อมแผนก
SELECT 
    u.user_id,
    u.name AS 'ชื่อ',
    u.email AS 'อีเมล',
    d.dept_name AS 'แผนก'
FROM Users u
JOIN Departments d ON u.dept_id = d.dept_id
ORDER BY d.dept_name, u.name;


-- 1.3 ดึงข้อมูลห้องทั้งหมดพร้อมจำนวนการจอง
SELECT 
    r.room_id,
    r.room_name AS 'ชื่อห้อง',
    r.capacity AS 'ความจุ',
    COUNT(b.booking_id) AS 'จำนวนการจอง'
FROM Rooms r
LEFT JOIN Bookings b ON r.room_id = b.room_id
GROUP BY r.room_id
ORDER BY COUNT(b.booking_id) DESC;


-- 1.4 ดึงข้อมูลการจองในวันที่เฉพาะ
SELECT 
    b.booking_id,
    u.name AS 'ชื่อผู้ใช้',
    r.room_name AS 'ห้อง',
    ts.start_time AS 'เวลา',
    b.date AS 'วันที่'
FROM Bookings b
JOIN Users u ON b.user_id = u.user_id
JOIN Rooms r ON b.room_id = r.room_id
JOIN TimeSlots ts ON b.timeslot_id = ts.timeslot_id
WHERE b.date = '2026-05-05'
ORDER BY ts.start_time;


-- 1.5 ดึงข้อมูลการจองของผู้ใช้คนใดคนหนึ่ง
SELECT 
    b.booking_id,
    r.room_name AS 'ห้อง',
    ts.start_time AS 'เวลา',
    b.date AS 'วันที่'
FROM Bookings b
JOIN Rooms r ON b.room_id = r.room_id
JOIN TimeSlots ts ON b.timeslot_id = ts.timeslot_id
WHERE b.user_id = 1
ORDER BY b.date, ts.start_time;


-- 1.6 ดึงข้อมูลช่วงเวลาที่ไม่มีการจอง (ยังว่าง)
SELECT DISTINCT
    ts.timeslot_id,
    ts.start_time AS 'เวลาเริ่ม',
    ts.end_time AS 'เวลาสิ้นสุด'
FROM TimeSlots ts
WHERE ts.timeslot_id NOT IN (
    SELECT DISTINCT timeslot_id FROM Bookings
)
ORDER BY ts.start_time;


-- 1.7 ดึงจำนวนการจองต่อแผนก
SELECT 
    d.dept_name AS 'แผนก',
    COUNT(b.booking_id) AS 'จำนวนการจอง'
FROM Departments d
LEFT JOIN Users u ON d.dept_id = u.dept_id
LEFT JOIN Bookings b ON u.user_id = b.user_id
GROUP BY d.dept_id, d.dept_name
ORDER BY COUNT(b.booking_id) DESC;


-- ==================== 2. INSERT Queries ====================

-- 2.1 เพิ่มแผนกใหม่
INSERT INTO Departments (dept_name) VALUES ('Public Relations');


-- 2.2 เพิ่มผู้ใช้งานใหม่
INSERT INTO Users (name, email, dept_id) 
VALUES ('นายสมพงษ์ นวม', 'sompong@company.com', 1);


-- 2.3 เพิ่มห้องเรียนใหม่
INSERT INTO Rooms (room_name, capacity) 
VALUES ('ห้อง 401', 55);


-- 2.4 เพิ่มช่วงเวลาใหม่
INSERT INTO TimeSlots (start_time, end_time) 
VALUES ('09:00', '11:00');


-- 2.5 เพิ่มการจองใหม่
INSERT INTO Bookings (user_id, room_id, timeslot_id, date) 
VALUES (1, 2, 3, '2026-05-10');


-- 2.6 เพิ่มหลายการจองในครั้งเดียว
INSERT INTO Bookings (user_id, room_id, timeslot_id, date) VALUES
    (2, 3, 2, '2026-05-10'),
    (3, 4, 3, '2026-05-10'),
    (4, 5, 1, '2026-05-10');


-- ==================== 3. UPDATE Queries ====================

-- 3.1 แก้ไขข้อมูลผู้ใช้
UPDATE Users 
SET email = 'newemail@company.com' 
WHERE user_id = 1;


-- 3.2 แก้ไขการจองให้ใช้ห้องอื่น
UPDATE Bookings 
SET room_id = 5, timeslot_id = 2 
WHERE booking_id = 1;


-- 3.3 แก้ไขความจุของห้อง
UPDATE Rooms 
SET capacity = 40 
WHERE room_name = 'ห้อง 101';


-- 3.4 แก้ไขแผนก
UPDATE Departments 
SET dept_name = 'Information Technology Department' 
WHERE dept_id = 1;


-- ==================== 4. DELETE Queries ====================

-- 4.1 ลบการจองเพียงรายการเดียว
DELETE FROM Bookings 
WHERE booking_id = 1;


-- 4.2 ลบการจองทั้งหมดของผู้ใช้คนใดคนหนึ่ง
DELETE FROM Bookings 
WHERE user_id = 1;


-- 4.3 ลบการจองในวันที่เฉพาะ
DELETE FROM Bookings 
WHERE date = '2026-05-05';


-- 4.4 ลบห้องที่ไม่มีการจอง (ต้องระวัง Foreign Key)
-- DELETE FROM Rooms 
-- WHERE room_id NOT IN (SELECT DISTINCT room_id FROM Bookings);


-- ==================== 5. Complex Queries ====================

-- 5.1 ห้องที่มีการจองมากที่สุด
SELECT 
    r.room_name AS 'ชื่อห้อง',
    COUNT(b.booking_id) AS 'จำนวนการจอง',
    AVG(r.capacity) AS 'ความจุเฉลี่ย'
FROM Rooms r
LEFT JOIN Bookings b ON r.room_id = b.room_id
GROUP BY r.room_id
HAVING COUNT(b.booking_id) > 0
ORDER BY COUNT(b.booking_id) DESC;


-- 5.2 ผู้ใช้ที่มีการจองมากที่สุด
SELECT 
    u.name AS 'ชื่อผู้ใช้',
    COUNT(b.booking_id) AS 'จำนวนการจอง'
FROM Users u
LEFT JOIN Bookings b ON u.user_id = b.user_id
GROUP BY u.user_id
ORDER BY COUNT(b.booking_id) DESC
LIMIT 5;


-- 5.3 ช่วงเวลาที่มีการจองมากที่สุด
SELECT 
    ts.start_time,
    ts.end_time,
    COUNT(b.booking_id) AS 'จำนวนการจอง'
FROM TimeSlots ts
LEFT JOIN Bookings b ON ts.timeslot_id = b.timeslot_id
GROUP BY ts.timeslot_id
ORDER BY COUNT(b.booking_id) DESC;


-- 5.4 ความขัดแย้งของการจอง (ห้องเดียวเวลาเดียวแต่วันต่างกัน)
SELECT 
    r.room_name,
    ts.start_time,
    ts.end_time,
    COUNT(*) AS 'จำนวนการจอง',
    GROUP_CONCAT(b.date, ', ') AS 'วันที่'
FROM Bookings b
JOIN Rooms r ON b.room_id = r.room_id
JOIN TimeSlots ts ON b.timeslot_id = ts.timeslot_id
GROUP BY b.room_id, b.timeslot_id
HAVING COUNT(*) > 1;


-- 5.5 สถิติการจองตามแผนกและวันที่
SELECT 
    d.dept_name AS 'แผนก',
    b.date AS 'วันที่',
    COUNT(b.booking_id) AS 'จำนวนการจอง'
FROM Bookings b
JOIN Users u ON b.user_id = u.user_id
JOIN Departments d ON u.dept_id = d.dept_id
GROUP BY d.dept_id, b.date
ORDER BY b.date, d.dept_name;


-- ==================== 6. Data Validation Queries ====================

-- 6.1 ตรวจสอบผู้ใช้ที่ไม่มีอีเมล
SELECT * FROM Users WHERE email IS NULL;


-- 6.2 ตรวจสอบห้องที่มีความจุเป็นศูนย์หรือ NULL
SELECT * FROM Rooms WHERE capacity IS NULL OR capacity = 0;


-- 6.3 ตรวจสอบข้อมูล orphan (ผู้ใช้ที่ไม่มีแผนกอยู่ในระบบ)
SELECT u.* FROM Users u
WHERE u.dept_id NOT IN (SELECT dept_id FROM Departments);


-- 6.4 ตรวจสอบการจองที่ซ้ำกัน (ห้องเดียวเวลาเดียววันเดียว)
SELECT 
    room_id, 
    timeslot_id, 
    date, 
    COUNT(*) AS 'จำนวนซ้ำ'
FROM Bookings
GROUP BY room_id, timeslot_id, date
HAVING COUNT(*) > 1;


-- ==================== 7. Utility Queries ====================

-- 7.1 ดึงจำนวนข้อมูลทั้งหมดในแต่ละตาราง
SELECT 'Departments' AS 'Table', COUNT(*) FROM Departments
UNION
SELECT 'Users', COUNT(*) FROM Users
UNION
SELECT 'Rooms', COUNT(*) FROM Rooms
UNION
SELECT 'TimeSlots', COUNT(*) FROM TimeSlots
UNION
SELECT 'Bookings', COUNT(*) FROM Bookings;


-- 7.2 ดึงข้อมูล ID ที่ใหญ่ที่สุดในแต่ละตาราง
SELECT MAX(dept_id) AS 'Max Dept ID' FROM Departments;
SELECT MAX(user_id) AS 'Max User ID' FROM Users;
SELECT MAX(room_id) AS 'Max Room ID' FROM Rooms;
SELECT MAX(booking_id) AS 'Max Booking ID' FROM Bookings;


-- ============================================================
-- Note: สำหรับการรันชุด queries นี้ ควรใช้ sqlite3 CLI ดังนี้:
-- sqlite3 classroom_booking.db < sample_queries.sql
-- ============================================================
