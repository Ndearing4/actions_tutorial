# actions_tutorial

A git repo to demonstrate how to effectively utilize the GitHub Actions page.

## Project Overview

This repo contains a small Python library (`src/math_utils.py`) with NumPy-powered utility functions, a demo module (`src/api_demo.py`) showing how to handle secret tokens via environment variables, and a test suite that runs automatically via GitHub Actions on every push and pull request.

## Repository Structure

```
actions_tutorial/
├── .github/
│   └── workflows/
│       └── python-tests.yml   # GitHub Actions workflow
├── src/
│   ├── math_utils.py          # Demo Python module (NumPy)
│   └── api_demo.py            # Environment variable / secrets demo
├── tests/
│   ├── test_math_utils.py     # Pytest test suite
│   └── test_api_demo.py       # Tests for api_demo (uses monkeypatch)
├── .env.example               # Template for local environment variables
├── requirements.txt           # Python dependencies
└── README.md
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/actions_tutorial.git
   cd actions_tutorial
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env       # macOS / Linux
   copy .env.example .env     # Windows
   ```
   Open `.env` and replace the placeholder values with your real credentials.
   The `.env` file is listed in `.gitignore` so it will **never** be committed or pushed.

## Running Tests Locally

```bash
pytest tests/ -v
```

## What the Demo Code Does

`src/math_utils.py` exposes four functions that showcase NumPy:

| Function | Description |
|---|---|
| `descriptive_stats(data)` | Returns the mean, median, and standard deviation |
| `moving_average(data, window)` | Computes a simple moving average via convolution |
| `normalize(data)` | Min-max scales values to the [0, 1] range |
| `matrix_multiply(a, b)` | Multiplies two 2-D matrices |

`src/api_demo.py` demonstrates reading secrets from the environment:

| Function | Description |
|---|---|
| `get_api_config()` | Loads `API_TOKEN` and `API_BASE_URL` from env vars; raises if the token is missing |
| `build_headers()` | Returns HTTP headers with a Bearer token ready for authenticated requests |

## Environment Variables and Secrets

Many projects need secret values (API keys, database passwords, etc.) that should **never** be committed to version control. This repo demonstrates the two-part pattern: a local `.env` file for development and GitHub repository secrets for CI.

### Local development — the `.env` file

1. Copy the template: `cp .env.example .env`
2. Fill in real values in `.env`.
3. `.env` is already in `.gitignore`, so git will never track it.
4. Load the variables before running your code:
   ```bash
   # Option A — export manually
   export API_TOKEN="your-secret-token"      # macOS / Linux
   set API_TOKEN=your-secret-token           # Windows CMD
   $env:API_TOKEN = "your-secret-token"      # PowerShell

   # Option B — automatic (already set up in this project)
   # python-dotenv is included in requirements.txt and called in api_demo.py,
   # so your .env file is loaded automatically at import time.
   ```

### GitHub Actions — repository secrets

Your `.env` file doesn't exist in CI because it's gitignored. Instead, you store secrets in your GitHub repo's settings and pass them to the workflow as environment variables.

**Adding a secret:**

1. Go to your repository on GitHub.
2. Navigate to **Settings > Secrets and variables > Actions**.
3. Click **New repository secret**.
4. Enter a name (e.g. `API_TOKEN`) and the secret value, then click **Add secret**.

**Using a secret in a workflow:**

Secrets are exposed to workflow steps via the `secrets` context. In this repo's workflow the test step passes them as environment variables:

```yaml
- name: Run tests
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
    API_BASE_URL: ${{ secrets.API_BASE_URL }}
  run: pytest tests/ -v
```

> **Important notes:**
> - GitHub automatically masks secret values in workflow logs so they won't be printed.
> - Secrets are **not** available to workflows triggered by pull requests from forks (this prevents external contributors from stealing them).
> - Never `echo` or log a secret directly — even though GitHub masks them, it's a bad habit.
> - If a step doesn't need a secret, don't pass it. Keep the blast radius small.

## How the GitHub Actions Workflow Works

The workflow file lives at `.github/workflows/python-tests.yml`. Here is what it does:

1. **Triggers** — runs on every push to `main` and on every pull request targeting `main`.
2. **Matrix strategy** — tests against Python 3.10, 3.11, and 3.12 in parallel.
3. **Steps for each Python version:**
   - Checks out the repo (`actions/checkout@v4`)
   - Installs the matching Python version (`actions/setup-python@v5`)
   - Installs pip dependencies from `requirements.txt`
   - Runs the test suite with `pytest tests/ -v`

You can view the results in the **Actions** tab of your GitHub repository after pushing.
