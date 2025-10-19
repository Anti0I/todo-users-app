import pytest
from unittest.mock import patch, MagicMock
from datetime import date, datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from task_service import TaskService
from schemas import TaskCreate, TaskUpdate


class TestTaskService:
    
    @patch('task_service.current_app')
    def test_get_all_tasks(self, mock_app):
        """Test getting all tasks"""
        mock_task = MagicMock()
        mock_task.to_dict.return_value = {
            "id": 1,
            "task_name": "Test Task",
            "user_id": 1,
            "created_at": datetime.now(),
            "status": "pending",
            "due_date": date.today(),
            "priority": "medium"
        }
        
        mock_app._session.query.return_value.all.return_value = [mock_task]
        
        result, error = TaskService.get_all()
        
        assert error is None
        assert len(result) == 1

    @patch('task_service.current_app')
    def test_get_task_by_id(self, mock_app):
        """Test getting a task by ID"""
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.task_name = "Test Task"
        
        mock_app._session.query.return_value.filter.return_value.first.return_value = mock_task
        
        result, error = TaskService.get_by_id(1)
        
        assert error is None
        assert result.task_name == "Test Task"

    @patch('task_service.current_app')
    def test_get_task_by_invalid_id(self, mock_app):
        """Test getting a task with invalid ID"""
        mock_app._session.query.return_value.filter.return_value.first.return_value = None
        
        result, error = TaskService.get_by_id(999)
        
        assert error == "Task not found"
        assert result is None

    @patch('task_service.Task')
    @patch('task_service.current_app')
    def test_create_task(self, mock_app, mock_task_model):
        """Test creating a new task"""
        task_data = TaskCreate(
            task_name="New Task",
            user_id=1,
            due_date=date.today()
        )
        
        mock_task = MagicMock()
        mock_task_model.return_value = mock_task
        
        result, error = TaskService.create(task_data)
        
        mock_app._session.add.assert_called_once()
        mock_app._session.commit.assert_called_once()

    @patch('task_service.Task')
    @patch('task_service.current_app')
    def test_update_task(self, mock_app, mock_task_model):
        """Test updating a task"""
        mock_task = MagicMock()
        mock_app._session.query.return_value.filter.return_value.first.return_value = mock_task
        
        task_data = TaskUpdate(task_name="Updated")
        
        result, error = TaskService.update(1, task_data)
        
        assert mock_app._session.commit.called

    @patch('task_service.current_app')
    def test_update_nonexistent_task(self, mock_app):
        """Test updating a non-existent task"""
        mock_app._session.query.return_value.filter.return_value.first.return_value = None
        
        task_data = TaskUpdate(task_name="Updated")
        
        result, error = TaskService.update(999, task_data)
        
        assert error == "Task not found"
        assert result is None

    @patch('task_service.current_app')
    def test_delete_task(self, mock_app):
        """Test deleting a task"""
        mock_task = MagicMock()
        mock_app._session.query.return_value.filter.return_value.first.return_value = mock_task
        
        result, error = TaskService.delete(1)
        
        assert error is None
        assert result is True
        mock_app._session.delete.assert_called_once()
        mock_app._session.commit.assert_called_once()

    @patch('task_service.current_app')
    def test_delete_nonexistent_task(self, mock_app):
        """Test deleting a non-existent task"""
        mock_app._session.query.return_value.filter.return_value.first.return_value = None
        
        result, error = TaskService.delete(999)
        
        assert error == "Task not found"
        assert result is None