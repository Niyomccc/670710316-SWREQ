from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    MetaData,
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Slot(Base):
    """รองรับ: FR-BKG-01, FR-BKG-06, CON-TECH-01"""
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True)
    slot_date = Column(Date, nullable=False)
    start_time = Column(String(16), nullable=False)
    package_code = Column(String(32), nullable=False)
    capacity = Column(Integer, nullable=False, default=0)
    remaining = Column(Integer, nullable=False, default=0)


class Booking(Base):
    """รองรับ: FR-BKG-02, FR-BKG-04, IF-HIS-01, CON-TECH-01"""
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    hn = Column(String(64), nullable=False)
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    queue_no = Column(String(32), nullable=True)  # รอ Q-02: รูปแบบยังไม่ระบุ
    status = Column(String(32), nullable=False, default="created")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    slot = relationship("Slot")


class AuditLog(Base):
    """รองรับ: DOM-PDPA-01, CON-TECH-01"""
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor_id = Column(String(128), nullable=False)
    action = Column(String(256), nullable=False)
    hn = Column(String(64), nullable=True)
    accessed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
