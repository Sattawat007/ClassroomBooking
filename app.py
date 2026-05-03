"""
Classroom Booking System - Flask Web Application
เว็บแอปพลิเคชันสำหรับจัดการการจองห้องเรียน
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

# ==================== Flask App Configuration ====================

app = Flask(__name__)
app.secret_key = 'classroom_booking_secret_key_2026'

# กำหนด path ของฐานข้อมูลให้รองรับทั้ง Windows และ PythonAnywhere
DB_PATH = os.path.join(os.path.dirname(__file__), 'classroom_booking.db')

# ==================== Database Functions ====================

def get_db_connection():
    """
    สร้างการเชื่อมต่อกับฐานข้อมูล SQLite
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # ให้สามารถเข้าถึงคอลัมน์ด้วยชื่อได้
    return conn


def get_all_bookings():
    """
    ดึงข้อมูลการจองทั้งหมดพร้อม JOIN กับตารางอื่นๆ
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        b.booking_id,
        b.date,
        u.name AS user_name,
        u.email AS user_email,
        r.room_name,
        r.capacity,
        ts.start_time,
        ts.end_time,
        d.dept_name
    FROM Bookings b
    JOIN Users u ON b.user_id = u.user_id
    JOIN Rooms r ON b.room_id = r.room_id
    JOIN TimeSlots ts ON b.timeslot_id = ts.timeslot_id
    JOIN Departments d ON u.dept_id = d.dept_id
    ORDER BY b.date DESC, ts.start_time DESC
    """

    cursor.execute(query)
    bookings = cursor.fetchall()
    conn.close()

    return bookings


def get_booking_by_id(booking_id):
    """
    ดึงข้อมูลการจองตาม ID
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        b.booking_id,
        b.user_id,
        b.room_id,
        b.timeslot_id,
        b.date,
        u.name AS user_name,
        r.room_name,
        ts.start_time,
        ts.end_time
    FROM Bookings b
    JOIN Users u ON b.user_id = u.user_id
    JOIN Rooms r ON b.room_id = r.room_id
    JOIN TimeSlots ts ON b.timeslot_id = ts.timeslot_id
    WHERE b.booking_id = ?
    """

    cursor.execute(query, (booking_id,))
    booking = cursor.fetchone()
    conn.close()

    return booking


def get_users():
    """
    ดึงข้อมูลผู้ใช้ทั้งหมด
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email FROM Users ORDER BY name")
    users = cursor.fetchall()
    conn.close()
    return users


def get_rooms():
    """
    ดึงข้อมูลห้องทั้งหมด
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room_id, room_name, capacity FROM Rooms ORDER BY room_name")
    rooms = cursor.fetchall()
    conn.close()
    return rooms


def get_timeslots():
    """
    ดึงข้อมูลช่วงเวลาทั้งหมด
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT timeslot_id, start_time, end_time FROM TimeSlots ORDER BY start_time")
    timeslots = cursor.fetchall()
    conn.close()
    return timeslots


def add_booking(user_id, room_id, timeslot_id, date):
    """
    เพิ่มการจองใหม่
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Bookings (user_id, room_id, timeslot_id, date)
            VALUES (?, ?, ?, ?)
        """, (user_id, room_id, timeslot_id, date))

        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()
        return booking_id
    except sqlite3.Error as e:
        conn.close()
        raise e


def update_booking(booking_id, user_id, room_id, timeslot_id, date):
    """
    แก้ไขการจอง
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE Bookings
            SET user_id = ?, room_id = ?, timeslot_id = ?, date = ?
            WHERE booking_id = ?
        """, (user_id, room_id, timeslot_id, date, booking_id))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        conn.close()
        raise e


def delete_booking(booking_id):
    """
    ลบการจอง
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM Bookings WHERE booking_id = ?", (booking_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        conn.close()
        raise e


