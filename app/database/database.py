from tortoise import Tortoise

from app.models.user import User
from app.schemas.user import UserRole


async def init_db(settings):
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["models.user", "models.project"]}
    )
    await Tortoise.generate_schemas()


async def init_default_admin():
    # 检查默认管理员是否存在
    admin = await User.filter(username="admin").first()
    if not admin:
        try:
            # 使用模型类方法创建用户
            admin_user = await User.create_user(
                username="admin",
                password="admin",  # 初始密码
                role=UserRole.ADMIN
            )
            await admin_user.save()
            print("Created default admin user")
        except Exception as e:
            print(f"Error creating admin user: {str(e)}")