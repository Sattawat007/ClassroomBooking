"""
Classroom Booking System - SQLite Database Setup Script
สคริปต์สำหรับสร้างฐานข้อมูล SQLite พร้อมตารางและข้อมูลตัวอย่าง
"""

import sqlite3
from sqlite3 import Error
from datetime import datetime

# ==================== Database Setup ====================

def create_connection(db_file):
    """
    สร้างการเชื่อมต่อกับฐานข้อมูล SQLite
    ถ้าไฟล์ไม่มี จะสร้างใหม่อัตโนมัติ
    
    Args:
        db_file (str): ชื่อไฟล์ฐานข้อมูล
    
    Returns:
        sqlite3.Connection: Connection object หรือ None หากเกิด error
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # เปิด Foreign Key Constraint (สำคัญสำหรับ Relational Database)
        conn.execute("PRAGMA foreign_keys = ON")
        print(f"✓ สร้างการเชื่อมต่อกับฐานข้อมูล: {db_file}")
        return conn
    except Error as e:
        print(f"✗ Error: {e}")
        return None


def create_tables(conn):
    """
    สร้างทั้ง 5 ตารางในฐานข้อมูล
    """
    cursor = conn.cursor()
    
    try:
        # ตาราง 1: Departments (แผนก)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Departments (
                dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
                dept_name TEXT NOT NULL UNIQUE
            )
        """)
        
        # ตาราง 2: Users (ผู้ใช้งาน)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                dept_id INTEGER NOT NULL,
                FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
            )
        """)
        
        # ตาราง 3: Rooms (ห้องเรียน)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_name TEXT NOT NULL,
                capacity INTEGER
            )
        """)
        
        # ตาราง 4: TimeSlots (ช่วงเวลา)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TimeSlots (
                timeslot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL
            )
        """)
        
        # ตาราง 5: Bookings (การจอง)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                timeslot_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (room_id) REFERENCES Rooms(room_id),
                FOREIGN KEY (timeslot_id) REFERENCES TimeSlots(timeslot_id)
            )
        """)
        
        conn.commit()
        print("✓ สร้างทั้ง 5 ตารางสำเร็จ")
        
    except Error as e:
        print(f"✗ Error สร้างตาราง: {e}")


# ==================== Insert Mock Data ====================

def insert_departments(conn):
    """
    เพิ่มข้อมูล 10 แผนก
    """
    departments = [
        ("Information Technology",),
        ("Human Resources",),
        ("Finance",),
        ("Marketing",),
        ("Sales",),
        ("Operations",),
        ("Research & Development",),
        ("Customer Service",),
        ("Administration",),
        ("Legal",),
    ]
    
    cursor = conn.cursor()
    try:
        cursor.executemany("INSERT OR IGNORE INTO Departments (dept_name) VALUES (?)", departments)
        conn.commit()
        print(f"✓ เพิ่มข้อมูล Departments: {len(departments)} แถว")
    except Error as e:
        print(f"✗ Error: {e}")


def insert_users(conn):
    """
    เพิ่มข้อมูล 10 ผู้ใช้งาน
    """
    users = [
        ("นายสมชาย ใจดี", "somchai@company.com", 1),
        ("นางสาวกรรม ทำงาน", "gam@company.com", 2),
        ("นายสมศักดิ์ เรียบร้อย", "somsak@company.com", 3),
        ("นางจิตรา บัญชี", "chittra@company.com", 3),
        ("นายวิทย์ ข้อมูล", "wit@company.com", 1),
        ("นางดวงตา ขายดี", "duang@company.com", 5),
        ("นายวรรณ การตลาด", "wan@company.com", 4),
        ("นางสาวจิตรา ดำเนิน", "jitra@company.com", 6),
        ("นายสัตบรรเพ ศึกษา", "satbun@company.com", 7),
        ("นางสาววีรุณ รับใช้", "veera@company.com", 8),
    ]
    
    cursor = conn.cursor()
    try:
        cursor.executemany(
            "INSERT OR IGNORE INTO Users (name, email, dept_id) VALUES (?, ?, ?)",
            users
        )
        conn.commit()
        print(f"✓ เพิ่มข้อมูล Users: {len(users)} แถว")
    except Error as e:
        print(f"✗ Error: {e}")


