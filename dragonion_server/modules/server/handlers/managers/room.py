from attrs import define
from .connection import Connection
from typing import Dict
from fastapi import WebSocket

from dragonion_core.proto.web import (
    webmessages_union,
    WebMessageMessage,
    WebNotificationMessage,
    webmessage_error_message_literal,
    WebErrorMessage, 
    WebUserMessage
)


@define
class Room(object):
    connections: Dict[str, Connection] = {}

    async def accept_connection(self, ws: WebSocket) -> Connection:
        """
        Accepts connection, checks username availability and adds it to dict of 
        connections 
        :param ws: Websocket of connection 
        :return: 
        """
        print('Incoming connection')
        await ws.accept()
        connection = Connection(
            username=(username := await ws.receive_text()),
            ws=ws,
            public_key=''
        )
        if username in self.connections.keys():
            await connection.send_error(
                'username_exists'
            )

        self.connections[username] = connection
        await connection.send_connect()
        print(f'Accepted {username}')
        return connection

    async def broadcast_webmessage(self, obj: webmessages_union):
        """
        Broadcasts WebMessages to all connections in room
        :param obj:  
        :return: 
        """
        for connection in self.connections.values():
            print(f'Sending to {connection.username}: {obj}')
            await connection.send_webmessage(obj)

    async def broadcast_message(self, from_username: str, message: str):
        """
        Broadcasts message to every user in room
        :param from_username: User that sent message
        :param message: content
        :return: 
        """
        await self.broadcast_webmessage(
            WebMessageMessage(
                username=from_username,
                message=message
            )
        )

    async def broadcast_notification(self, message: str):
        """
        Broadcasts notification from server
        :param message: Content
        :return: 
        """
        await self.broadcast_webmessage(
            WebNotificationMessage(
                message=message
            )
        )

    async def broadcast_error(
            self,
            error_message: webmessage_error_message_literal
    ):
        """
        Broadcasts server error
        :param error_message: See webmessage_error_message_literal
        :return: 
        """
        await self.broadcast_webmessage(
            WebErrorMessage(
                error_message=error_message
            )
        )

    async def broadcast_user_disconnected(self, username: str):
        """
        Broadcasts that user is disconnected
        :param username: Username of user that disconnected
        :return: 
        """
        await self.broadcast_webmessage(
            WebUserMessage(
                type="disconnect",
                username=username
            )
        )

    async def get_connection_by(self, attribute: str, value: str) -> Connection | None:
        """
        Search for connection by attribute and value in it
        :param attribute: 
        :param value: 
        :return: 
        """
        for connection in self.connections.values():
            if getattr(connection, attribute) == value:
                return connection

    async def disconnect(self, connection: Connection, close_reason: str | None = None):
        """
        Disconnects by connection object. 
        :param connection: Object of connection. 
                           It can be obtained using get_connection_by
        :param close_reason: Reason if exists
        :return: 
        """
        if connection not in self.connections.values():
            return

        del self.connections[connection.username]

        try:
            await connection.ws.close(
                reason=close_reason
            )
        except Exception as e:
            print(f'Cannot close {connection.username} ws, '
                  f'maybe it\'s already closed: {e}')

        return connection.username
