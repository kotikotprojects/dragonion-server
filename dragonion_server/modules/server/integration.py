from dragonion_server.utils.onion import Onion


def integrate_onion(port: int, name: str) -> Onion:
    onion = Onion()
    onion.connect()
    onion.write_onion_service(name, port)
    print(f'Available on {onion.start_onion_service(name)}')
    return onion
