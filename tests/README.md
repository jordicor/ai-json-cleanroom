# Test Suite for AI JSON Cleanroom

Comprehensive test suite with unit tests, integration tests, and performance benchmarks.

## Quick Start

### Install Test Dependencies

```bash
# Install pytest
pip install pytest pytest-cov

# Install orjson for performance tests (optional)
pip install orjson
```

### Run All Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest --cov=ai_json_cleanroom tests/

# Run specific test file
pytest tests/test_extraction.py

# Run specific test class
pytest tests/test_repair.py::TestJSONRepair

# Run specific test
pytest tests/test_repair.py::TestJSONRepair::test_repair_single_quotes
```

### Run Performance Benchmark

```bash
# Run the json vs orjson benchmark
python tests/benchmark_json_vs_orjson.py
```

## Test Organization

### Core Test Modules

- **`test_json_engine.py`** - Tests for JSON parsing engine (orjson/stdlib)
  - Parse simple and complex JSON
  - Unicode handling
  - Large numbers
  - Empty structures
  - Bytes/bytearray input

- **`test_extraction.py`** - Tests for JSON extraction from mixed text
  - Markdown code fences (```json)
  - Generic code fences (```)
  - Balanced block extraction
  - Chatty AI responses
  - Multiple JSON blocks

- **`test_repair.py`** - Tests for JSON repair strategies
  - Single quote fixing
  - Unquoted key quoting
  - Python constant replacement (True/False/None)
  - JavaScript comment removal
  - Trailing comma removal
  - Smart quote normalization
  - Repair limits and safeguards

- **`test_truncation.py`** - Tests for truncation detection
  - Truncated arrays and objects
  - Various truncation patterns
  - Ellipsis detection
  - Unterminated strings
  - Unbalanced braces/brackets

- **`test_schema_validation.py`** - Tests for JSON Schema validation
  - Type validation
  - Required fields
  - String constraints (minLength, maxLength, pattern)
  - Number constraints (minimum, maximum)
  - Array validation (minItems, maxItems, uniqueItems)
  - Enum and const
  - Nested objects
  - additionalProperties
  - anyOf combinator

- **`test_path_expectations.py`** - Tests for path-based validation
  - Simple and nested paths
  - Array wildcards (`[*]`)
  - Pattern matching
  - Enum-like constraints (`in`)
  - Numeric bounds
  - String length
  - Array size
  - Optional paths

### Performance Benchmarks

- **`benchmark_json_vs_orjson.py`** - Comprehensive performance comparison
  - Parse performance (simple and complex JSON)
  - Serialization performance
  - Full validation pipeline
  - Malformed JSON repair performance
  - Detailed timing reports

### Test Fixtures

Located in `tests/fixtures/`:

- **`simple.json`** - Simple JSON with basic types (~150 bytes)
- **`complex.json`** - Complex nested structure with arrays, objects (~3KB)
- **`malformed_mixed_quotes.json`** - JSON with mixed single/double quotes
- **`malformed_unquoted_keys.json`** - JSON with unquoted object keys
- **`truncated_array.json`** - Incomplete JSON array
- **`truncated_object.json`** - Incomplete JSON object

## Example Test Commands

### Run Tests by Category

```bash
# Test extraction functionality only
pytest tests/test_extraction.py -v

# Test repair functionality only
pytest tests/test_repair.py -v

# Test schema validation only
pytest tests/test_schema_validation.py -v
```

### Run Tests with Markers (if configured)

```bash
# Run only fast tests
pytest tests/ -m "not slow"

# Run integration tests
pytest tests/ -m integration
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=ai_json_cleanroom --cov-report=html tests/

# Open coverage report
# Windows: start htmlcov/index.html
# Linux/Mac: open htmlcov/index.html

# Generate terminal coverage report
pytest --cov=ai_json_cleanroom --cov-report=term-missing tests/
```

## Writing New Tests

### Test Structure

```python
"""
Description of test module.
"""

import pytest
from ai_json_cleanroom import validate_ai_json


class TestFeatureName:
    """Test suite for specific feature."""

    def test_specific_behavior(self):
        """Test description."""
        # Arrange
        input_data = '{"test": "value"}'

        # Act
        result = validate_ai_json(input_data)

        # Assert
        assert result.json_valid
        assert result.data["test"] == "value"
```

### Using Fixtures

```python
def test_with_fixture(self, simple_json, malformed_mixed_quotes):
    """Test using predefined fixtures from conftest.py."""
    result = validate_ai_json(malformed_mixed_quotes)
    assert result.json_valid
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input_str,expected", [
    ('{"valid": true}', True),
    ('{"valid": false}', False),
])
def test_multiple_cases(self, input_str, expected):
    """Test multiple cases with same logic."""
    result = validate_ai_json(input_str)
    assert result.data["valid"] == expected
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install pytest pytest-cov orjson
    pytest --cov=ai_json_cleanroom tests/
```

## Test Coverage Goals

- **Minimum target:** 80% code coverage
- **Ideal target:** 90%+ code coverage
- Focus on:
  - Edge cases
  - Error handling
  - Repair safeguards
  - Schema validation completeness

## Benchmark Results

Typical performance on modern hardware (Python 3.11):

| Operation | stdlib json | orjson | Speedup |
|-----------|------------|--------|---------|
| Parse simple | ~100 µs | ~28 µs | **3.6x** |
| Parse complex | ~450 µs | ~125 µs | **3.6x** |
| Serialize simple | ~85 µs | ~24 µs | **3.5x** |
| Serialize complex | ~380 µs | ~105 µs | **3.6x** |

Run `python tests/benchmark_json_vs_orjson.py` for results on your system.

## Troubleshooting Tests

### Import Errors

```bash
# Make sure ai_json_cleanroom is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%  # Windows
```

### Fixture Not Found

```bash
# Ensure fixtures directory exists
ls tests/fixtures/
```

### orjson Not Found (Benchmark)

```bash
# Install orjson for full benchmark
pip install orjson

# Or run benchmark without orjson (slower but works)
python tests/benchmark_json_vs_orjson.py
```

## Contributing Tests

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all existing tests pass
3. Add test for the new feature
4. Add test for edge cases
5. Update this README if adding new test files

```bash
# Before committing
pytest tests/ --cov=ai_json_cleanroom
```

---

**Questions?** Check the main README.md or open an issue.
