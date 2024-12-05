from pydantic import BaseModel, Field


class EventPayload(BaseModel):
    type_: str = Field(alias="type")
    amount: float
    user_id: int
    t: int | str


class EventResponse(BaseModel):
    alert: bool
    alert_codes: list[int] | bool = False
    user_id: int
