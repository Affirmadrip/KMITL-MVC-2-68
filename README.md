# Promise Tracker (MVC)

Web Application สำหรับติดตามคำสัญญาของนักการเมือง 
พัฒนาด้วย Flask (Python) ตามแนวคิด MVC (Model–View–Controller)

## โครงสร้างระบบแบบ MVC
- **Model**: `models.py`
- **View**: โฟลเดอร์ `templates/`
- **Controller**: โฟลเดอร์ `controllers/`
- **Database Script**: `seed.py`

การอธิบายรายละเอียดของแต่ละไฟล์ อยู่ใน Private Comment ของ Google Classroom

## วิธีการ Run โปรแกรม
**1. สร้างและเปิดใช้งาน Virtual Environment**
- python -m venv .venv
- .venv\Scripts\activate

**2. ติดตั้ง Library**
- pip install flask flask_sqlalchemy

**3. สร้างฐานข้อมูลและ Sample Data**
- python seed.py

**4. Run ระบบ**
- python app.py และเปิด http://127.0.0.1:5000