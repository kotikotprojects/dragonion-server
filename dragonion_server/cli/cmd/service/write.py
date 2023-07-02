import click

from dragonion_server.utils.onion import Onion
from dragonion_server.common import console


class ServiceWriteCommand(click.Command):
    def __init__(self):
        super().__init__(
            name='write',
            callback=self.callback,
            params=[
                click.Option(
                    ('--name', '-n'),
                    required=True,
                    prompt=True,
                    type=str,
                    help='Name of service to write to'
                ),
                click.Option(
                    ('--port', '-p'),
                    required=True,
                    prompt=True,
                    type=int,
                    help='Port to start service on'
                )
            ]
        )

    @staticmethod
    def callback(name: str, port: int):
        try:
            Onion.write_onion_service(name, port)
            print(f'Written service "{name}" info')
        except Exception as e:
            assert e
            console.print_exception(show_locals=True)
