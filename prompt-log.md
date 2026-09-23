# Prompt Log

- created by AI session for tasks generation

- ใช้คำสั่ง: /tasks กับไฟล์ specs/001-booking/spec.md -> สร้าง specs/001-booking/tasks.md (รอบแรก)
- ใช้คำสั่ง: /implement T-01 -> สร้าง `backend/app/db/models.py`, `backend/app/db/migrations/001_init.py`, `backend/app/db/session.py`, และ `backend/app/tests/test_T01_models.py`; ผล: tests ผ่านในระดับ unit (pytest ของไฟล์นั้นผ่าน); สิ่งที่เกือบต้องเดา: ไม่มีการเดา ข้อ Q-02 ถูกระบุเป็น Open Question และยังไม่ได้ตัดสิน
 - ใช้คำสั่ง: /implement T-01 -> สร้าง `backend/app/db/models.py`, `backend/app/db/migrations/001_init.py`, `backend/app/db/session.py`, และ `backend/app/tests/test_T01_models.py`; ผล: tests ผ่านในระดับ unit (pytest ของไฟล์นั้นผ่าน); สิ่งที่เกือบต้องเดา: ไม่มีการเดา ข้อ Q-02 ถูกระบุเป็น Open Question และยังไม่ได้ตัดสิน

- ใช้คำสั่ง: /implement T-02 -> สร้าง `backend/app/config.py`, ปรับ `backend/app/db/session.py`, และเพิ่ม `backend/app/tests/test_T02_session.py`; ผล: tests ผ่าน; สิ่งที่เกือบต้องเดา: ไม่มี

- ใช้คำสั่ง: /tasks กับไฟล์ specs/001-booking/spec.md -> สร้าง specs/001-booking/tasks.md ตาม template ของ prompt ที่สอดคล้องกับ spec.md และ plan.md; ผล: มี 12 task, 1 task รอ Q-02 (T-05), และได้ตรวจความครบ AC + Constraint ครบทุกตัวตาม spec

- ใช้คำสั่ง: /implement T-01 กับไฟล์ specs/001-booking/tasks.md -> แก้ `backend/app/db/migrations/001_init.py` เพื่อ reset SQLite file ทดสอบก่อนสร้าง schema; ผล: pytest `app/tests/test_T01_models.py` ผ่าน; สิ่งที่เกือบต้องเดา: ฐานข้อมูล SQLite test file ถูกใช้งานซ้ำและมีข้อมูลเก่าจึงทำให้ count เพิ่มขึ้น จึงถามและแก้โดยล้างฐานข้อมูลทดสอบเฉพาะไฟล์ `test_db.sqlite3` ก่อนสร้างตาราง
