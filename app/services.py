from .repositories import UserRepository, TaskRepository
from .models import Task

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, username: str, role: [str] = None):
        return self.repo.create(username=username, role=role)

    def get_user(self, user_id: int):
        return self.repo.get(user_id)

class TaskService:
    def __init__(self, repo: TaskRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def create_task(self, **kwargs) -> Task:
        user = self.user_repo.get(kwargs.get('user_id'))
        if not user:
            raise ValueError('User not found')
        task = Task(**kwargs)
        return self.repo.create(task)

    def list_tasks(self):
        return self.repo.list()

    def get_task(self, task_id: int):
        return self.repo.get(task_id)

    def update_task(self, task_id: int, **changes):
        task = self.repo.get(task_id)
        if not task:
            return None
        for k, v in changes.items():
            if hasattr(task, k):
                setattr(task, k, v)
        return self.repo.update(task)

    def delete_task(self, task_id: int):
        return self.repo.delete(task_id)