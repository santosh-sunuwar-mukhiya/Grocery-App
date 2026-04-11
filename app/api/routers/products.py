from uuid import UUID
from fastapi import APIRouter
from app.api.dependencies import ProductServiceDep, UserDep
from app.api.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductRead])
async def get_products(service: ProductServiceDep):
    return await service.get_all()


@router.post("/", response_model=ProductRead)
async def create_product(product: ProductCreate, service: ProductServiceDep, _: UserDep):
    return await service.create(product)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: UUID,
    product: ProductUpdate,
    service: ProductServiceDep,
    _: UserDep,
):
    return await service.update(product_id, product)


@router.delete("/{product_id}")
async def delete_product(product_id: UUID, service: ProductServiceDep, _: UserDep):
    await service.delete(product_id)
    return {"detail": "Product deleted"}