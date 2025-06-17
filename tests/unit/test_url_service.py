import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from app.services.url_service import URLService
from app.models.url import URLModel


class TestURLService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock()
        self.url_service = URLService(self.mock_repository)

    def test_generate_short_code_creates_unique_code(self):
        self.mock_repository.get_by_short_code.return_value = None
        
        short_code = self.url_service.generate_short_code()
        
        self.assertIsInstance(short_code, str)
        self.assertEqual(len(short_code), 6)
        self.assertTrue(short_code.isalnum())

    def test_generate_short_code_retries_on_collision(self):
        self.mock_repository.get_by_short_code.side_effect = [
            URLModel(id=1, short_code="abc123"),  # collision
            None  # no collision
        ]
        
        short_code = self.url_service.generate_short_code()
        
        self.assertEqual(self.mock_repository.get_by_short_code.call_count, 2)

    def test_create_url_with_custom_code(self):
        custom_code = "custom123"
        original_url = "https://example.com"
        self.mock_repository.get_by_short_code.return_value = None
        expected_url = URLModel(id=1, original_url=original_url, short_code=custom_code)
        self.mock_repository.create.return_value = expected_url

        result = self.url_service.create_url(original_url, custom_code=custom_code)

        self.mock_repository.create.assert_called_once()
        self.assertEqual(result.short_code, custom_code)
        self.assertEqual(result.original_url, original_url)

    def test_create_url_with_duplicate_custom_code_raises_error(self):
        custom_code = "duplicate"
        original_url = "https://example.com"
        self.mock_repository.get_by_short_code.return_value = URLModel(id=1, short_code=custom_code)

        with self.assertRaises(ValueError) as context:
            self.url_service.create_url(original_url, custom_code=custom_code)

        self.assertIn("already exists", str(context.exception))

    def test_create_url_without_custom_code_generates_code(self):
        original_url = "https://example.com"
        self.mock_repository.get_by_short_code.return_value = None
        expected_url = URLModel(id=1, original_url=original_url, short_code="abc123")
        self.mock_repository.create.return_value = expected_url

        with patch.object(self.url_service, 'generate_short_code', return_value="abc123"):
            result = self.url_service.create_url(original_url)

        self.assertEqual(result.short_code, "abc123")

    def test_get_url_by_short_code(self):
        short_code = "abc123"
        expected_url = URLModel(id=1, short_code=short_code)
        self.mock_repository.get_by_short_code.return_value = expected_url

        result = self.url_service.get_url_by_short_code(short_code)

        self.assertEqual(result, expected_url)
        self.mock_repository.get_by_short_code.assert_called_once_with(short_code)

    def test_increment_click_count(self):
        url_id = 1
        expected_url = URLModel(id=url_id, click_count=5)
        self.mock_repository.increment_click_count.return_value = expected_url

        result = self.url_service.increment_click_count(url_id)

        self.assertEqual(result, expected_url)
        self.mock_repository.increment_click_count.assert_called_once_with(url_id)

    def test_is_url_expired_returns_false_for_non_expired(self):
        future_date = datetime.utcnow() + timedelta(days=1)
        url = URLModel(expires_at=future_date)

        result = self.url_service.is_url_expired(url)

        self.assertFalse(result)

    def test_is_url_expired_returns_true_for_expired(self):
        past_date = datetime.utcnow() - timedelta(days=1)
        url = URLModel(expires_at=past_date)

        result = self.url_service.is_url_expired(url)

        self.assertTrue(result)

    def test_is_url_expired_returns_false_for_no_expiry(self):
        url = URLModel(expires_at=None)

        result = self.url_service.is_url_expired(url)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()