def insert_rooms(conn):
    """
    เพิ่มข้อมูล 10 ห้องเรียน
    """
    rooms = [
        ("ห้อง 101", 30),
        ("ห้อง 102", 25),
        ("ห้อง 103", 40),
        ("ห้อง 201", 50),
        ("ห้อง 202", 35),
        ("ห้อง 203", 20),
        ("ห้อง 301", 45),
        ("ห้อง 302", 60),
        ("ห้อง Auditorium", 150),
        ("Meeting Room A", 15),
    ]
    
    cursor = conn.cursor()
    try:
        cursor.executemany(
            "INSERT OR IGNORE INTO Rooms (room_name, capacity) VALUES (?, ?)",
            rooms
        )
        conn.commit()
        print(f"✓ เพิ่มข้อมูล Rooms: {len(rooms)} แถว")
    except Error as e:
        print(f"✗ Error: {e}")


def insert_timeslots(conn):
    """
    เพิ่มข้อมูล 10 ช่วงเวลา
    """
    timeslots = [
        ("08:00", "10:00"),
        ("10:00", "12:00"),
        ("13:00", "15:00"),
        ("15:00", "17:00"),
        ("17:00", "19:00"),
        ("08:30", "10:30"),
        ("11:00", "13:00"),
        ("14:00", "16:00"),
        ("16:00", "18:00"),
        ("18:00", "20:00"),
    ]
    
    cursor = conn.cursor()
    try:
        cursor.executemany(
            "INSERT OR IGNORE INTO TimeSlots (start_time, end_time) VALUES (?, ?)",
            timeslots
        )
        conn.commit()
        print(f"✓ เพิ่มข้อมูล TimeSlots: {len(timeslots)} แถว")
    except Error as e:
        print(f"✗ Error: {e}")


def insert_bookings(conn):
    """
    เพิ่มข้อมูล 10 การจอง
    """
    bookings = [
        (1, 1, 1, "2026-05-05"),
        (2, 2, 2, "2026-05-05"),
        (3, 3, 3, "2026-05-05"),
        (4, 4, 1, "2026-05-06"),
        (5, 5, 2, "2026-05-06"),
        (6, 1, 4, "2026-05-06"),
        (7, 2, 5, "2026-05-07"),
        (8, 3, 6, "2026-05-07"),
        (9, 4, 7, "2026-05-07"),
        (10, 5, 8, "2026-05-08"),
    ]
    
    cursor = conn.cursor()
    try:
        cursor.executemany(
            "INSERT OR IGNORE INTO Bookings (user_id, room_id, timeslot_id, date) VALUES (?, ?, ?, ?)",
            bookings
        )
        conn.commit()
        print(f"✓ เพิ่มข้อมูล Bookings: {len(bookings)} แถว")
    except Error as e:
        print(f"✗ Error: {e}")


# ==================== Display Data ====================

def display_table_count(conn):
    """
    แสดงจำนวนแถวในแต่ละตาราง
    """
    cursor = conn.cursor()
    tables = ['Departments', 'Users', 'Rooms', 'TimeSlots', 'Bookings']
    
    print("\n" + "="*50)
    print("จำนวนข้อมูลในแต่ละตาราง")
    print("="*50)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:20} → {count} แถว")


# ==================== SQL Query Examples ====================

