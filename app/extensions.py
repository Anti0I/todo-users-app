from .repositories import UserRepository, TaskRepository
from .services import UserService, TaskService

class Extensions:
    def __init__(self):
        self.user_repo = None
        self.task_repo = None
        self.user_service = None
        self.task_service = None

extensions = Extensions()

def init_extensions(app, db):
    extensions.user_repo = UserRepository()
    extensions.task_repo = TaskRepository()
    extensions.user_service = UserService(extensions.user_repo)
    extensions.task_service = TaskService(extensions.task_repo, extensions.user_repo)
    app.extensions['app_services'] = extensions