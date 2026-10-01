"""Cliente HTTP com sessão falsa no lugar do Postgres."""

import pytest
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app


class FakeResult:
    def __init__(self, rows):
        self._rows = rows

    def scalars(self):
        return self

    def all(self):
        return self._rows


class FakeSession:
    """Substitui AsyncSession só nas operações que as rotas usam."""

    def __init__(self):
        self.added = []
        self.deleted = []
        self.committed = 0
        self.store = {}
        self.query_rows = []

    def add(self, obj):
        self.added.append(obj)

    async def commit(self):
        self.committed += 1

    async def delete(self, obj):
        self.deleted.append(obj)

    async def get(self, model, obj_id):
        return self.store.get((model, str(obj_id)))

    async def execute(self, _statement):
        return FakeResult(self.query_rows)

    def remember(self, model, obj):
        self.store[(model, str(obj.id))] = obj


@pytest.fixture
def db():
    return FakeSession()


@pytest.fixture
def client(db):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
