from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from typing import Generator
import importlib

import importlib.util
import os
import sys

# รองรับ: CON-TECH-01 (ใช้ DATABASE_URL เพื่อเชื่อมต่อฐานข้อมูลตามข้อกำหนด)
def _load_config():
	base_dir = os.path.dirname(__file__)
	config_path = os.path.normpath(os.path.join(base_dir, "..", "config.py"))
	spec = importlib.util.spec_from_file_location("app_config", config_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[spec.name] = module
	spec.loader.exec_module(module)
	return module


config = _load_config()
DATABASE_URL = config.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@contextmanager
def get_session() -> Generator:
	"""รองรับ: CON-TECH-01 - ให้ context manager สำหรับ SQLAlchemy session"""
	session = SessionLocal()
	try:
		yield session
	finally:
		session.close()
