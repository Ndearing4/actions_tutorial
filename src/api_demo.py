import os
from dotenv import load_dotenv

load_dotenv()


def get_api_config():
    """Load API configuration from environment variables.

    Raises ValueError if required variables are missing, so the app
    fails fast rather than making unauthenticated requests.
    """
    token = os.environ.get("API_TOKEN")
    base_url = os.environ.get("API_BASE_URL", "https://api.example.com")

    if not token:
        raise ValueError(
            "API_TOKEN is not set. "
            "Create a .env file locally or configure a GitHub repository secret."
        )

    return {"token": token, "base_url": base_url}


def build_headers():
    """Build HTTP request headers using the API token."""
    config = get_api_config()
    return {
        "Authorization": f"Bearer {config['token']}",
        "Content-Type": "application/json",
    }


if __name__ == "__main__":
    config = get_api_config()
    print(f"Base URL : {config['base_url']}")
    print(f"Token    : {config['token'][:4]}{'*' * (len(config['token']) - 4)}")
