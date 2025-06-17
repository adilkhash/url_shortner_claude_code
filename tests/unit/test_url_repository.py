import unittest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from app.repositories.url_repository import URLRepository
from app.models.url import URLModel


class TestURLRepository(unittest.TestCase):
    def setUp(self):
        self.mock_db = Mock()
        self.mock_session = Mock()
        self.mock_db.get_session.return_value = self.mock_session
        self.repository = URLRepository(self.mock_db)

    def test_create_url(self):
        url = URLModel(
            original_url="https://example.com",
            short_code="abc123",
            created_at=datetime.utcnow()
        )
        url.id = 1

        result = self.repository.create(url)

        self.mock_session.add.assert_called_once_with(url)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(url)
        self.assertIsInstance(result, URLModel)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.original_url, "https://example.com")
        self.assertEqual(result.short_code, "abc123")

    def test_get_by_short_code_returns_url_when_found(self):
        mock_url = URLModel(
            original_url="https://example.com",
            short_code="abc123",
            click_count=5
        )
        mock_url.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_url
        self.mock_session.query.return_value = mock_query

        result = self.repository.get_by_short_code("abc123")

        self.mock_session.query.assert_called_once_with(URLModel)
        self.assertIsInstance(result, URLModel)
        self.assertEqual(result.short_code, "abc123")
        self.assertEqual(result.click_count, 5)

    def test_get_by_short_code_returns_none_when_not_found(self):
        mock_query = Mock()
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        self.mock_session.query.return_value = mock_query

        result = self.repository.get_by_short_code("nonexistent")

        self.assertIsNone(result)

    def test_get_by_id_returns_url_when_found(self):
        mock_url = URLModel(
            original_url="https://example.com",
            short_code="abc123"
        )
        mock_url.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_url
        self.mock_session.query.return_value = mock_query

        result = self.repository.get_by_id(1)

        self.assertIsInstance(result, URLModel)
        self.assertEqual(result.id, 1)

    def test_increment_click_count(self):
        mock_url = URLModel(
            original_url="https://example.com",
            short_code="abc123",
            click_count=5
        )
        mock_url.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_url
        self.mock_session.query.return_value = mock_query

        result = self.repository.increment_click_count(1)

        self.assertIsInstance(result, URLModel)
        self.assertEqual(result.click_count, 6)
        self.mock_session.commit.assert_called_once()

    def test_deactivate_url(self):
        mock_url = URLModel(
            original_url="https://example.com",
            short_code="abc123",
            is_active=True
        )
        mock_url.id = 1
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_url
        self.mock_session.query.return_value = mock_query

        result = self.repository.deactivate_url(1)
        
        self.assertTrue(result)
        self.assertFalse(mock_url.is_active)
        self.mock_session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()