from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from practice.databases.session import create_db_tables
from practice.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
   create_db_tables()
   print("Server started and all the tables are created.")
   yield
   print("...Server Stopped and Connection with Tables are closed.")
app = FastAPI(lifespan=lifespan_handler)

@app.get("/")
def root():
    return {"message": "Hello world."}



###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    # Check for shipment with given id
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )
    save

    return shipments[id]


### Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    # Create and assign shipment a new id
    new_id = max(shipments.keys()) + 1
    # Add to shipments dict
    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": "placed",
    }
    save()
    # Return id for later use
    return {"id": new_id}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    # Update data with given fields
    shipments[id].update(body)
    save()
    return shipments[id]


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    # Remove from datastore
    shipments.pop(id)
    save()
    return {"detail": f"Shipment with id #{id} is deleted!"}







### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )