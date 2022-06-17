from pydantic import BaseModel, Field


class AuthBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=30)
    password: str = Field(..., min_length=8)


class SigninBase(AuthBase):
    pass


class SignupBase(AuthBase):
    fullname: str = Field(..., max_length=30)

    class Config:
        orm_mode = True