def get_booking_stats():
    """
    ดึงสถิติการจองสำหรับ Dashboard
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # จำนวนการจองทั้งหมด
    cursor.execute("SELECT COUNT(*) FROM Bookings")
    total_bookings = cursor.fetchone()[0]

    # จำนวนห้องทั้งหมด
    cursor.execute("SELECT COUNT(*) FROM Rooms")
    total_rooms = cursor.fetchone()[0]

    # จำนวนผู้ใช้ทั้งหมด
    cursor.execute("SELECT COUNT(*) FROM Users")
    total_users = cursor.fetchone()[0]

    # การจองวันนี้ (ถ้ามี)
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM Bookings WHERE date = ?", (today,))
    today_bookings = cursor.fetchone()[0]

    conn.close()

    return {
        'total_bookings': total_bookings,
        'total_rooms': total_rooms,
        'total_users': total_users,
        'today_bookings': today_bookings
    }


# ==================== Flask Routes ====================

@app.route('/')
def index():
    """
    หน้า Dashboard แสดงรายการการจองทั้งหมด
    """
    try:
        bookings = get_all_bookings()
        stats = get_booking_stats()
        return render_template('index.html', bookings=bookings, stats=stats)
    except Exception as e:
        flash(f'เกิดข้อผิดพลาด: {str(e)}', 'error')
        return render_template('index.html', bookings=[], stats={'total_bookings': 0, 'total_rooms': 0, 'total_users': 0, 'today_bookings': 0})


@app.route('/add', methods=['GET', 'POST'])
def add_booking_route():
    """
    หน้าเพิ่มการจองใหม่
    """
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            room_id = request.form['room_id']
            timeslot_id = request.form['timeslot_id']
            date = request.form['date']

            # ตรวจสอบข้อมูล
            if not all([user_id, room_id, timeslot_id, date]):
                flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'error')
                return redirect(url_for('add_booking_route'))

            # เพิ่มการจอง
            booking_id = add_booking(user_id, room_id, timeslot_id, date)
            flash(f'เพิ่มการจองสำเร็จ (ID: {booking_id})', 'success')
            return redirect(url_for('index'))

        except sqlite3.IntegrityError:
            flash('ไม่สามารถเพิ่มการจองได้ อาจมีข้อมูลซ้ำหรือข้อมูลอ้างอิงไม่ถูกต้อง', 'error')
        except Exception as e:
            flash(f'เกิดข้อผิดพลาด: {str(e)}', 'error')

    # GET request - แสดงฟอร์ม
    try:
        users = get_users()
        rooms = get_rooms()
        timeslots = get_timeslots()
        return render_template('add_booking.html', users=users, rooms=rooms, timeslots=timeslots)
    except Exception as e:
        flash(f'เกิดข้อผิดพลาดในการโหลดข้อมูล: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/edit/<int:booking_id>', methods=['GET', 'POST'])
def edit_booking_route(booking_id):
    """
    หน้าแก้ไขการจอง
    """
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            room_id = request.form['room_id']
            timeslot_id = request.form['timeslot_id']
            date = request.form['date']

            # ตรวจสอบข้อมูล
            if not all([user_id, room_id, timeslot_id, date]):
                flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'error')
                return redirect(url_for('edit_booking_route', booking_id=booking_id))

            # แก้ไขการจอง
            update_booking(booking_id, user_id, room_id, timeslot_id, date)
            flash('แก้ไขการจองสำเร็จ', 'success')
            return redirect(url_for('index'))

        except sqlite3.IntegrityError:
            flash('ไม่สามารถแก้ไขการจองได้ ข้อมูลอ้างอิงไม่ถูกต้อง', 'error')
        except Exception as e:
            flash(f'เกิดข้อผิดพลาด: {str(e)}', 'error')

    # GET request - แสดงฟอร์มพร้อมข้อมูลเดิม
    try:
        booking = get_booking_by_id(booking_id)
        if not booking:
            flash('ไม่พบข้อมูลการจองที่ระบุ', 'error')
            return redirect(url_for('index'))

        users = get_users()
        rooms = get_rooms()
        timeslots = get_timeslots()

        return render_template('edit_booking.html',
                             booking=booking,
                             users=users,
                             rooms=rooms,
                             timeslots=timeslots)
    except Exception as e:
        flash(f'เกิดข้อผิดพลาดในการโหลดข้อมูล: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/delete/<int:booking_id>', methods=['POST'])
def delete_booking_route(booking_id):
    """
    ลบการจอง
    """
    try:
        delete_booking(booking_id)
        flash('ลบการจองสำเร็จ', 'success')
    except Exception as e:
        flash(f'เกิดข้อผิดพลาดในการลบ: {str(e)}', 'error')

    return redirect(url_for('index'))


# ==================== Error Handlers ====================

@app.errorhandler(404)
def page_not_found(e):
    """
    จัดการหน้า 404
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """
    จัดการข้อผิดพลาดภายในเซิร์ฟเวอร์
    """
    return render_template('500.html'), 500


# ==================== Main ====================

if __name__ == '__main__':
    # ตรวจสอบว่าไฟล์ฐานข้อมูลมีอยู่หรือไม่
    if not os.path.exists(DB_PATH):
        print(f"⚠️  ไม่พบไฟล์ฐานข้อมูล: {DB_PATH}")
        print("กรุณารัน setup_database.py ก่อน")
        exit(1)

    print("🚀 Classroom Booking System")
    print(f"📁 Database: {DB_PATH}")
    print("🌐 Starting Flask server...")

    # รัน Flask app
    app.run(debug=True, host='0.0.0.0', port=8000)
