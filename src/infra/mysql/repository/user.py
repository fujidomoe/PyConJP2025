from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from src.domain.model.user import User
from src.domain.repository.user import IUserRepo
from src.infra.mysql.model.user import UserDTO


class UserRepo(IUserRepo):
    def __init__(self, session: Session):
        self.session = session

    def find_user_by_auth0_id(self, auth0_id: str) -> User | None:
        try:
            x = self.session.query(UserDTO).filter(UserDTO.auth0_id == auth0_id).one()
        except NoResultFound:
            return None
        return User(user_id=x.id, auth0_id=x.auth0_id, name=x.name, email=x.email)
