from pydantic import BaseModel


class DigitalTwinEventCreate(BaseModel):
    event_type: str
    payload: dict
