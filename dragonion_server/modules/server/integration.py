import sys

from dragonion_core.proto.file import AuthFile
from rich import print

from dragonion_server.utils.config.db import services
from dragonion_server.utils.onion import Onion


def integrate_onion(port: int, name: str) -> Onion:
    """
    Starts onion service, writes it to config
    :param port: Port, where local service is started
    :param name: Name of service to get or write to config
    :return: Onion object, that is connected and service is started
    """
    onion = Onion()

    try:
        onion.connect()
        onion.write_onion_service(name, port)
    finally:
        if not onion.connected_to_tor:
            onion.cleanup()
            sys.exit(1)

    print(
        f"[green]Available on[/] "
        f"{(onion_host := onion.start_onion_service(name))}.onion"
    )

    auth = AuthFile(name)
    auth["host"] = f"{onion_host}.onion"
    auth["auth"] = onion.auth_string
    print(f"To connect to server just share [green]{auth.filename}[/] file")
    print(
        f"Or use [#ff901b]service id[/] and [#564ec3]auth string[/]: \n"
        f"[#ff901b]{onion_host}[/] \n"
        f"[#564ec3]{services[name].client_auth_priv_key}[/]"
    )

    return onion
