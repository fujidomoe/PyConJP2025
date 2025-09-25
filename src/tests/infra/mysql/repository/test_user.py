import pytest

from src.domain.model.user import User
from src.infra.mysql.repository.user import UserRepo
from src.tests.conftest import fixture_user, session


class TestUserRepository:
    @pytest.fixture()
    def setup(self):
        fixture_user(id=1, auth0_id="abc12345", name="fujidomoe", email="fujidomoe@pyconjp.com")

    @pytest.mark.usefixtures("setup")
    def test_get_user_by_id_exist(self):
        act = UserRepo(session).find_user_by_auth0_id("abc12345")
        want = User(
            user_id=1,
            auth0_id="abc12345",
            name="fujidomoe",
            email="fujidomoe@pyconjp.com",
        )
        assert act == want

    @pytest.mark.usefixtures("setup")
    def test_get_user_by_id_not_exist(self):
        act = UserRepo(session).find_user_by_auth0_id("not_exist")
        assert act is None
