from ...utils import ModuleGroup
from .write import ServiceWriteCommand
from .run import ServiceRunCommand
from .remove import ServiceRemoveCommand


service_group = ModuleGroup(
    name='service',
    commands={
        'write': ServiceWriteCommand(),
        'run': ServiceRunCommand(),
        'remove': ServiceRemoveCommand()
    }
)
