from sqlalchemy import create_engine
import importlib.util
import os
import sys


def _load_base_from_models():
    # Load models.py relative to this migrations file to obtain Base
    base_dir = os.path.dirname(__file__)
    models_path = os.path.normpath(os.path.join(base_dir, "..", "models.py"))
    spec = importlib.util.spec_from_file_location("db_models", models_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return getattr(module, "Base")


def upgrade(engine_url: str = "sqlite:///:memory:"):
    """Create initial tables: slots, bookings, audit_logs
    รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
    """
    engine = create_engine(engine_url)
    Base = _load_base_from_models()
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    # quick manual run for developer
    upgrade()
