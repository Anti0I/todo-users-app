import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from user_service import UserService
from schemas import UserCreate, UserUpdate


class TestUserService:
    
    @patch('user_service.current_app')
    def test_get_all_users(self, mock_app):
        """Test getting all users"""
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {
            "id": 1,
            "username": "testuser",
            "role": "admin",
            "created_at": datetime.now()
        }
        
        mock_app._session.query.return_value.all.return_value = [mock_user]
        
        result, error = UserService.get_all()
        
        assert error is None
        assert len(result) == 1

    @patch('user_service.current_app')
    def test_get_user_by_id(self, mock_app):
        """Test getting a user by ID"""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "testuser"
        
        mock_app._session.query.return_value.filter.return_value.first.return_value = mock_user
        
        result, error = UserService.get_by_id(1)
        
        assert error is None
        assert result.username == "testuser"

    @patch('user_service.current_app')
    def test_get_user_by_invalid_id(self, mock_app):
        """Test getting a user with invalid ID"""
        mock_app._session.query.return_value.filter.return_value.first.return_value = None
        
        result, error = UserService.get_by_id(999)
        
        assert error == "User not found"
        assert result is None

    @patch('user_service.User')
    @patch('user_service.current_app')
    def test_create_user(self, mock_app, mock_user_model):
        """Test creating a new user"""
        user_data = UserCreate(username="newuser", role="user")
        
        mock_user = MagicMock()
        mock_user_model.return_value = mock_user
        
        result, error = UserService.create(user_data)
        
        mock_app._session.add.assert_called_once()
        mock_app._session.commit.assert_called_once()

    @patch('user_service.User')
    @patch('user_service.current_app')
    def test_update_user(self, mock_app, mock_user_model):
        """Test updating a user"""
        mock_user = MagicMock()
        mock_app._session.query.return_value.filter.return_value.first.return_value = mock_user
        
        user_data = UserUpdate(username="updated")
        
        result, error = UserService.update(1, user_data)
        
        assert mock_app._session.commit.called

    @patch('user_service.current_app')
    def test_update_nonexistent_user(self, mock_app):
        """Test updating a non-existent user"""
        mock_app._session.query.return_value.filter.return_value.first.return_value = None
        
        user_data = UserUpdate(username="updated")
        
        result, error = UserService.update(999, user_data)
        
        assert error == "User not found"
        assert result is None

    @patch('user_service.current_app')
    def test_delete_user(self, mock_app):
        """Test deleting a user"""
        mock_user = MagicMock()
        mock_app._session.query.return_value.filter.return_value.first.return_value = mock_user
        
        result, error = UserService.delete(1)
        
        assert error is None
        assert result is True
        mock_app._session.delete.assert_called_once()
        mock_app._session.commit.assert_called_once()

    @patch('user_service.current_app')
    def test_delete_nonexistent_user(self, mock_app):
        """Test deleting a non-existent user"""
        mock_app._session.query.return_value.filter.return_value.first.return_value = None
        
        result, error = UserService.delete(999)
        
        assert error == "User not found"
        assert result is None