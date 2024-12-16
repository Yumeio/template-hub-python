from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    organizations: str

    class Config:
        orm_mode = True

class RepositoryBase(BaseModel):
    name: str
    description: str
    type: str
    org: Optional[str] = None
    private: Optional[bool] = False
    status_lfs: Optional[bool] = False

class RepositoryCreate(RepositoryBase):
    pass

class RepositoryResponse(RepositoryBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True 