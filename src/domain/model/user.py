from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    auth0_id: str
    name: str
    email: str
