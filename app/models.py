from datetime import datetime
import enum
from .db import db

class StatusEnum(str, enum.Enum):
    pending = 'pending'
    in_progress = 'in-progress'
    completed = 'completed'

class PriorityEnum(str, enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    role = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    tasks = db.relationship('Task', back_populates='user', cascade='all, delete-orphan')

class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.Enum(StatusEnum, values_callable=lambda x: [e.value for e in StatusEnum]),
                       default=StatusEnum.pending.value, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.Enum(PriorityEnum, values_callable=lambda x: [e.value for e in PriorityEnum]),
                         default=PriorityEnum.medium.value, nullable=False)

    user = db.relationship('User', back_populates='tasks')