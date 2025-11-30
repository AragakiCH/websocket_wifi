import asyncio
from typing import Set, List, Dict

from ..core.config import get_settings
from ..core.models import Event, LogbookEntry
from ..core.event_bus import publish
from ..adapters.ctrlx_logbook import CtrlXLogbookClient

settings = get_settings()


class LogbookStreamer:
    def __init__(self) -> None:
        self.client = CtrlXLogbookClient()
        self._seen_cursors: Set[str] = set()
        self._last_snapshot: List[Dict] = []

    @property
    def last_snapshot(self) -> List[Dict]:
        return list(self._last_snapshot)

    async def run_forever(self) -> None:
        while True:
            try:
                entries = await self.client.fetch_entries()
                print(f"[logbook] {len(entries)} entries recibidos")

                if settings.ONLY_PLC_MESSAGES:
                    entries = [e for e in entries if e.get("entity") == "plc"]

                if not entries:
                    await asyncio.sleep(settings.POLL_PERIOD_SEC)
                    continue

                entries_sorted = sorted(entries, key=lambda e: e.get("timestamp", ""))
                self._last_snapshot = entries_sorted

                new_entries: List[LogbookEntry] = []
                for raw in entries_sorted:
                    cursor = raw.get("__CURSOR")
                    if not cursor or cursor in self._seen_cursors:
                        continue
                    self._seen_cursors.add(cursor)
                    new_entries.append(LogbookEntry.model_validate(raw))

                if new_entries:
                    print(f"[logbook] nuevos {len(new_entries)} logs → publish")
                    ev = Event(type="logbook", source="ctrlx_logbook", entries=new_entries)
                    await publish(ev)
                else:
                    print("[logbook] sin nuevos logs")

            except Exception as ex:
                print(f"[logbook] error: {ex}")

            await asyncio.sleep(settings.POLL_PERIOD_SEC)

    async def close(self) -> None:
        await self.client.close()
