from datetime import datetime

from fastapi import APIRouter, HTTPException
from tortoise.transactions import atomic
from app.models.user import User
from app.models.admin import AdminApplication
from app.schemas.user import UserRole

router = APIRouter(tags=["Admin"])


@router.post("/applications/{application_id}/approve")
async def approve_application(
        application_id: int
):
    async with atomic():
        application = await AdminApplication.filter(id=application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        user = await User.filter(id=application.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 更新用户角色
        user.role = UserRole.ADMIN
        await user.save()

        # 更新申请状态
        application.status = "approved"
        application.reviewed_at = datetime.utcnow()
        await application.save()

    return {"message": "Application approved", "user_id": user.id}
