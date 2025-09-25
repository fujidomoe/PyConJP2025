from sqlalchemy.orm.session import Session

from src.domain.model.user import User
from src.domain.repository.user import IUserRepo


class UserRepo(IUserRepo):
    def __init__(self, session: Session):
        self.session = session

    def find_user_by_auth0_id(self, auth0_id: str) -> User | None:
        return User(user_id=1, auth0_id="abc12345", name="fujidomoe", email="fujidomoe@pyconjp.com")
