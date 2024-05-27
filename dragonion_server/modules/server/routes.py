from fastapi import APIRouter, WebSocket

from .handlers.websocket_server import serve_websocket

router = APIRouter()


@router.websocket("/{room_name}")
async def root(websocket: WebSocket, room_name: str):
    await serve_websocket(websocket, room_name)
