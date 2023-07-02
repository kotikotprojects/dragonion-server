import click

from dragonion_server.modules.server import run
from dragonion_server.common import console


class ServiceRunCommand(click.Command):
    def __init__(self):
        super().__init__(
            name='run',
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
                    required=False,
                    prompt=True,
                    prompt_required=False,
                    type=int,
                    help='Port to start service on'
                )
            ]
        )

    @staticmethod
    def callback(name: str, port: int | None):
        try:
            run(name, port)
        except Exception as e:
            assert e
            console.print_exception(show_locals=True)
