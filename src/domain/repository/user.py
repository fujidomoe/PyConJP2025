from abc import ABC, abstractmethod

from src.domain.model.user import User


class IUserRepo(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User | None:
        pass

    # @abstractmethod
    # def create_user(self, user_data: dict) -> int:
    #     pass
    #
    # @abstractmethod
    # def update_user(self, user_id: int, user_data: dict) -> bool:
    #     pass
    #
    # @abstractmethod
    # def delete_user(self, user_id: int) -> bool:
    #     pass
