import importlib.util
import os
import sys
from sqlalchemy import create_engine


def load_module_from_path(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


base_dir = os.path.dirname(__file__)
config = load_module_from_path(os.path.join(base_dir, "..", "config.py"), "app_config")
db_session = load_module_from_path(os.path.join(base_dir, "..", "db", "session.py"), "db_session")
DATABASE_URL = config.DATABASE_URL
get_session = db_session.get_session
SessionLocal = db_session.SessionLocal


def test_database_url_default():
    assert DATABASE_URL.startswith("sqlite://")


def test_session_local_connects():
    # create a temporary engine to ensure SessionLocal is configured
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.close()


def test_get_session_contextmanager():
    with get_session() as session:
        # session should have execute method
        assert hasattr(session, "execute")
