from attrs import define
from fastapi import WebSocket
from dragonion_core.proto.web.webmessage import (
    set_time,
    webmessages_union,
    webmessage_error_message_literal,
    WebErrorMessage
)


@define
class Connection(object):
    ws: WebSocket
    username: str
    public_key: str
    password: str

    async def send_webmessage(self, obj: webmessages_union):
        """
        Sends WebMessage object to this connection
        :param obj: Should be some type of WebMessage
        :return: 
        """
        await self.ws.send_text(set_time(obj).to_json())

    async def send_error(
            self,
            error_message: webmessage_error_message_literal
    ):
        """
        Sends error with specified messages
        :param error_message: See webmessage_error_message_literal for available
        :return: 
        """
        await self.send_webmessage(
            WebErrorMessage(
                error_message=error_message
            )
        )
