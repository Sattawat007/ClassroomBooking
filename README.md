# Classroom Booking System - Flask Web App

## 📋 ภาพรวม
เว็บแอปพลิเคชันสำหรับจัดการการจองห้องเรียน สร้างด้วย Flask และ Tailwind CSS มีฟีเจอร์ CRUD แบบครบครัน

---

## 🚀 การเริ่มใช้งาน

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. เตรียมฐานข้อมูล
```bash
python3 setup_database.py
```

### 3. รันเว็บแอป
```bash
python3 app.py
```

### 4. เข้าถึงเว็บไซต์
เปิดเบราว์เซอร์ไปที่: `http://localhost:8000`

---

## 📁 โครงสร้างโปรเจกต์

```
ClassroomBooking System/
├── app.py                          # Flask Web Application
├── setup_database.py              # Database Setup Script
├── classroom_booking.db           # SQLite Database
├── requirements.txt               # Python Dependencies
├── sample_queries.sql             # SQL Query Examples
├── templates/                     # HTML Templates
│   ├── index.html                 # Dashboard Page
│   ├── add_booking.html           # Add Booking Form
│   └── edit_booking.html          # Edit Booking Form
└── README.md                      # This file
```

---

## 🎨 ฟีเจอร์หลัก

### ✅ Dashboard (หน้าแรก)
- **สถิติการจอง**: แสดงจำนวนการจองทั้งหมด ห้องเรียน ผู้ใช้ และการจองวันนี้
- **ตารางการจอง**: แสดงรายการการจองทั้งหมดพร้อมข้อมูลแบบ JOIN
- **การจัดการ**: ปุ่มแก้ไขและลบการจอง
- **Responsive Design**: ดูได้ทั้งบนเดสก์ท็อปและมือถือ

### ✅ เพิ่มการจอง
- **ฟอร์มเพิ่มการจอง**: เลือกผู้ใช้ ห้องเรียน ช่วงเวลา และวันที่
- **Dropdown**: เลือกข้อมูลจากฐานข้อมูลที่มีอยู่
- **Validation**: ตรวจสอบข้อมูลก่อนบันทึก
- **Flash Messages**: แสดงผลการทำงาน

### ✅ แก้ไขการจอง
- **ฟอร์มแก้ไข**: แก้ไขข้อมูลการจองที่มีอยู่
- **ข้อมูลเดิม**: แสดงข้อมูลปัจจุบันให้เห็น
- **Validation**: ตรวจสอบข้อมูลก่อนบันทึก

### ✅ ลบการจอง
- **การยืนยัน**: แสดง dialog ยืนยันก่อนลบ
- **Flash Messages**: แสดงผลการลบ

---

## 🎨 ออกแบบ UI/UX

### ธีมสี: Purple & Orange
- **Primary (Purple)**: สำหรับปุ่มหลัก และ accent colors
- **Secondary (Orange)**: สำหรับปุ่มรอง และ highlight
- **Gray Scale**: สำหรับพื้นหลังและข้อความ

### Responsive Design
- **Mobile First**: ออกแบบให้ใช้งานบนมือถือได้สะดวก
- **Grid Layout**: จัดวางองค์ประกอบให้สมดุล
- **Card Design**: ใช้การ์ดเพื่อจัดกลุ่มข้อมูล

### Components
- **Navigation**: Header กับปุ่มนำทาง
- **Statistics Cards**: แสดงตัวเลขสถิติ
- **Data Table**: แสดงข้อมูลในรูปแบบตาราง
- **Forms**: ฟอร์มสำหรับเพิ่ม/แก้ไขข้อมูล
- **Flash Messages**: แสดงข้อความแจ้งเตือน

---

## 🔧 เทคนิคการพัฒนา

### Backend (Flask)
```python
# Database Connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# CRUD Operations
def get_all_bookings():  # READ
def add_booking():       # CREATE
def update_booking():    # UPDATE
def delete_booking():    # DELETE

# Routes
@app.route('/')                    # Dashboard
@app.route('/add', methods=['GET', 'POST'])    # Add booking
@app.route('/edit/<id>', methods=['GET', 'POST'])  # Edit booking
@app.route('/delete/<id>', methods=['POST'])   # Delete booking
```

### Frontend (HTML + Tailwind CSS)
```html
<!-- Statistics Cards -->
<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
    <div class="bg-white rounded-xl shadow-lg p-6 border-l-4 border-primary-500">
        <!-- Card content -->
    </div>
</div>

<!-- Data Table -->
<table class="min-w-full divide-y divide-gray-200">
    <thead class="bg-primary-50">
        <tr>
            <!-- Table headers -->
        </tr>
    </thead>
    <tbody>
        <!-- Table rows -->
    </tbody>
</table>
```

### SQL JOIN Query
```sql
SELECT
    b.booking_id,
    u.name AS user_name,
    r.room_name,
    ts.start_time,
    ts.end_time,
    b.date
FROM Bookings b
JOIN Users u ON b.user_id = u.user_id
JOIN Rooms r ON b.room_id = r.room_id
JOIN TimeSlots ts ON b.timeslot_id = ts.timeslot_id
ORDER BY b.date DESC, ts.start_time DESC
```

