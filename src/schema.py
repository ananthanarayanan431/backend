
from enum import Enum as PyEnum
from pydantic import BaseModel, Field


class ShipmentStatus(str, PyEnum):
    placed = "PLACED"
    in_transit = "IN_TRANSIT"
    out_for_delivery = "OUT_FOR_DELIVERY"
    delivered = "DELIVERED"

class BaseShipment(BaseModel):
    content: str 
    weight: float = Field(le=25)
    destination: int 

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass 

class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: str | None = Field(default=None, le=25)
    destination: int | None = Field(default=None)
    status: ShipmentStatus