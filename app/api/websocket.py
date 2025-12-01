import asyncio
import json
from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..core.event_bus import events_stream
from ..core.models import Event

router = APIRouter()


@router.websocket("/ws/events")
async def websocket_events(ws: WebSocket):
    await ws.accept()
    print("[ws] cliente conectado")

    # Tarea que escucha el bus y empuja al cliente
    async def sender():
        async for ev in events_stream():
            try:
                await ws.send_text(ev.model_dump_json(by_alias=True))
            except Exception:
                break

    sender_task: Optional[asyncio.Task] = asyncio.create_task(sender())

    try:
        # mantenemos la conexión viva
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        if sender_task and not sender_task.done():
            sender_task.cancel()
        print("[ws] cliente desconectado")