---

## 📊 ฐานข้อมูล Schema

### ตารางหลักที่ใช้งาน
- **Bookings**: เก็บข้อมูลการจอง (user_id, room_id, timeslot_id, date)
- **Users**: ข้อมูลผู้ใช้ (name, email, dept_id)
- **Rooms**: ข้อมูลห้องเรียน (room_name, capacity)
- **TimeSlots**: ช่วงเวลา (start_time, end_time)

### ความสัมพันธ์ (Foreign Keys)
```
Bookings → Users (user_id)
Bookings → Rooms (room_id)
Bookings → TimeSlots (timeslot_id)
Users → Departments (dept_id)
```

---

## 🛠️ การปรับแต่ง

### เปลี่ยนธีมสี
แก้ไขใน `tailwind.config` ในไฟล์ HTML:
```javascript
colors: {
    primary: { /* Purple colors */ },
    secondary: { /* Orange colors */ }
}
```

### เพิ่มฟีลด์ใหม่
1. แก้ไขฐานข้อมูลใน `setup_database.py`
2. เพิ่มฟิลด์ในฟอร์ม HTML
3. ปรับปรุงฟังก์ชันใน `app.py`

### เพิ่มการตรวจสอบ
เพิ่ม validation ใน routes:
```python
if not all([user_id, room_id, timeslot_id, date]):
    flash('กรุณากรอกข้อมูลให้ครบถ้วน', 'error')
    return redirect(url_for('add_booking_route'))
```

---

## 🔒 ความปลอดภัย

### Input Validation
- ตรวจสอบข้อมูลทุกฟิลด์ก่อนบันทึก
- ใช้ `required` ในฟอร์ม HTML
- ตรวจสอบ Foreign Key constraints

### SQL Injection Protection
- ใช้ parameterized queries
- ไม่ concatenate SQL strings

### Error Handling
- จัดการ exceptions อย่างเหมาะสม
- แสดงข้อความ error ที่เป็นมิตร

---

## 📱 การใช้งานบนมือถือ

เว็บไซต์ออกแบบมาให้ใช้งานบนมือถือได้สะดวก:
- **Responsive Grid**: ปรับขนาดตามหน้าจอ
- **Touch-Friendly**: ปุ่มและลิงก์มีขนาดเหมาะสม
- **Mobile Navigation**: เมนูที่ใช้งานง่าย

---

## 🚀 Deployment

### สำหรับ Production
```bash
# ตั้งค่า environment variables
export FLASK_ENV=production
export FLASK_DEBUG=0

# รันด้วย Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### สำหรับ PythonAnywhere
1. Upload ไฟล์ทั้งหมด
2. ติดตั้ง dependencies
3. รัน setup_database.py
4. ตั้งค่า WSGI file ชี้ไปที่ app

---

## 🐛 การแก้ปัญหา

### Port ถูกใช้งาน
```bash
# ตรวจสอบ port ที่ถูกใช้
lsof -i :8000

# เปลี่ยน port ใน app.py
app.run(debug=True, port=3000)
```

### Database Error
```bash
# ลบและสร้างฐานข้อมูลใหม่
rm classroom_booking.db
python3 setup_database.py
```

### Dependencies Error
```bash
# ติดตั้งใหม่
pip install --upgrade -r requirements.txt
```

---

## 📈 การพัฒนาต่อ

### ฟีเจอร์ที่สามารถเพิ่มเติม
1. **User Authentication**: เข้าสู่ระบบและจัดการสิทธิ์
2. **Booking Calendar**: ปฏิทินแสดงการจอง
3. **Email Notifications**: แจ้งเตือนการจอง
4. **Room Availability**: ตรวจสอบห้องว่าง
5. **Booking History**: ประวัติการจอง
6. **Admin Panel**: จัดการข้อมูลระบบ

### API Endpoints
```python
@app.route('/api/bookings', methods=['GET'])      # Get all bookings
@app.route('/api/bookings', methods=['POST'])     # Create booking
@app.route('/api/bookings/<id>', methods=['PUT']) # Update booking
@app.route('/api/bookings/<id>', methods=['DELETE']) # Delete booking
```

---

## 📚 ทรัพยากร

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Font Awesome Icons](https://fontawesome.com/)

---

## ✨ สรุป

เว็บแอปพลิเคชันนี้มีฟีเจอร์ครบครันสำหรับจัดการการจองห้องเรียน:

✅ **Dashboard** ที่แสดงสถิติและรายการจอง  
✅ **CRUD Operations** สำหรับจัดการการจอง  
✅ **Responsive Design** ใช้งานได้ทุกอุปกรณ์  
✅ **Modern UI** ด้วย Tailwind CSS และธีมสีสวยงาม  
✅ **Database Integration** เชื่อมต่อ SQLite อย่างปลอดภัย  
✅ **Error Handling** จัดการข้อผิดพลาดอย่างเหมาะสม  

**พร้อมใช้งานได้ทันที!** 🎉

---

*Created: May 3, 2026*
*Framework: Flask + Tailwind CSS*
*Database: SQLite*