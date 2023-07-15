from fastapi import WebSocket, WebSocketDisconnect
from .managers.service import Service
from .objects.webmessage import (
    webmessages_union,
    WebMessage
)


service = Service()


async def serve_websocket(websocket: WebSocket, room_name: str):
    """
    Serves websocket
    :param websocket: Ws to serve 
    :param room_name: Room name to connect ws to
    :return: 
    """
    print(f'Connection opened room {room_name}')
    room = await service.get_room(room_name)
    connection = await room.accept_connection(websocket)

    while True:
        try:
            data = await websocket.receive_text()
            print(f"Received in {room_name}: ", data)

            try:
                webmessage: webmessages_union = \
                    WebMessage.from_json(data)
            except Exception as e:
                print(f"Cannot decode message, {e}")
                await connection.send_error("invalid_webmessage")
                continue

            await room.broadcast_webmessage(webmessage)

        except RuntimeError:
            username = await room.disconnect(connection)
            await room.broadcast_user_disconnected(username)
            print(f'Closed {username}')
            break
        except WebSocketDisconnect:
            username = await room.disconnect(connection)
            await room.broadcast_user_disconnected(username)
            print(f'Closed {username}')
            break
        except Exception as e:
            print(f'Exception in {connection.username}: {e.__class__}: {e}')
            continue
