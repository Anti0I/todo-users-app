from .db import db
from .models import Task, User
from typing import Optional, List

class UserRepository:
    def create(self, username: str, role: Optional[str] = None) -> User:
        user = User(username=username, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    def get(self, user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    def list(self) -> List[User]:
        return User.query.all()

    def delete(self, user_id: int) -> bool:
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

class TaskRepository:
    def create(self, task: Task) -> Task:
        db.session.add(task)
        db.session.commit()
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return Task.query.get(task_id)

    def list(self) -> List[Task]:
        return Task.query.order_by(Task.created_at.desc()).all()

    def update(self, task: Task) -> Task:
        db.session.commit()
        return task

    def delete(self, task_id: int) -> bool:
        task = Task.query.get(task_id)
        if not task:
            return False
        db.session.delete(task)
        db.session.commit()
        return True