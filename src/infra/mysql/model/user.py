from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from src.infra.mysql.db import Base


class UserDTO(Base):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("email"),)

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    auth0_id: Mapped[str] = mapped_column(VARCHAR(length=255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(length=255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(length=255), nullable=False)
