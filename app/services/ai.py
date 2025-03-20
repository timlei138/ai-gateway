import httpx
from fastapi import HTTPException
from ..config import settings
from ..models.project import Project


async def get_project_by_token(api_token: str) -> Project:
    project = await Project.get_or_none(api_token=api_token)
    if not project:
        raise HTTPException(status_code=403, detail="Invalid API token")
    return project


async def call_openai(
        text: str,
        max_tokens: int,
        stream: bool = False
):
    headers = {
        "Authorization": f"Bearer {settings.Settings.OPENAI_API_KEY.get_secret_value()}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}],
            "max_tokens": max_tokens,
            "stream": stream
        }

        try:
            if stream:
                return client.stream(
                    "POST",
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
            else:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"OpenAI API error: {e.response.text}"
            )
