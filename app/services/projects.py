import secrets
from fastapi import HTTPException
from tortoise.exceptions import IntegrityError
from ..models.project import Project
from ..config.settings import settings


async def generate_secure_token():
    return secrets.token_urlsafe(settings.API_TOKEN_BYTES)


async def create_user_project(user, project_name: str):
    for _ in range(3):
        api_token = await generate_secure_token()
        try:
            return await Project.create(
                name=project_name,
                api_token=api_token,
                user=user
            )
        except IntegrityError:
            continue
    raise HTTPException(
        status_code=500,
        detail="Failed to generate unique API token"
    )
