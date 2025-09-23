import pytest


@pytest.fixture(scope="session", autouse=True)
def scope_session():
    yield
