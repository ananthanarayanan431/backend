from pydantic import BaseModel


class Shipment(BaseModel):
    id: int
    content: str
    status: str
    user_id: str
    user_name: str
