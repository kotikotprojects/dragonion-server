import sys

import click

from dragonion_server.common import console
from dragonion_server.modules.server import integrate_onion, run, run_without_onion


class ServiceRunCommand(click.Command):
    def __init__(self):
        super().__init__(
            name="run",
            callback=self.callback,
            params=[
                click.Option(
                    ("--name", "-n"),
                    required=True,
                    prompt=True,
                    type=str,
                    help="Name of service to write to",
                ),
                click.Option(
                    ("--port", "-p"),
                    required=False,
                    prompt=True,
                    prompt_required=False,
                    type=int,
                    help="Port to start service on",
                ),
                click.Option(
                    ("--without-tor", "-wt"),
                    is_flag=True,
                    help="Run service without tor",
                ),
                click.Option(
                    ("--only-tor", "-ot"),
                    is_flag=True,
                    help="Run only tor proxy to service",
                ),
            ],
        )

    @staticmethod
    def callback(name: str, port: int | None, without_tor: bool, only_tor: bool):
        try:
            if without_tor and only_tor:
                print("Cannot run only tor without tor, exiting")
                sys.exit(1)
            elif without_tor:
                run_without_onion(name, port)
            elif only_tor:
                if port is None:
                    print(
                        "For this mode, you need to specify port, "
                        "to which requests will be redirected. Cannot start "
                        "tor service, exiting"
                    )
                    sys.exit(1)
                onion = integrate_onion(port, name)
                input("Press Enter to stop onion and service...")
                onion.cleanup()
            else:
                run(name, port)
        except Exception as e:
            assert e
            console.print_exception(show_locals=True)
