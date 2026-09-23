Feature: จองคิวตรวจสุขภาพ
Spec ID: SPEC-BKG-001
อ้างอิง: plan.md
วันที่: 2569-09-23

สรุป: มี 12 งานย่อย, 1 งานรอ Open Questions

-### T-01 สร้าง migration และตารางฐานข้อมูล
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-xx
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migrations สร้างตาราง `slots`, `bookings`, `audit_logs` สำเร็จและรันใน test DB
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 เตรียม session DB และ config
- รองรับ: CON-TECH-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/app/db/session.py, backend/app/config.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: tests รันโดยเชื่อมต่อ SQLite in-memory ผ่าน `DATABASE_URL` แบบทดสอบ
- สถานะ: พร้อมทำ

## T-02 Implementation Notes
- สถานะปัจจุบัน: เสร็จ รอทีมตรวจ
- ทดสอบ: `backend/app/tests/test_T02_session.py` ผ่าน

### T-03 GET /slots: คำนวณช่วงว่างภายใน 30 วัน
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05 (ทดสอบประสิทธิภาพย่อส่วน), ไม่มี AC ตรง ๆ สำหรับ functional response -> test_AC_BKG_05
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/slots/router.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: GET /slots คืนรายการช่วงเวลาและ `remaining` สำหรับ 30 วัน และ test performance ย่อส่วนผ่าน
- สถานะ: พร้อมทำ

### T-04 POST /bookings: บันทึกการจองพื้นฐานและตัดที่นั่ง
- รองรับ: FR-BKG-04
- ตรวจด้วย: AC-BKG-01 (test_AC_BKG_01)
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py
- ต้องทำหลัง: T-01, T-02, T-03
- เสร็จเมื่อ: POST /bookings สร้าง booking ใน DB และ `remaining` ลดลงตาม AC-BKG-01
- สถานะ: พร้อมทำ

### T-05 กันจองซ้ำวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02 (test_AC_BKG_02)
- ไฟล์ที่แตะ: backend/app/booking/service.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: ระบบปฏิเสธการจองใหม่เมื่อมี booking ยังไม่ใช้ในวันเดียวกัน และคืนหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-06 เสนอช่วงใกล้เคียงเมื่อเต็ม (409 + 3 ตัวเลือก)
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03 (test_AC_BKG_03)
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py
- ต้องทำหลัง: T-04, T-05
- เสร็จเมื่อ: POST /bookings คืน 409 พร้อมรายการ 3 ช่วงที่ใกล้ที่สุด (วันเดียวกัน + วันถัดไป)
- สถานะ: พร้อมทำ

### T-07 คิวส่งข้อความแบบ asynchronous และส่งซ้ำ
- รองรับ: IF-NOT-01, FR-BKG-05, NFR-REL-02, ASM-03
- ตรวจด้วย: AC-BKG-04 (test_AC_BKG_04)
- ไฟล์ที่แตะ: backend/app/notify/queue.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: POST /bookings วางงานส่งข้อความลงคิว และเมื่อจำลองการส่งไม่สำเร็จ มีงานส่งซ้ำตาม ASM-03 (5 นาที 3 ครั้ง)
- สถานะ: พร้อมทำ

### T-08 audit log middleware
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06 (test_AC_BKG_06)
- ไฟล์ที่แตะ: backend/app/audit/middleware.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: ทุกการเข้าถึงข้อมูลการจองบันทึก `actor_id`, `accessed_at`, `hn` ใน `audit_logs`
- สถานะ: พร้อมทำ

### T-09 HIS lookup client (GET /patients/lookup)
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ (เป็น integration) -> เพิ่ม test เบื้องต้นใน conftest
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/app/patients/router.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: endpoint คืน `hn` จากเลขบัตร โดยไม่เก็บเลขบัตรใน DB
- สถานะ: พร้อมทำ

### T-10 หน้าจอ SlotPicker (ใช้ API จำลอง)
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ -> หน้าจอจะมี test หน้าจอสำหรับ AC-BKG-05 (ถ้ามี)
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/__tests__/AC-BKG-05.test.jsx
- ต้องทำหลัง: ไม่มี (ใช้ API จำลองตาม plan ข้อ 4)
- เสร็จเมื่อ: หน้าจอโหลดช่วงเวลาและแสดง `remaining` ตาม API จำลอง
- สถานะ: พร้อมทำ

### T-11 หน้ายืนยัน (ConfirmBooking) แสดง 409 และ 3 ตัวเลือก
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03.test.jsx (หน้ายืนยัน)
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: เมื่อ API จำลองตอบ 409 หน้าจอแสดงข้อความ "ช่วงเวลาเต็ม" และปุ่ม 3 ตัวเลือก
- สถานะ: พร้อมทำ

### T-12 ต่อหน้าจอกับ API จริง (integration)
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-01, AC-BKG-03 (integration test), AC-BKG-05 (performance measure หยาบ)
- ไฟล์ที่แตะ: frontend/* และ backend/* ที่เกี่ยวข้อง
- ต้องทำหลัง: T-03, T-06, T-10, T-11
- เสร็จเมื่อ: หน้าจอเรียก API จริงและการจองทำงาน end-to-end ในสภาพแวดล้อม dev
- สถานะ: รอ Q-02

## ตารางตรวจความครบ - AC
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-04 |
| AC-BKG-02 | T-05 |
| AC-BKG-03 | T-06, T-11 |
| AC-BKG-04 | T-07, T-04 |
| AC-BKG-05 | T-03 |
| AC-BKG-06 | T-08 |

## ตารางตรวจความครบ - Constraints
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01, T-02 |
| DOM-PDPA-01 | T-08, T-01 |
| IF-IDP-01 | (auth/idp.py ต้องมี) -> ไม่ได้แตกเป็น task แยกตาม plan |
| IF-HIS-01 | T-09, T-01 |
| IF-NOT-01 | T-07 |

## สิ่งที่ยังไม่ทำ (Open Questions)
- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และรูปแบบ -> T-12 รอ Q-02
