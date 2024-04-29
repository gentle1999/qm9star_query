from datetime import datetime
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = False
    is_superuser: bool = False
    nick_name: str = Field(
        regex="^[a-zA-Z0-9_]*$",
        description="only letters, numbers, underscores allowed",
        unique=True,
        index=True,
    )
    registration_time: datetime | None = Field(default_factory=datetime.now)
    last_login: datetime | None = Field(default_factory=datetime.now)
    snapshot_number: int = 0