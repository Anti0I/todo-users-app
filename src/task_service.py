from flask import current_app
from models import Task, StatusEnum, PriorityEnum
from schemas import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    @staticmethod
    def get_all():
        try:
            tasks = current_app._session.query(Task).all()
            return [TaskResponse.model_validate(task) for task in tasks], None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_by_id(task_id):
        try:
            task = current_app._session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return None, "Task not found"
            return TaskResponse.model_validate(task), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def create(data: TaskCreate):
        try:
            task = Task(
                task_name=data.task_name,
                user_id=data.user_id,
                due_date=data.due_date,
                status=StatusEnum(data.status.value),
                priority=PriorityEnum(data.priority.value)
            )
            
            current_app._session.add(task)
            current_app._session.commit()
            return TaskResponse.model_validate(task), None
        except Exception as e:
            current_app._session.rollback()
            return None, str(e)

    @staticmethod
    def update(task_id, data: TaskUpdate):
        try:
            task = current_app._session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return None, "Task not found"
            
            if data.task_name is not None:
                task.task_name = data.task_name
            if data.user_id is not None:
                task.user_id = data.user_id
            if data.due_date is not None:
                task.due_date = data.due_date
            if data.status is not None:
                task.status = StatusEnum(data.status.value)
            if data.priority is not None:
                task.priority = PriorityEnum(data.priority.value)
            
            current_app._session.commit()
            return TaskResponse.model_validate(task), None
        except Exception as e:
            current_app._session.rollback()
            return None, str(e)

    @staticmethod
    def delete(task_id):
        try:
            task = current_app._session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return None, "Task not found"
            
            current_app._session.delete(task)
            current_app._session.commit()
            return True, None
        except Exception as e:
            current_app._session.rollback()
            return None, str(e)