import os

# รองรับ: CON-TECH-01
# อ่าน `DATABASE_URL` จาก environment หรือใช้ค่าเริ่มต้นสำหรับทดสอบ
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///:memory:")