def display_query_examples(conn):
    """
    แสดงตัวอย่าง SQL Queries
    """
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print("ตัวอย่าง SQL Queries")
    print("="*50)
    
    # 1. JOIN Query - ดึงข้อมูลการจองพร้อมชื่อผู้ใช้, ห้อง และเวลา
    print("\n[1] JOIN Query - ดึงข้อมูลการจองพร้อมรายละเอียด")
    print("-" * 50)
    query1 = """
    SELECT 
        b.booking_id,
        u.name AS 'ชื่อผู้ใช้',
        r.room_name AS 'ชื่อห้อง',
        ts.start_time AS 'เวลาเริ่ม',
        ts.end_time AS 'เวลาสิ้นสุด',
        b.date AS 'วันที่จอง'
    FROM Bookings b
    JOIN Users u ON b.user_id = u.user_id
    JOIN Rooms r ON b.room_id = r.room_id
    JOIN TimeSlots ts ON b.timeslot_id = ts.timeslot_id
    ORDER BY b.date, ts.start_time
    """
    print("SQL Query:")
    print(query1)
    print("\nผลลัพธ์:")
    cursor.execute(query1)
    results = cursor.fetchall()
    for row in results[:5]:  # แสดง 5 แถวแรก
        print(f"  Booking ID {row[0]}: {row[1]} จองห้อง {row[2]} เวลา {row[3]}-{row[4]} วันที่ {row[5]}")
    print(f"  ... (แสดง 5 แถว จากทั้งหมด {len(results)} แถว)")
    
    # 2. SELECT Query - ดึงข้อมูลผู้ใช้พร้อมแผนก
    print("\n[2] SELECT with JOIN - ดึงข้อมูลผู้ใช้พร้อมแผนก")
    print("-" * 50)
    query2 = """
    SELECT 
        u.user_id,
        u.name AS 'ชื่อ',
        u.email AS 'อีเมล',
        d.dept_name AS 'แผนก'
    FROM Users u
    JOIN Departments d ON u.dept_id = d.dept_id
    LIMIT 5
    """
    print("SQL Query:")
    print(query2)
    print("\nผลลัพธ์:")
    cursor.execute(query2)
    for row in cursor.fetchall():
        print(f"  {row[0]}. {row[1]:20} | {row[2]:20} | {row[3]}")
    
    # 3. INSERT Query Example
    print("\n[3] INSERT Query Example - วิธีเพิ่มการจองใหม่")
    print("-" * 50)
    insert_example = """
    INSERT INTO Bookings (user_id, room_id, timeslot_id, date)
    VALUES (1, 2, 3, '2026-05-10')
    """
    print("SQL Query:")
    print(insert_example)
    print("(โค้ดตัวอย่าง - ไม่ได้รันจริง)")
    
    # 4. UPDATE Query Example
    print("\n[4] UPDATE Query Example - วิธีแก้ไขการจอง")
    print("-" * 50)
    update_example = """
    UPDATE Bookings
    SET room_id = 5, timeslot_id = 2
    WHERE booking_id = 1
    """
    print("SQL Query:")
    print(update_example)
    print("(โค้ดตัวอย่าง - ไม่ได้รันจริง)")
    
    # 5. DELETE Query Example
    print("\n[5] DELETE Query Example - วิธีลบการจอง")
    print("-" * 50)
    delete_example = """
    DELETE FROM Bookings
    WHERE booking_id = 1
    """
    print("SQL Query:")
    print(delete_example)
    print("(โค้ดตัวอย่าง - ไม่ได้รันจริง)")
    
    # 6. Aggregation Query
    print("\n[6] Aggregation Query - จำนวนการจองต่อห้อง")
    print("-" * 50)
    query6 = """
    SELECT 
        r.room_name AS 'ชื่อห้อง',
        COUNT(b.booking_id) AS 'จำนวนการจอง'
    FROM Rooms r
    LEFT JOIN Bookings b ON r.room_id = b.room_id
    GROUP BY r.room_id
    ORDER BY COUNT(b.booking_id) DESC
    """
    print("SQL Query:")
    print(query6)
    print("\nผลลัพธ์:")
    cursor.execute(query6)
    for row in cursor.fetchall():
        print(f"  {row[0]:20} → {row[1]} ครั้ง")


# ==================== Main Function ====================

def main():
    """
    ฟังก์ชันหลักในการรันทั้งสคริปต์
    """
    print("\n" + "="*50)
    print("Classroom Booking System")
    print("Database Setup Script")
    print("="*50 + "\n")
    
    db_file = "/Users/sattawat/Documents/ClassroomBooking System/classroom_booking.db"
    
    # สร้างการเชื่อมต่อ
    conn = create_connection(db_file)
    
    if conn is not None:
        # สร้างตาราง
        print("\n[1] สร้างตาราง...")
        create_tables(conn)
        
        # เพิ่มข้อมูลตัวอย่าง
        print("\n[2] เพิ่มข้อมูลตัวอย่าง...")
        insert_departments(conn)
        insert_users(conn)
        insert_rooms(conn)
        insert_timeslots(conn)
        insert_bookings(conn)
        
        # แสดงจำนวนข้อมูล
        display_table_count(conn)
        
        # แสดงตัวอย่าง Query
        print("\n[3] ตัวอย่าง SQL Queries...")
        display_query_examples(conn)
        
        # ปิดการเชื่อมต่อ
        conn.close()
        
        print("\n" + "="*50)
        print("✓ สำเร็จ! ฐานข้อมูล classroom_booking.db พร้อมใช้งาน")
        print("="*50 + "\n")
    else:
        print("✗ ไม่สามารถสร้างการเชื่อมต่อกับฐานข้อมูล")


if __name__ == "__main__":
    main()
