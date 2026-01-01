from typing import Any
from fastapi import FastAPI
from fastapi import HTTPException
from scalar_fastapi import get_scalar_api_reference
from .schema import Shipment
from .databases import database

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/shipments/latest")
def get_latest_shipment() -> Shipment:
    return database[-1]

@app.get("/shipments/{id}")
def get_shipment(id: int) -> Shipment:
    shipment = next((shipment for shipment in database if shipment.id == id), None)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

@app.get("/shipments/{id}/status")
def get_shipment_status(id: int) -> str:
    shipment = next((shipment for shipment in database if shipment.id == id), None)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment.status

@app.get("/shipments-fields/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, str]:
    try:
        allowed_fields = [ "content", "status", "user_id", "user_name"]
        if field not in allowed_fields:
            raise HTTPException(status_code=400, detail="Invalid field")

        for shipment in database:
            if shipment.id == id:
                return {field: getattr(shipment, field, None) or "Not found"}
        return {field: "Not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/shipments")
def create_shipment(shipment: Shipment) -> str:
    database.append(shipment)
    return f"New shipment created: {shipment.content}"


@app.put("/shipments/{id}")
def update_shipments(id: int, shipment_update: Shipment) -> dict[str, Any]:
    try:
        for _, shipment in enumerate(database):
            if shipment.id == id:
                database[id-1] = shipment_update
                print(f"Shipment updated: {shipment.content}")
                return { "shipment": shipment }
        raise HTTPException(status_code=404, detail="Shipment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/all-shipments")
def get_all_shipments() -> list[Shipment]:
    return database

@app.delete("/shipments/{id}")
def delete_shipments(id: int) -> dict[str,Shipment | str]:
    try:
        for _,shipment in enumerate(database):
            if shipment.id == id:
                deleted_shipment = database[id-1]
                database.pop(id-1)
                print(f"Shipment deleted from {shipment.content} & {shipment.id}")
                return {"Deleted Shipment": deleted_shipment}
        raise HTTPException(status_code=404, detail="Shipment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference",
    )
