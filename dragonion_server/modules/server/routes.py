from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse


router = APIRouter()


@router.get("/", response_model=str)
async def root(request: Request):
    return PlainTextResponse("dragonion-server")
