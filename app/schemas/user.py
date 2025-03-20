from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum


# 新增用户角色枚举
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserCreate(BaseModel):
    username: str = Field(...,
                          min_length=3,
                          max_length=50,)
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="必须包含大小写字母和数字"
    )

    @field_validator('password')
    def validate_password(cls, v):
        if not any(c.islower() for c in v):
            raise ValueError('必须包含至少一个小写字母')
        if not any(c.isupper() for c in v):
            raise ValueError('必须包含至少一个大写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('必须包含至少一个数字')
        return v


class UserLogin(BaseModel):
    username: str = Field(..., description="admin")
    password: str = Field(..., description="admin")


# 新增管理员申请模型
class AdminApplicationCreate(BaseModel):
    reason: str = Field(..., max_length=500)


class UserInDB(BaseModel):
    id: int
    username: str
    role: UserRole = Field(default=UserRole.USER)  # 替换is_admin为role
    created_at: datetime

    class Config:
        from_attributes = True


# 新增带token响应的模型
class UserLoginResponse(UserInDB):
    access_token: str
    token_type: str = "bearer"
