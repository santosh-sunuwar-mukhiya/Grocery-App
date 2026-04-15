from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import TaskServiceDep
from app.api.schemas.task import TaskRead, TaskCreate, TaskUpdate

router = APIRouter(prefix="/task", tags=["Task"])

@router.get("/{id}", response_model=TaskRead)
async def get_task(id: int, service: TaskServiceDep):
    task = await service.get(id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id #{task} was not found"
        )

    return task

@router.post("/task")
async def add_task(task_create: TaskCreate, service: TaskServiceDep):
    task = await service.add(task_create)
    return task

@router.patch("/{id}")
async def update_task(id: int,update_data: TaskUpdate, service: TaskServiceDep):
    task = update_data.model_dump(exclude_unset=True)

    if not task:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"No data provided to update on {task}"
        )

    updated_task = await service.update(id, task)
    return updated_task



@router.delete("/{id}")
async def delete_task(id: int, service: TaskServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}