import asyncio
from typing import AsyncIterator

from .models import Event

# Un bus simple basado en asyncio.Queue
_event_queue: "asyncio.Queue[Event]" = asyncio.Queue(maxsize=1000)


async def publish(event: Event) -> None:
    """Productores (logbook, OPC UA, etc.) mandan eventos aquí."""
    await _event_queue.put(event)


async def events_stream() -> AsyncIterator[Event]:
    """Consumidor para el WebSocket; lee del bus indefinidamente."""
    while True:
        ev = await _event_queue.get()
        yield ev
