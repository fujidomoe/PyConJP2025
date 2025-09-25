from abc import ABC, abstractmethod

from src.domain.model.user import User


class IUserRepo(ABC):
    @abstractmethod
    def find_user_by_auth0_id(self, auth0_id: str) -> User | None:
        pass
