from flask import jsonify, request, Response
from flask.views import MethodView
from pydantic import ValidationError
from task_service import TaskService
from user_service import UserService
from schemas import TaskCreate, TaskUpdate, UserCreate, UserUpdate


class BaseHandler(MethodView):
    def response(self, data=None, message=None, status_code=200):
        payload = {}
        if message:
            payload["message"] = message
        if data is not None:
            if isinstance(data, list):
                payload["data"] = [item.model_dump() if hasattr(item, 'model_dump') else item for item in data]
            else:
                payload["data"] = data.model_dump() if hasattr(data, 'model_dump') else data
        return jsonify(payload), status_code

    def error(self, message, status_code=400):
        return jsonify({"error": message}), status_code


class TaskHandler(BaseHandler):
    def get(self, item_id=None):
        if item_id:
            data, error = TaskService.get_by_id(item_id)
            if error:
                return self.error(error, 404)
            return self.response(data=data, status_code=200)
        
        data, error = TaskService.get_all()
        if error:
            return self.error(error, 500)
        return self.response(data=data, status_code=200)

    def post(self):
        try:
            task_data = TaskCreate(**request.json)
            data, error = TaskService.create(task_data)
            if error:
                return self.error(error, 400)
            return self.response(data=data, message="Task created", status_code=201)
        except ValidationError as e:
            return self.error(str(e), 422)

    def patch(self, item_id):
        try:
            task_data = TaskUpdate(**request.json)
            data, error = TaskService.update(item_id, task_data)
            if error:
                return self.error(error, 404)
            return self.response(data=data, message="Task updated", status_code=200)
        except ValidationError as e:
            return self.error(str(e), 422)

    def delete(self, item_id):
        _, error = TaskService.delete(item_id)
        if error:
            return self.error(error, 404)
        return self.response(message="Task deleted", status_code=200)


class UserHandler(BaseHandler):
    def get(self, item_id=None):
        if item_id:
            data, error = UserService.get_by_id(item_id)
            if error:
                return self.error(error, 404)
            return self.response(data=data, status_code=200)
        
        data, error = UserService.get_all()
        if error:
            return self.error(error, 500)
        return self.response(data=data, status_code=200)

    def post(self):
        try:
            user_data = UserCreate(**request.json)
            data, error = UserService.create(user_data)
            if error:
                return self.error(error, 400)
            return self.response(data=data, message="User created", status_code=201)
        except ValidationError as e:
            return self.error(str(e), 422)

    def patch(self, item_id):
        try:
            user_data = UserUpdate(**request.json)
            data, error = UserService.update(item_id, user_data)
            if error:
                return self.error(error, 404)
            return self.response(data=data, message="User updated", status_code=200)
        except ValidationError as e:
            return self.error(str(e), 422)

    def delete(self, item_id):
        _, error = UserService.delete(item_id)
        if error:
            return self.error(error, 404)
        return self.response(message="User deleted", status_code=200)