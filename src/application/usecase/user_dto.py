from pydantic import BaseModel

from src.domain.model.user import User


class UserMeOutPutDTO(BaseModel):
    user_id: int
    auth0_id: str
    name: str
    email: str

    @classmethod
    def from_entity(cls, user: User) -> "UserMeOutPutDTO":
        return cls(
            user_id=user.user_id,
            auth0_id=user.auth0_id,
            name=user.name,
            email=user.email,
        )
