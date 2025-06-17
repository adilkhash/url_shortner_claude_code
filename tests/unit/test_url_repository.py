import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.repositories.url_repository import URLRepository
from app.models.url import URLModel


class TestURLRepository(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.repository = URLRepository(self.mock_db)

    def test_create_url(self):
        url = URLModel(
            original_url="https://example.com",
            short_code="abc123",
            created_at=datetime.utcnow()
        )
        
        self.mock_db.execute.return_value = Mock()
        self.mock_db.fetchone.return_value = {
            "id": 1,
            "original_url": "https://example.com",
            "short_code": "abc123",
            "created_at": url.created_at,
            "click_count": 0,
            "expires_at": None,
            "is_active": True
        }

        result = self.repository.create(url)

        self.assertIsInstance(result, URLModel)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.original_url, "https://example.com")
        self.assertEqual(result.short_code, "abc123")

    def test_get_by_short_code_returns_url_when_found(self):
        self.mock_db.execute.return_value = Mock()
        self.mock_db.fetchone.return_value = {
            "id": 1,
            "original_url": "https://example.com",
            "short_code": "abc123",
            "created_at": datetime.utcnow(),
            "click_count": 5,
            "expires_at": None,
            "is_active": True
        }

        result = self.repository.get_by_short_code("abc123")

        self.assertIsInstance(result, URLModel)
        self.assertEqual(result.short_code, "abc123")
        self.assertEqual(result.click_count, 5)

    def test_get_by_short_code_returns_none_when_not_found(self):
        self.mock_db.execute.return_value = Mock()
        self.mock_db.fetchone.return_value = None

        result = self.repository.get_by_short_code("nonexistent")

        self.assertIsNone(result)

    def test_get_by_id_returns_url_when_found(self):
        self.mock_db.execute.return_value = Mock()
        self.mock_db.fetchone.return_value = {
            "id": 1,
            "original_url": "https://example.com",
            "short_code": "abc123",
            "created_at": datetime.utcnow(),
            "click_count": 0,
            "expires_at": None,
            "is_active": True
        }

        result = self.repository.get_by_id(1)

        self.assertIsInstance(result, URLModel)
        self.assertEqual(result.id, 1)

    def test_increment_click_count(self):
        self.mock_db.execute.return_value = Mock()
        self.mock_db.fetchone.return_value = {
            "id": 1,
            "original_url": "https://example.com",
            "short_code": "abc123",
            "created_at": datetime.utcnow(),
            "click_count": 6,
            "expires_at": None,
            "is_active": True
        }

        result = self.repository.increment_click_count(1)

        self.assertIsInstance(result, URLModel)
        self.assertEqual(result.click_count, 6)
        self.mock_db.execute.assert_called()

    def test_deactivate_url(self):
        self.mock_db.execute.return_value = Mock()
        
        self.repository.deactivate_url(1)
        
        self.mock_db.execute.assert_called()
        self.mock_db.commit.assert_called()


if __name__ == '__main__':
    unittest.main()