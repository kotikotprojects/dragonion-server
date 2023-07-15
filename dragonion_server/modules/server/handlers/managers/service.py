from .connection import Connection
from .room import Room
from typing import Dict

from ..objects.webmessage import (
    webmessage_error_message_literal
)


class Service(object):
    rooms: Dict[str, Room] = {}

    async def get_room(self, name: str) -> Room:
        if name in self.rooms.keys():
            return self.rooms[name]

        self.rooms[name] = Room()
        return self.rooms[name]

    async def broadcast_notification(self, message: str):
        for room in self.rooms.values():
            await room.broadcast_notification(message)

    async def broadcast_error(
            self,
            error_message: webmessage_error_message_literal
    ):
        for room in self.rooms.values():
            await room.broadcast_error(error_message)

    async def get_room_by_connection(self, connection: Connection) -> Room:
        """
        Searches for room by valid connection object in it
        :param connection: Connection in unknown room to search
        :return: 
        """
        for room in self.rooms.values():
            if connection in room.connections.values():
                return room

    async def get_connection_by_attribute(
            self, attribute: str, value: str
    ) -> Connection:
        """
        Gets connection in some room by attribute and value in it
        :param attribute: 
        :param value: 
        :return: 
        """
        for room in self.rooms.values():
            if connection := await room.get_connection_by(attribute, value):
                return connection

    async def close_room(self, room_name: str, reason: str = 'Unknown reason'):
        """
        Closes all connections in room
        :param room_name: Close name
        :param reason: Reason to close room, default is Unknown reason
        :return: 
        """
        room = self.rooms.get(room_name)
        if room is None:
            return

        for connection in room.connections.values():
            await room.disconnect(
                connection=connection,
                close_reason=f'Room is closed: {reason}'
            )
