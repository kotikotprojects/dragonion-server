import click

from .cmd.service.service import service_group

cli = click.CommandCollection(name="dragonion-server", sources=[service_group()])
