Feature: จองคิวตรวจสุขภาพ (Booking)
Spec ID: SPEC-BKG-001
อ้างอิง: plan.md
วันที่: 2569-09-23

สรุป: มี 12 งานย่อย, 1 งานรอ Open Questions

### T-01 สร้าง migration และโครงสร้างตารางข้อมูล
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-xx
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง `slots`, `bookings`, `audit_logs` และ schema ทำงานใน test DB ได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 ตั้งค่า session และ config ของฐานข้อมูล
- รองรับ: CON-TECH-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/app/config.py, backend/app/db/session.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: pytest ใช้ SQLite in-memory ผ่าน `DATABASE_URL` แบบทดสอบได้โดยไม่ต้องมี PostgreSQL จริง
- สถานะ: พร้อมทำ

### T-03 ตรวจยืนยันตัวตนและค้น HN จาก HIS
- รองรับ: IF-IDP-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-xx
- ไฟล์ที่แตะ: backend/app/auth/idp.py, backend/app/his/client.py, backend/app/patients/router.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ระบบตรวจผลยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการ และ endpoint สำหรับค้น HN จากเลขบัตรทำงานโดยไม่เก็บเลขบัตรใน DB
- สถานะ: พร้อมทำ

### T-04 GET /slots: คำนวณช่วงว่างภายใน 30 วัน
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/slots/router.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: GET /slots คืนรายการช่วงเวลาและ `remaining` สำหรับ 30 วัน และ test performance ย่อส่วนผ่าน
- สถานะ: พร้อมทำ

### T-05 บันทึกการจองพื้นฐานและส่งคืนหมายเลขคิวชั่วคราว
- รองรับ: FR-BKG-04, IF-HIS-01
- ตรวจด้วย: AC-BKG-01, AC-BKG-04
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py
- ต้องทำหลัง: T-01, T-02, T-04
- เสร็จเมื่อ: POST /bookings บันทึกการจอง ตัดจำนวนที่นั่ง และส่งหมายเลขคิวกลับทันที โดยยังรอคำตอบ Q-02 ว่ารูปแบบและการรีเซ็ตคิวต้องเป็นแบบใด
- สถานะ: รอ Q-02

### T-06 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: เมื่อมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ระบบปฏิเสธการจองใหม่และแสดงหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-07 เสนอช่วงใกล้เคียงเมื่อช่วงเวลาถูกจองเต็ม
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py
- ต้องทำหลัง: T-05, T-06
- เสร็จเมื่อ: POST /bookings คืน 409 พร้อม 3 ช่วงที่ใกล้ที่สุดในวันเดียวกันและวันถัดไป และไม่สร้างการจองซ้อน
- สถานะ: พร้อมทำ

### T-08 คิวส่งข้อความแบบ asynchronous และส่งซ้ำตามกติกา
- รองรับ: IF-NOT-01, FR-BKG-05, NFR-REL-02, ASM-03
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: POST /bookings วางงานส่งข้อความลงคิว และเมื่อจำลองการส่งไม่สำเร็จ มีรายการส่งซ้ำภายใน 5 นาที ตาม ASM-03
- สถานะ: พร้อมทำ

### T-09 บันทึก audit log ทุกครั้งที่เข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: ทุกการเข้าถึงข้อมูลการจองบันทึก actor_id, accessed_at, hn ลงใน `audit_logs`
- สถานะ: พร้อมทำ

### T-10 หน้าเลือกแพ็กเกจและช่วงเวลา (API จำลอง)
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-xx
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/api/client.js
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอโหลดแพ็กเกจและช่วงเวลาได้จาก API จำลอง พร้อมแสดง `remaining` ที่ตรงตามสัญญา
- สถานะ: พร้อมทำ

### T-11 หน้ายืนยันและแสดงผลการจอง (API จำลอง)
- รองรับ: FR-BKG-03, FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/pages/BookingResult.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: เมื่อ API จำลองตอบ 409 หน้าจอแสดงข้อความ "ช่วงเวลาเต็ม" พร้อม 3 ตัวเลือก และเมื่อยืนยันสำเร็จแสดงหมายเลขคิวตามข้อมูลที่คืนกลับ
- สถานะ: พร้อมทำ

### T-12 ต่อหน้าจอกับ API จริงและตรวจ end-to-end
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-03, AC-BKG-05
- ไฟล์ที่แตะ: frontend/src/api/client.js, frontend/src/App.jsx, backend/app/slots/router.py, backend/app/booking/router.py
- ต้องทำหลัง: T-04, T-07, T-10, T-11
- เสร็จเมื่อ: หน้าแอปเรียก API จริงได้และการจองทำงาน end-to-end ในสภาพแวดล้อม dev
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ - AC
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-05 |
| AC-BKG-02 | T-06 |
| AC-BKG-03 | T-07, T-11 |
| AC-BKG-04 | T-05, T-08 |
| AC-BKG-05 | T-04 |
| AC-BKG-06 | T-09 |

## ตารางตรวจความครบ - Constraints
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01, T-02 |
| DOM-PDPA-01 | T-01, T-09 |
| IF-IDP-01 | T-03 |
| IF-HIS-01 | T-03, T-05 |
| IF-NOT-01 | T-08 |

## สิ่งที่ยังไม่ทำ (Open Questions)
- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร -> T-05 รอ Q-02

