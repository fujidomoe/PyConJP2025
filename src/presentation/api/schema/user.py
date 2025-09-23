from pydantic import BaseModel


class UserMeResponse(BaseModel):
    user_id: int
    name: str
    email: str

    @classmethod
    def from_dto(cls, dto) -> "UserMeResponse":
        return cls(
            user_id=dto.user_id,
            name=dto.name,
            email=dto.email,
        )
