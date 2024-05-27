from datetime import datetime

from dragonion_core.proto.web.webmessage import WebMessage, webmessages_union
from fastapi import WebSocket, WebSocketDisconnect

from .managers.exceptions import GotInvalidWebmessage
from .managers.service import Service

service = Service()


async def serve_websocket(websocket: WebSocket, room_name: str):
    """
    Serves websocket
    :param websocket: Ws to serve 
    :param room_name: Room name to connect ws to
    :return: 
    """
    print(f'[{datetime.now().time()}] Connection opened room {room_name}')
    room = await service.get_room(room_name)
    connection = await room.accept_connection(websocket)

    while True:
        try:
            data = await websocket.receive_text()

            try:
                webmessage: webmessages_union = WebMessage.from_json(data)
            except Exception as e:
                await connection.send_error("invalid_webmessage")
                continue

            try:
                match webmessage.type:
                    case "disconnect":
                        await room.disconnect(connection)
                    case "broadcastable":
                        await room.broadcast_message(webmessage)

            except GotInvalidWebmessage:
                await connection.send_error("invalid_webmessage")

        except RuntimeError:
            username = await room.disconnect(connection)
            if username is not None:
                await room.broadcast_user_disconnected(username)
            print(f'[{datetime.now().time()}] Closed {username}')
            break
        except WebSocketDisconnect:
            username = await room.disconnect(connection)
            if username is not None:
                await room.broadcast_user_disconnected(username)
            print(f'[{datetime.now().time()}] Closed {username}')
            break
        except Exception as e:
            print(f'[{datetime.now().time()}] Exception in '
                  f'{connection.username}: {e.__class__}: {e}')
            continue
