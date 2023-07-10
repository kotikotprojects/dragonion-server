from stem.control import Controller
from .stem_process import launch_tor_with_config
from stem import ProtocolError

import socket
import random
import os
import psutil
import subprocess
import tempfile
import platform
import time
import base64
import nacl.public

from rich import print

from dragonion_server.utils.core import dirs
from dragonion_server.utils import config
from dragonion_server.utils.config.db import services


def get_available_port(min_port: int = 1000, max_port: int = 65535):
    with socket.socket() as tmpsock:
        while True:
            try:
                tmpsock.bind(("127.0.0.1", random.randint(min_port, max_port)))
                break
            except OSError:
                pass
        _, port = tmpsock.getsockname()
    return port


def key_str(key):
    key_bytes = bytes(key)
    key_b32 = base64.b32encode(key_bytes)
    assert key_b32[-4:] == b"===="
    key_b32 = key_b32[:-4]
    s = key_b32.decode("utf-8")
    return s


class Onion(object):
    tor_data_directory_name: str
    tor_control_socket: str | None
    tor_control_port: int | None
    tor_torrc: str
    tor_socks_port: int
    tor_cookie_auth_file: str
    tor_data_directory: tempfile.TemporaryDirectory
    tor_path: str = dirs.get_tor_paths()
    tor_proc: subprocess.Popen | None
    c: Controller
    connected_to_tor: bool = False
    auth_string: str
    graceful_close_onions: list = list()

    def kill_same_tor(self):
        for proc in psutil.process_iter(["pid", "name", "username"]):
            try:
                cmdline = proc.cmdline()
                if (
                        cmdline[0] == self.tor_path
                        and cmdline[1] == "-f"
                        and cmdline[2] == self.tor_torrc
                ):
                    proc.terminate()
                    proc.wait()
                    break
            except Exception as e:
                assert e

    def get_config(self, tor_data_directory_name) -> dict:
        self.tor_cookie_auth_file = os.path.join(tor_data_directory_name, "cookie")
        try:
            self.tor_socks_port = get_available_port(1000, 65535)
        except Exception as e:
            print(f"Cannot bind any port for socks proxy: {e}")
        self.tor_torrc = os.path.join(tor_data_directory_name, "torrc")

        self.kill_same_tor()

        tor_config = {
            'DataDirectory': tor_data_directory_name,
            'SocksPort': str(self.tor_socks_port),
            'CookieAuthentication': '1',
            'CookieAuthFile': self.tor_cookie_auth_file,
            'AvoidDiskWrites': '1',
            'Log': [
                'NOTICE stdout'
            ]
        }

        if platform.system() in ["Windows", "Darwin"]:
            try:
                self.tor_control_port = get_available_port(1000, 65535)
                tor_config = tor_config | {"ControlPort": str(self.tor_control_port)}
            except Exception as e:
                print(f"Cannot bind any control port: {e}")
            self.tor_control_socket = None
        else:
            self.tor_control_port = None
            self.tor_control_socket = os.path.abspath(os.path.join(
                tor_data_directory_name, "control_socket"
            ))
            tor_config = tor_config | {"ControlSocket": str(self.tor_control_socket)}

        return tor_config
    
    def connect(self):
        self.tor_data_directory = tempfile.TemporaryDirectory(
            dir=dirs.build_tmp_dir()
        )
        self.tor_data_directory_name = self.tor_data_directory.name

        self.tor_proc = launch_tor_with_config(
            config=self.get_config(self.tor_data_directory_name),
            tor_cmd=self.tor_path,
            take_ownership=True,
            init_msg_handler=print
        )

        time.sleep(2)

        if platform.system() in ["Windows", "Darwin"]:
            self.c = Controller.from_port(port=self.tor_control_port)
            self.c.authenticate()
        else:
            self.c = Controller.from_socket_file(path=self.tor_control_socket)
            self.c.authenticate()

        self.connected_to_tor = True

    @staticmethod
    def write_onion_service(name: str, port: int):
        if name in services.keys():
            service: config.models.ServiceModel = services[name]
            service.port = port
            services[name] = service
            return services[name]

        client_auth_priv_key_raw = nacl.public.PrivateKey.generate()
        client_auth_priv_key = key_str(client_auth_priv_key_raw)
        client_auth_pub_key = key_str(
            client_auth_priv_key_raw.public_key
        )

        services[name] = config.models.ServiceModel(
            port=port,
            client_auth_priv_key=client_auth_priv_key,
            client_auth_pub_key=client_auth_pub_key
        )
        return services[name]

    def start_onion_service(self, name: str) -> str:
        """
        Starts onion service
        :param name: Name of created service (must exist in data.storage)
        :return: .onion url
        """
        if name not in services.keys():
            raise 'Service not created'

        service: config.models.ServiceModel = services[name]

        try:
            res = self.c.create_ephemeral_hidden_service(
                {80: service.port},
                await_publication=True,
                key_type=service.key_type,
                key_content=service.key_content,
                client_auth_v3=service.client_auth_pub_key,
            )

        except ProtocolError as e:
            print("Tor error: {}".format(e.args[0]))
            raise

        onion_id = res.service_id

        self.graceful_close_onions.append(res.service_id)

        if service.key_type == "NEW":
            service.service_id = res.service_id
            service.key_type = "ED25519-V3"
            service.key_content = res.private_key

        self.auth_string = f'{res.service_id}:descriptor:' \
                           f'x25519:{service.client_auth_priv_key}'

        services[name] = service

        return onion_id

    def stop_onion_service(self, name):
        service: config.models.ServiceModel = services[name]
        if service.service_id:
            try:
                self.c.remove_ephemeral_hidden_service(
                    service.service_id
                )
            except Exception as e:
                print(e)

    def is_authenticated(self):
        if self.c is not None:
            return self.c.is_authenticated()
        else:
            return False

    def cleanup(self):
        if self.tor_proc:
            try:
                rendezvous_circuit_ids = []
                for c in self.c.get_circuits():
                    if (
                            c.purpose == "HS_SERVICE_REND"
                            and c.rend_query in self.graceful_close_onions
                    ):
                        rendezvous_circuit_ids.append(c.id)

                symbols = list("\\|/-")
                symbols_i = 0

                while True:
                    num_rend_circuits = 0
                    for c in self.c.get_circuits():
                        if c.id in rendezvous_circuit_ids:
                            num_rend_circuits += 1

                    if num_rend_circuits == 0:
                        print(
                            "\rTor rendezvous circuits have closed" + " " * 20
                        )
                        break

                    if num_rend_circuits == 1:
                        circuits = "circuit"
                    else:
                        circuits = "circuits"
                    print(
                        f"\rWaiting for {num_rend_circuits} Tor rendezvous "
                        f"{circuits} to close {symbols[symbols_i]} ",
                        end="",
                    )
                    symbols_i = (symbols_i + 1) % len(symbols)
                    time.sleep(1)
            except Exception as e:
                print(e)

            self.tor_proc.terminate()
            time.sleep(0.2)
            if self.tor_proc.poll() is None:
                try:
                    self.tor_proc.kill()
                    time.sleep(0.2)
                except Exception as e:
                    print(e)
            self.tor_proc = None

        self.connected_to_tor = False

        try:
            self.tor_data_directory.cleanup()
        except Exception as e:
            print(f'Cannot cleanup temporary directory: {e}')

    @property
    def get_tor_socks_port(self):
        assert isinstance(self.tor_socks_port, int)
        return "127.0.0.1", self.tor_socks_port
