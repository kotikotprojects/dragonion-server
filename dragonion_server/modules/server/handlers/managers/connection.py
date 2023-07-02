from attrs import define
from fastapi import WebSocket
from ..objects.webmessage import (
    webmessages_union,
    webmessage_error_message_literal,
    WebErrorMessage,
    WebUserMessage
)


@define
class Connection(object):
    ws: WebSocket
    username: str
    public_key: str

    async def send_webmessage(self, obj: webmessages_union):
        await self.ws.send_text(obj.to_json())

    async def send_error(
            self,
            error_message: webmessage_error_message_literal
    ):
        await self.send_webmessage(
            WebErrorMessage(
                error_message=error_message
            )
        )

    async def send_connect(self):
        await self.send_webmessage(
            WebUserMessage(
                type="connect",
                username=self.username
            )
        )
