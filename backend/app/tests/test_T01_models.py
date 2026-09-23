import importlib.util
import sys
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import os


def load_module_from_path(path, name):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[name] = module
	spec.loader.exec_module(module)
	return module


def test_migrations_create_tables():
	# Arrange: load migration and models modules by file path
	base_dir = os.path.dirname(__file__)
	migrations_path = os.path.normpath(os.path.join(base_dir, "..", "db", "migrations", "001_init.py"))
	models_path = os.path.normpath(os.path.join(base_dir, "..", "db", "models.py"))
	migrations = load_module_from_path(migrations_path, "migrations_001_init")
	models = load_module_from_path(models_path, "db_models")

	# Act: use a file-based sqlite DB so migration and test share the same DB
	db_file = os.path.join(base_dir, "test_db.sqlite3")
	engine_url = f"sqlite:///{db_file}"
	# ensure migration creates tables in that file
	migrations.upgrade(engine_url)

	engine = create_engine(engine_url)
	Session = sessionmaker(bind=engine)
	session = Session()

	# Insert sample rows
	Slot = models.Slot
	Booking = models.Booking
	AuditLog = models.AuditLog

	slot = Slot(slot_date=date(2026, 9, 24), start_time="09:00", package_code="PKG1", capacity=10, remaining=10)
	session.add(slot)
	session.commit()

	booking = Booking(hn="HN123", slot_id=slot.id, status="created")
	session.add(booking)
	session.commit()

	audit = AuditLog(actor_id="user1", action="view_booking", hn="HN123")
	session.add(audit)
	session.commit()

	# Assert: rows exist
	assert session.query(Slot).count() == 1
	assert session.query(Booking).count() == 1
	assert session.query(AuditLog).count() == 1
