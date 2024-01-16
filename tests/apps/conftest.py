from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from main import app


@pytest.fixture(scope="module")
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://testserver") as ac:    
        yield ac
