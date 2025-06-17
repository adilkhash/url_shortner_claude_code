import unittest
from unittest.mock import Mock, patch
from litestar.testing import TestClient
from app.main import create_app


class TestURLEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = TestClient(app=self.app)

    @patch('app.services.url_service.URLService')
    def test_create_short_url_success(self, mock_service_class):
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        
        mock_url = Mock()
        mock_url.id = 1
        mock_url.original_url = "https://example.com"
        mock_url.short_code = "abc123"
        mock_url.created_at = "2023-01-01T00:00:00"
        mock_url.click_count = 0
        mock_url.expires_at = None
        mock_url.is_active = True
        
        mock_service.create_url.return_value = mock_url

        response = self.client.post(
            "/api/v1/urls",
            json={"original_url": "https://example.com"}
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["original_url"], "https://example.com")
        self.assertEqual(data["short_code"], "abc123")

    @patch('app.services.url_service.URLService')
    def test_create_short_url_with_custom_code(self, mock_service_class):
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        
        mock_url = Mock()
        mock_url.id = 1
        mock_url.original_url = "https://example.com"
        mock_url.short_code = "custom123"
        mock_url.created_at = "2023-01-01T00:00:00"
        mock_url.click_count = 0
        mock_url.expires_at = None
        mock_url.is_active = True
        
        mock_service.create_url.return_value = mock_url

        response = self.client.post(
            "/api/v1/urls",
            json={
                "original_url": "https://example.com",
                "custom_code": "custom123"
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["short_code"], "custom123")

    @patch('app.services.url_service.URLService')
    def test_redirect_to_original_url(self, mock_service_class):
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        
        mock_url = Mock()
        mock_url.id = 1
        mock_url.original_url = "https://example.com"
        mock_url.short_code = "abc123"
        mock_url.is_active = True
        mock_url.expires_at = None
        
        mock_service.get_url_by_short_code.return_value = mock_url
        mock_service.is_url_expired.return_value = False

        response = self.client.get("/abc123", follow_redirects=False)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.headers["location"], "https://example.com")
        mock_service.increment_click_count.assert_called_once_with(1)

    @patch('app.services.url_service.URLService')
    def test_redirect_not_found(self, mock_service_class):
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_service.get_url_by_short_code.return_value = None

        response = self.client.get("/nonexistent")

        self.assertEqual(response.status_code, 404)

    @patch('app.services.url_service.URLService')
    def test_get_url_stats(self, mock_service_class):
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        
        mock_url = Mock()
        mock_url.id = 1
        mock_url.original_url = "https://example.com"
        mock_url.short_code = "abc123"
        mock_url.created_at = "2023-01-01T00:00:00"
        mock_url.click_count = 10
        mock_url.expires_at = None
        mock_url.is_active = True
        
        mock_service.get_url_by_short_code.return_value = mock_url

        response = self.client.get("/api/v1/urls/abc123/stats")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["click_count"], 10)
        self.assertEqual(data["short_code"], "abc123")


if __name__ == '__main__':
    unittest.main()