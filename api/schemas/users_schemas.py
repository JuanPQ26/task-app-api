from pydantic import BaseModel
# schemas
from api.schemas.tasks_schemas import Task


class UserBase(BaseModel):
    fullname: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    tasks: list[Task] = []

    class Config:
        orm_mode = True

