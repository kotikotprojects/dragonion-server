import typing as t

import click


class ModuleGroup(click.Group):
    def __init__(
        self,
        name: t.Optional[str] = None,
        commands: t.Optional[
            t.Union[t.Dict[str, click.Command], t.Sequence[click.Command]]
        ] = None,
        **attrs: t.Any,
    ) -> None:
        new_commands = dict()
        for command_key in commands.keys():
            new_commands[f"{name}-{command_key}"] = commands[command_key]

        super().__init__(name, new_commands, **attrs)
