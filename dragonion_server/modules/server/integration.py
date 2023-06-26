from dragonion_server.utils.onion import Onion
from dragonion_server.utils.generated_auth.db import AuthFile
from dragonion_server.utils.config.db import services


def integrate_onion(port: int, name: str) -> Onion:
    onion = Onion()
    onion.connect()
    onion.write_onion_service(name, port)
    print(f'Available on {(onion_host := onion.start_onion_service(name))}')
    auth = AuthFile(name)
    auth['host'] = onion_host
    auth['auth'] = onion.auth_string
    print(f'To connect to server share .onion host and auth string (next line), '
          f'also you can just share {auth.filename} file')
    print(onion.auth_string)
    print(f'Raw url auth string: {services[name].client_auth_priv_key}')
    return onion
