from typing import Any, Dict, Optional, Literal, List
from pydantic import BaseModel, Field


EventSource = Literal["ctrlx_logbook", "opcua"]


class LogbookEntry(BaseModel):
    timestamp: Optional[str]
    entity: Optional[str]
    logLevel: Optional[str]
    mainTitle: Optional[str]
    detailedTitle: Optional[str]
    dynamicDescription: Optional[str]
    mainDiagnosisCode: Optional[str]
    cursor: Optional[str] = Field(alias="__CURSOR", default=None)

    class Config:
        allow_population_by_field_name = True
        extra = "allow"   # por si ctrlX mete más campos


class Event(BaseModel):
    type: Literal["logbook", "opcua"]
    source: EventSource
    entries: Optional[List[LogbookEntry]] = None
    payload: Optional[Dict[str, Any]] = None
