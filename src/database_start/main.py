from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .database import Database
from .models import ShipmentCreate, ShipmentRead, ShipmentUpdate

app = FastAPI()
db = Database()


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    """get the shipments from the given ID"""
    try:
        shipment = db.get(id)
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
            )
        return shipment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/shipment", response_model=None)
def create_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    """Create a new shipment"""
    try:
        new_id = db.create(shipment=shipment)
        if new_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not found"
            )
        return {"Id": new_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    """Update the shipment data"""
    try:
        updated_shipment = db.update(id=id, shipment=shipment)
        if updated_shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="not found"
            )
        return updated_shipment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.delete("/shipment", response_model=None)
def delete_shipment(id: int):
    """Delete the shipment data"""
    try:
        db.delete(id=id)
        return {"message": "Shipment deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Reference",
    )
