from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from ..services.ai import call_openai, get_project_by_token
from ..schemas.ai import OpenAIRequest
from ..models.project import Project

import json

router = APIRouter(tags=["OpenAI API"])


async def verify_api_token(x_api_token: str = Header(...)) -> Project:
    return await get_project_by_token(x_api_token)


@router.post("/v1/chat/completions")
async def openai_http(
        request: OpenAIRequest,
        project: Project = Depends(verify_api_token)
):
    try:
        response = await call_openai(
            text=request.text,
            max_tokens=request.max_tokens
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v1/chat/completions/stream")
async def openai_stream(
        request: OpenAIRequest,
        project: Project = Depends(verify_api_token)
):
    async def generate():
        try:
            async with call_openai(
                    text=request.text,
                    max_tokens=request.max_tokens,
                    stream=True
            ) as response:
                async for chunk in response.aiter_lines():
                    if chunk.startswith("data: "):
                        data = chunk[6:].strip()
                        if data == "[DONE]":
                            break
                        yield f"data: {data}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )