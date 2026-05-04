# Getting Started with GitHub Copilot

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey mihi-hun!

Mona here. I'm done preparing your exercise. Hope you enjoy! 💚

Remember, it's self-paced so feel free to take a break! ☕️

[![](https://img.shields.io/badge/Go%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/mihi-hun/skills-getting-started-with-github-copilot/issues/1)

---

## Testing

This project includes comprehensive tests for the FastAPI backend using pytest. Tests are organized by feature in the `tests/` directory.

### Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run with coverage report:**
```bash
pytest tests/ --cov=src --cov-report=html
```

**Run specific test file:**
```bash
pytest tests/test_activities.py -v
```

**Run tests matching a pattern:**
```bash
pytest tests/ -k "signup" -v
```

### Test Structure

Tests are organized by API endpoint functionality:

- **`tests/test_activities.py`** — Tests for the GET `/activities` endpoint
  - Retrieval of all activities
  - Response structure validation
  - Participant list verification

- **`tests/test_signup.py`** — Tests for the POST `/activities/{activity_name}/signup` endpoint
  - Successful student signup
  - Error handling (activity not found, already signed up)
  - Participant count updates
  - Multi-activity signup workflow

- **`tests/test_unregister.py`** — Tests for the DELETE `/activities/{activity_name}/unregister` endpoint
  - Successful student unregistration
  - Error handling (activity not found, not signed up)
  - Participant count updates
  - Complete signup/unregister workflow

### Test Fixtures

The `tests/conftest.py` file provides shared fixtures:

- **`client`** — FastAPI TestClient for making requests to the API
- **`reset_activities`** — Autouse fixture that resets the in-memory activities database before each test
- **`test_email`** — Email of a pre-registered student
- **`new_student_email`** — Email for testing new student signups

### CI/CD

Tests run automatically on:
- Push to the `main` branch
- Pull requests against `main`

The workflow (`.github/workflows/test.yml`) runs tests with coverage reporting and uploads coverage reports as artifacts.

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

