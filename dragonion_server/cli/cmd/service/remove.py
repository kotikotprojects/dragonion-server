import os

import click

from dragonion_server.utils.config import db
from dragonion_server.common import console


class ServiceRemoveCommand(click.Command):
    def __init__(self):
        super().__init__(
            name='remove',
            callback=self.callback,
            params=[
                click.Option(
                    ('--name', '-n'),
                    required=True,
                    prompt=True,
                    type=str,
                    help='Name of service to write to'
                )
            ]
        )

    @staticmethod
    def callback(name: str):
        try:
            del db.services[name]
            if os.path.isfile(f'{name}.auth'):
                os.remove(f'{name}.auth')
                
            print(f'Removed service {name}')
        except KeyError:
            print(f'Service "{name}" does not exist in this storage')
        except Exception as e:
            assert e
            console.print_exception(show_locals=True)
