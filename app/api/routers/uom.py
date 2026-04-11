from fastapi import APIRouter
from app.api.dependencies import UOMServiceDep, UserDep
from app.api.schemas.uom import UOMCreate, UOMRead

router = APIRouter(prefix="/uom", tags=["UOM"])


@router.get("/", response_model=list[UOMRead])
async def get_uoms(service: UOMServiceDep):
    """Public — anyone can list units of measure."""
    return await service.get_all()


@router.post("/", response_model=UOMRead)
async def create_uom(uom: UOMCreate, service: UOMServiceDep, _: UserDep):
    """Protected — only authenticated users can add a new UOM."""
    return await service.create(uom)