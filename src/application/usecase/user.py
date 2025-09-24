from abc import ABC, abstractmethod

from injector import inject

from src.application.usecase.user_dto import UserMeOutPutDTO
from src.domain.model.user import User
from src.domain.repository.user import IUserRepo


class IUserMeUseCase(ABC):
    @abstractmethod
    def handle(self, user: User) -> UserMeOutPutDTO | None:
        pass


class UserMeInteractor(IUserMeUseCase):
    @inject
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo

    def handle(self, user: User) -> UserMeOutPutDTO | None:
        u: User | None = self.user_repo.find_user_by_auth0_id(user.auth0_id)
        if u is None:
            return None
        return UserMeOutPutDTO.from_entity(u)
