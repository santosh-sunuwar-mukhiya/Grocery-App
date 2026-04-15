from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=["User"])

@router.get("/{id}")
async def get_task(id: int):
    pass

@router.post("/user")
async def add_task(id: int):
    pass

@router.patch("/{id}")
async def update_task(id: int):
    pass

@router.delete("/{id}")
async def delete_task(id: int):
    pass