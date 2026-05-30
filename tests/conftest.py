import pytest
from fastapi.testclient import TestClient

from taskflow import db
from taskflow.main import app


@pytest.fixture(autouse=True)
def reset_db():
    db.seed()
    yield
    db.seed()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_risheel():
    return {"Authorization": "Bearer tok-risheel"}


@pytest.fixture
def auth_vaibhav():
    return {"Authorization": "Bearer tok-vaibhav"}


@pytest.fixture
def auth_manthan():
    return {"Authorization": "Bearer tok-manthan"}


@pytest.fixture
def auth_priya():
    return {"Authorization": "Bearer tok-priya"}
