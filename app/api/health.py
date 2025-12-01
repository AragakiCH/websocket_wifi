from fastapi import APIRouter

from ..core.config import get_settings

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/info")
async def info():
    s = get_settings()
    return {
        "ctrlx_host": s.CTRLX_HOST,
        "ctrlx_port": s.CTRLX_PORT,
        "opcua_enabled": s.OPCUA_ENABLED,
    }
      