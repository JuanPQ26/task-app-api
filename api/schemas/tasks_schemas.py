from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(min_length=1)
    body: str | None = Field(None)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str = Field(None)
    body: str = Field(None)


class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
