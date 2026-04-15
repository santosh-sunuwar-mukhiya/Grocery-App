from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.task import TaskCreate, TaskUpdate
from app.databases.models import Task, TaskStatus


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Task:
        task = await self.session.get(Task, id)
        return task

    async def add(self, task_create: TaskCreate) -> Task:
        new_task  = Task(
            **task_create.model_dump(),
            status=TaskStatus.not_done,
            estimated_time=datetime.now() + timedelta(days=3)
        )

        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)

        return new_task

    async def update(self, id: int, update_task: TaskUpdate) -> TaskUpdate:

        task = self.session.get(Task, id)

        if not task:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Task with id #{task} does not exist."
            )

        task.sqlmodel_update(update_task)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete(self, id: int):
        task = self.session.get(Task, id)

        if not task:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Task with id #{task} does not exist."
            )

        await self.session.delete(task)
        await self.session.commit()