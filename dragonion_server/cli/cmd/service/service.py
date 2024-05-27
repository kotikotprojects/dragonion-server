from ...utils import ModuleGroup
from .remove import ServiceRemoveCommand
from .run import ServiceRunCommand
from .write import ServiceWriteCommand

service_group = ModuleGroup(
    name="service",
    commands={
        "write": ServiceWriteCommand(),
        "run": ServiceRunCommand(),
        "remove": ServiceRemoveCommand(),
    },
)
