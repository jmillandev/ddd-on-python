from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture

from db.session import SessionLocal
from main import app


@fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
