from flask import current_app
from models import User
from schemas import UserCreate, UserUpdate, UserResponse


class UserService:
    @staticmethod
    def get_all():
        try:
            users = current_app._session.query(User).all()
            return [UserResponse.model_validate(user) for user in users], None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_by_id(user_id):
        try:
            user = current_app._session.query(User).filter(User.id == user_id).first()
            if not user:
                return None, "User not found"
            return UserResponse.model_validate(user), None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def create(data: UserCreate):
        try:
            user = User(
                username=data.username,
                role=data.role
            )
            
            current_app._session.add(user)
            current_app._session.commit()
            return UserResponse.model_validate(user), None
        except Exception as e:
            current_app._session.rollback()
            return None, str(e)

    @staticmethod
    def update(user_id, data: UserUpdate):
        try:
            user = current_app._session.query(User).filter(User.id == user_id).first()
            if not user:
                return None, "User not found"
            
            if data.username is not None:
                user.username = data.username
            if data.role is not None:
                user.role = data.role
            
            current_app._session.commit()
            return UserResponse.model_validate(user), None
        except Exception as e:
            current_app._session.rollback()
            return None, str(e)

    @staticmethod
    def delete(user_id):
        try:
            user = current_app._session.query(User).filter(User.id == user_id).first()
            if not user:
                return None, "User not found"
            
            current_app._session.delete(user)
            current_app._session.commit()
            return True, None
        except Exception as e:
            current_app._session.rollback()
            return None, str(e)