import asyncio
from fastapi import FastAPI

from .core.config import get_settings
from .services.logbook_stream import LogbookStreamer
from .api import websocket as ws_api
from .api import health as health_api

settings = get_settings()
app = FastAPI(title="Log Gateway", version="1.0.0")

# Routers HTTP/WS
app.include_router(health_api.router, prefix="")
app.include_router(ws_api.router, prefix="")

# Instancia global del streamer
logbook_streamer = LogbookStreamer()


@app.on_event("startup")
async def on_startup():
    print("[app] startup, iniciando LogbookStreamer...")
    asyncio.create_task(logbook_streamer.run_forever())

    # Aquí en el futuro:
    # if settings.OPCUA_ENABLED:
    #    asyncio.create_task(opcua_streamer.run_forever())


@app.on_event("shutdown")
async def on_shutdown():
    await logbook_streamer.close()
    print("[app] shutdown completo")
