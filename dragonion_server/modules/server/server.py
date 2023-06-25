from fastapi import FastAPI
import uvicorn
from dragonion_server.utils.onion import get_available_port
from .integration import integrate_onion
from .routes import router


def get_app(port: int, name: str) -> FastAPI:
    onion = integrate_onion(port, name)
    return FastAPI(
        title=f'dragonion-server: {name}',
        description=f'Secure dragonion chat endpoint server - service {name}',
        on_shutdown=[onion.cleanup]
    )


def run(name: str, port: int = get_available_port()):
    app = get_app(port, name)
    app.include_router(router)
    uvicorn.run(app, host='0.0.0.0', port=port)
