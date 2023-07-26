from attrs import define
from .connection import Connection
from .exceptions import GotInvalidWebmessage
from typing import Dict
from fastapi import WebSocket

from json.decoder import JSONDecodeError

from dragonion_core.proto.web.webmessage import (
    webmessages_union,
    set_time,
    WebMessageMessage,
    WebBroadcastableMessage,
    WebNotificationMessage,
    webmessage_error_message_literal,
    WebErrorMessage,
    WebConnectionMessage,
    WebDisconnectMessage,
    WebConnectionResultMessage
)


@define
class Room(object):
    connections: Dict[str, Connection] = {}

    async def accept_connection(self, ws: WebSocket) -> Connection | None:
        """
        Accepts connection, checks username availability and adds it to dict of 
        connections 
        :param ws: Websocket of connection 
        :return: 
        """
        print('Incoming connection')
        await ws.accept()
        try:
            connection_message = WebConnectionMessage.from_json(
                await ws.receive_text()
            )
        except JSONDecodeError:
            await ws.send_text(set_time(WebErrorMessage(
                'invalid_webmessage'
            )).to_json())
            await ws.close(reason='invalid_webmessage')
            return 
        
        connection = Connection(
            username=connection_message.username,
            ws=ws,
            public_key=connection_message.public_key,
            password=connection_message.password
        )
        
        if connection_message.username in self.connections.keys():
            await connection.send_error(
                'username_exists'
            )
            await ws.close(reason='username_exists')
            return 

        self.connections[connection_message.username] = connection
        await connection.send_webmessage(WebConnectionResultMessage(
            connected_users=dict(
                map(
                    lambda i, j: (i, j),
                    [_username for _username in list(self.connections.keys())
                     if self.connections[_username].password ==
                     connection_message.password],
                    [_connection.public_key for _connection 
                     in self.connections.values() if _connection.password ==
                     connection_message.password]
                )
            )
        ))

        await self.broadcast_webmessage(connection_message)
        print(f'Accepted {connection_message.username}')
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

    async def broadcast_message(self, broadcastable: WebBroadcastableMessage):
        """
        Broadcasts message to every user in room
        :param broadcastable: String object with json representation of 
                                   WebBroadcastableMessage
        :return: 
        """
        try: 
            for to_username in broadcastable.messages.keys():
                try:
                    await self.connections[to_username].send_webmessage(
                        broadcastable.messages[to_username]
                    )
                except KeyError:
                    continue
        except JSONDecodeError:
            raise GotInvalidWebmessage

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
            WebDisconnectMessage(
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
