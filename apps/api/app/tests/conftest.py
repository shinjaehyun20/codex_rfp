import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# must set before app import
_db_fd, _db_path = tempfile.mkstemp(prefix="proposal_ops_test", suffix=".db")
os.close(_db_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"

from apps.api.app.db.base import Base
from apps.api.app.db.session import get_db
from apps.api.app.main import app, get_storage


class FakeStorage:
    def __init__(self):
        self.objects = {}

    def put_bytes(self, key: str, body: bytes, content_type: str = "application/octet-stream") -> str:
        self.objects[key] = body
        return f"s3://proposal-artifacts/{key}"


@pytest.fixture()
def client():
    engine = create_engine(os.environ["DATABASE_URL"], future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_storage] = lambda: FakeStorage()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}
