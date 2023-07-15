from fastapi import FastAPI
import uvicorn
from dragonion_server.utils.onion import get_available_port
from .integration import integrate_onion
from .routes import router


def get_app(port: int, name: str) -> FastAPI:
    """
    Creates FastAPI object and runs integrate_onion
    :param port: Must be same with port on which uvicorn is running 
    :param name: Name of service
    :return: FastAPI object with onion.cleanup function on shutdown
    """
    onion = integrate_onion(port, name)
    return FastAPI(
        title=f'dragonion-server: {name}',
        description=f'Secure dragonion chat endpoint server - service {name}',
        on_shutdown=[onion.cleanup]
    )


def run(name: str, port: int | None = get_available_port()):
    """
    Runs service with specified name and starts onion
    :param name: Name of service
    :param port: Port where to start service, if not specified - gets random available
    :return: 
    """
    if port is None:
        port = get_available_port()
    app = get_app(port, name)
    app.include_router(router)
    uvicorn.run(app, host='0.0.0.0', port=port)
