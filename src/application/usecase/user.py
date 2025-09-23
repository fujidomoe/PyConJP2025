from abc import ABC, abstractmethod
from src.application.usecase.user_dto import UserMeOutPutDTO
from injector import inject
from  src.domain.repository.user import IUserRepo



class IUserMeUseCase(ABC):
    @abstractmethod
    def handle(self, user_id: int) -> UserMeOutPutDTO | None:
        pass


class UserMeInteractor(IUserMeUseCase):
    @inject
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo

    def handle(self, user_id: int) -> UserMeOutPutDTO | None:
        user = self.user_repo.get_user_by_id(user_id)
        if user is None:
            return None
        return UserMeOutPutDTO.from_entity(user)


