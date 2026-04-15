from fastapi import APIRouter, HTTPException, status

from practice.api.dependencies import ShipmentServiceDep
from practice.databases.models import Shipment
from practice.api.schemas.shipment import ShipmentRead, ShipmentUpdate, ShipmentCreate

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Hello world."}



###  a shipment by id
@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id: int, service: ShipmentServiceDep):
    # Check for shipment with given id
    shipment = await service.get(id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@router.post("/shipment", status_code = status.HTTP_201_CREATED, response_model = ShipmentRead)
async def submit_shipment(shipment: ShipmentCreate, service: ShipmentServiceDep) -> Shipment:
    return await service.add(shipment)


### Update fields of a shipment
@router.patch("/shipment", response_model=ShipmentRead)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ShipmentServiceDep):
    update_shipment = shipment_update.model_dump(exclude_unset=True)

    if not update_shipment:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No data provided to update."
        )

    shipment = await service.update(id, shipment_update)

    return shipment


### Delete a shipment by id
@router.delete("/shipment")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}
