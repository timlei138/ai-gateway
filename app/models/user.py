from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext
from datetime import datetime
from ..schemas.user import UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=300)
    role = fields.CharEnumField(UserRole, default=UserRole.USER)
    force_password_change = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    projects = fields.ReverseRelation["Project"]

    @classmethod
    async def create_user(cls, username: str, password: str, role: UserRole = UserRole.USER):
        hashed_password = pwd_context.hash(password)
        # 默认管理员首次创建需要强制修改密码
        force_change = (username == "admin")
        return await cls.create(
            username=username,
            hashed_password=hashed_password,
            role=role,
            force_password_change=force_change
        )

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.hashed_password)

    class PydanticMeta:
        exclude = ["hashed_password"]
