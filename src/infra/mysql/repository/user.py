from src.domain.repository.user import IUserRepo
from src.domain.model.user import User
from sqlalchemy.orm.session import Session


class UserRepo(IUserRepo):
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int) -> User | None:
        return User(
            user_id=1,
            name="John Doe",
            email="john@sample.com"
        )
