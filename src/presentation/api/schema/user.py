from pydantic import BaseModel


class UserMeResponse(BaseModel):
    user_id: int
    auth0_id: str
    name: str
    email: str

    @classmethod
    def from_dto(cls, dto) -> "UserMeResponse":
        return cls(
            user_id=dto.user_id,
            auth0_id=dto.auth0_id,
            name=dto.name,
            email=dto.email,
        )
