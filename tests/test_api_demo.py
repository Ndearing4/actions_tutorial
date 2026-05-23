import os
import pytest
from src.api_demo import get_api_config, build_headers


class TestGetApiConfig:
    def test_returns_config_when_token_set(self, monkeypatch):
        monkeypatch.setenv("API_TOKEN", "test-secret-123")
        monkeypatch.setenv("API_BASE_URL", "https://staging.example.com")

        config = get_api_config()

        assert config["token"] == "test-secret-123"
        assert config["base_url"] == "https://staging.example.com"

    def test_uses_default_base_url(self, monkeypatch):
        monkeypatch.setenv("API_TOKEN", "tok")
        monkeypatch.delenv("API_BASE_URL", raising=False)

        config = get_api_config()

        assert config["base_url"] == "https://api.example.com"

    def test_raises_when_token_missing(self, monkeypatch):
        monkeypatch.delenv("API_TOKEN", raising=False)

        with pytest.raises(ValueError, match="API_TOKEN is not set"):
            get_api_config()


class TestBuildHeaders:
    def test_headers_contain_bearer_token(self, monkeypatch):
        monkeypatch.setenv("API_TOKEN", "my-token")

        headers = build_headers()

        assert headers["Authorization"] == "Bearer my-token"
        assert headers["Content-Type"] == "application/json"
