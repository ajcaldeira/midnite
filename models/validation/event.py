from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EventPayload(BaseModel):
    type_: str = Field(alias="type")
    amount: float
    user_id: int
    t: Optional[int] = Field(default_factory=lambda: int(datetime.now().timestamp()))


class EventResponse(BaseModel):
    alert: bool
    alert_codes: list[int] | bool = False
    user_id: int
