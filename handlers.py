from flask import jsonify, request, Response
from flask.views import MethodView
from flask import current_app
from database import Task, User, StatusEnum, PriorityEnum


class BaseHandler(MethodView):
    def get_response(self, data, status_code):
        return jsonify(data), status_code

    def get_error(self, message, status_code=400):
        return jsonify({"error": message}), status_code


class TaskHandler(BaseHandler):
    def get(self) -> Response:
        try:
            tasks = current_app._session.query(Task).all()
            return self.get_response({"tasks": [task.to_dict() for task in tasks]}, 200)
        except Exception as e:
            return self.get_error(str(e), 500)

    def post(self) -> Response:
        try:
            data = request.json
            required_fields = ["task_name", "user_id", "due_date"]
            
            if not all(field in data for field in required_fields):
                return self.get_error("Missing required fields", 400)
            
            status = data.get("status", "pending")
            priority = data.get("priority", "medium")
            
            try:
                status_enum = StatusEnum(status)
                priority_enum = PriorityEnum(priority)
            except ValueError:
                return self.get_error("Invalid status or priority", 400)
            
            new_task = Task(
                task_name=data["task_name"],
                user_id=data["user_id"],
                due_date=data["due_date"],
                status=status_enum,
                priority=priority_enum
            )
            
            current_app._session.add(new_task)
            current_app._session.commit()
            return self.get_response({"message": "Task created", "task": new_task.to_dict()}, 201)
        
        except Exception as e:
            current_app._session.rollback()
            return self.get_error(str(e), 500)

    def patch(self, item_id: int) -> Response:
        try:
            task = current_app._session.query(Task).filter(Task.id == item_id).first()
            
            if not task:
                return self.get_error("Task not found", 404)
            
            data = request.json
            
            if "task_name" in data:
                task.task_name = data["task_name"]
            if "user_id" in data:
                task.user_id = data["user_id"]
            if "due_date" in data:
                task.due_date = data["due_date"]
            if "status" in data:
                try:
                    task.status = StatusEnum(data["status"])
                except ValueError:
                    return self.get_error("Invalid status", 400)
            if "priority" in data:
                try:
                    task.priority = PriorityEnum(data["priority"])
                except ValueError:
                    return self.get_error("Invalid priority", 400)
            
            current_app._session.commit()
            return self.get_response({"message": "Task updated", "task": task.to_dict()}, 200)
        
        except Exception as e:
            current_app._session.rollback()
            return self.get_error(str(e), 500)

    def delete(self, item_id: int) -> Response:
        try:
            task = current_app._session.query(Task).filter(Task.id == item_id).first()
            
            if not task:
                return self.get_error("Task not found", 404)
            
            current_app._session.delete(task)
            current_app._session.commit()
            return self.get_response({"message": "Task deleted"}, 200)
        
        except Exception as e:
            current_app._session.rollback()
            return self.get_error(str(e), 500)


class UserHandler(BaseHandler):
    def get(self) -> Response:
        try:
            users = current_app._session.query(User).all()
            return self.get_response({"users": [user.to_dict() for user in users]}, 200)
        except Exception as e:
            return self.get_error(str(e), 500)

    def post(self) -> Response:
        try:
            data = request.json
            required_fields = ["username", "role"]
            
            if not all(field in data for field in required_fields):
                return self.get_error("Missing required fields", 400)
            
            new_user = User(
                username=data["username"],
                role=data["role"]
            )
            
            current_app._session.add(new_user)
            current_app._session.commit()
            return self.get_response({"message": "User created", "user": new_user.to_dict()}, 201)
        
        except Exception as e:
            current_app._session.rollback()
            return self.get_error(str(e), 500)

    def patch(self, item_id: int) -> Response:
        try:
            user = current_app._session.query(User).filter(User.id == item_id).first()
            
            if not user:
                return self.get_error("User not found", 404)
            
            data = request.json
            
            if "username" in data:
                user.username = data["username"]
            if "role" in data:
                user.role = data["role"]
            
            current_app._session.commit()
            return self.get_response({"message": "User updated", "user": user.to_dict()}, 200)
        
        except Exception as e:
            current_app._session.rollback()
            return self.get_error(str(e), 500)

    def delete(self, item_id: int) -> Response:
        try:
            user = current_app._session.query(User).filter(User.id == item_id).first()
            
            if not user:
                return self.get_error("User not found", 404)
            
            current_app._session.delete(user)
            current_app._session.commit()
            return self.get_response({"message": "User deleted"}, 200)
        
        except Exception as e:
            current_app._session.rollback()
            return self.get_error(str(e), 500)