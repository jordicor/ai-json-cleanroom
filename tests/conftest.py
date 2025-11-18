"""
Pytest configuration and shared fixtures for ai-json-cleanroom tests.
"""

import pytest
import json
import os
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def simple_json(fixtures_dir):
    """Load simple.json fixture."""
    with open(fixtures_dir / "simple.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def complex_json(fixtures_dir):
    """Load complex.json fixture."""
    with open(fixtures_dir / "complex.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def malformed_mixed_quotes():
    """Return JSON with mixed single/double quotes."""
    return """{
  'name': "Alice Johnson",
  'age': 30,
  'email': "alice@example.com"
}"""


@pytest.fixture
def malformed_unquoted_keys():
    """Return JSON with unquoted keys."""
    return '{name: "Bob Builder", age: 35, email: "bob@example.com", active: true}'


@pytest.fixture
def truncated_array():
    """Return truncated JSON array."""
    return '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "na'


@pytest.fixture
def truncated_object():
    """Return truncated JSON object."""
    return '{"data": {"status": "ok", "count":'


@pytest.fixture
def markdown_wrapped_json():
    """Return JSON wrapped in markdown code fence."""
    return '''Sure! Here's the data:

```json
{
  "name": "Charlie",
  "email": "charlie@example.com"
}
```

Let me know if you need anything else!'''


@pytest.fixture
def json_with_comments():
    """Return JSON with JavaScript-style comments."""
    return '''{
  "name": "Alice",  // user name
  "age": 30,        /* current age */
  "active": true
}'''


@pytest.fixture
def json_with_trailing_commas():
    """Return JSON with trailing commas."""
    return '''{
  "items": [1, 2, 3,],
  "name": "test",
}'''


@pytest.fixture
def json_with_python_constants():
    """Return JSON with Python constants."""
    return '{"active": True, "deleted": False, "parent": None}'


@pytest.fixture
def ai_chatty_response():
    """Return typical chatty AI response with JSON."""
    return """I'll help you with that! Here's the user data you requested:

```json
{
  'name': "Alice Johnson",
  active: True,
  "email": "alice@example.com",
  "age": 30,
}
```

Hope this helps! Let me know if you need any modifications."""
