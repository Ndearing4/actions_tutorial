import os
import pytest

pytestmark = pytest.mark.live


class TestApiLive:
    """Verify that the runtime environment has the required secrets.

    These tests read os.environ directly — they are NOT covered by
    python-dotenv so they will fail unless the variables are set in the
    actual environment (export, GitHub Actions secrets, etc.).
    """

    def test_api_token_is_configured(self):
        token = os.environ.get("API_TOKEN")
        assert token, "API_TOKEN is not set in the environment"

    def test_api_token_is_not_placeholder(self):
        token = os.environ.get("API_TOKEN", "")
        assert token != "your-secret-token-here", (
            "API_TOKEN still contains the placeholder from .env.example"
        )

    def test_base_url_is_https(self):
        url = os.environ.get("API_BASE_URL", "")
        assert url.startswith("https://"), (
            f"API_BASE_URL should be an HTTPS URL, got: '{url}'"
        )
