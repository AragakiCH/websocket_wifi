from typing import Optional, List, Dict

import httpx

from ..core.config import get_settings

settings = get_settings()


class CtrlXLogbookClient:
    def __init__(self) -> None:
        self._http: Optional[httpx.AsyncClient] = None
        self._token: Optional[str] = None

    async def _ensure_http(self) -> None:
        if self._http is None:
            self._http = httpx.AsyncClient(verify=False, timeout=10.0)

    async def _get_token(self) -> str:
        if self._token:
            return self._token

        async with httpx.AsyncClient(verify=False, timeout=5.0) as c:
            resp = await c.post(
                settings.token_url,
                json={"name": settings.CTRLX_USER, "password": settings.CTRLX_PASS},
            )
            resp.raise_for_status()
            data = resp.json()
            self._token = data["access_token"]
            print("[auth] token obtenido")
            return self._token

    async def fetch_entries(self) -> List[Dict]:
        await self._ensure_http()
        token = await self._get_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        params = {
            "limit": settings.LOGBOOK_LIMIT,
            "reverse": "false",
            "messageType": "rexroth_diag",
        }

        resp = await self._http.get(settings.logbook_url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("entries", [])

    async def close(self) -> None:
        if self._http:
            await self._http.aclose()
            self._http = None
