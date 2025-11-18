"""
Tests for path-based expectations validation.
"""

import pytest
from ai_json_cleanroom import validate_ai_json


class TestPathExpectations:
    """Test path-based validation expectations."""

    def test_simple_path_required(self):
        """Test simple path with required check."""
        expectations = [
            {"path": "name", "required": True}
        ]

        # Valid
        data = '{"name": "Alice", "age": 30}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Missing required path
        data = '{"age": 30}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_nested_path(self):
        """Test validation of nested paths."""
        expectations = [
            {"path": "user.email", "required": True, "type": "string"}
        ]

        # Valid
        data = '{"user": {"email": "alice@example.com", "name": "Alice"}}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Missing nested field
        data = '{"user": {"name": "Alice"}}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_array_wildcard(self):
        """Test wildcard for array items."""
        expectations = [
            {"path": "users[*].email", "required": True, "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"}
        ]

        # Valid - all users have valid emails
        data = '''{"users": [
            {"email": "alice@example.com"},
            {"email": "bob@example.com"}
        ]}'''
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Invalid - one user missing email
        data = '''{"users": [
            {"email": "alice@example.com"},
            {"name": "Bob"}
        ]}'''
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_pattern_validation(self):
        """Test pattern matching in expectations."""
        expectations = [
            {"path": "email", "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"}
        ]

        # Valid email
        data = '{"email": "alice@example.com"}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Invalid email
        data = '{"email": "not-an-email"}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_enum_in_expectations(self):
        """Test 'in' constraint (enum-like)."""
        expectations = [
            {"path": "status", "in": ["active", "inactive", "pending"]}
        ]

        # Valid
        data = '{"status": "active"}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Invalid value
        data = '{"status": "deleted"}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_numeric_bounds_in_expectations(self):
        """Test minimum and maximum in expectations."""
        expectations = [
            {"path": "age", "minimum": 0, "maximum": 150},
            {"path": "score", "minimum": 0, "maximum": 100}
        ]

        # Valid
        data = '{"age": 30, "score": 85.5}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Age too high
        data = '{"age": 200, "score": 85.5}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_string_length_in_expectations(self):
        """Test min_length and max_length in expectations."""
        expectations = [
            {"path": "username", "min_length": 3, "max_length": 20}
        ]

        # Valid
        data = '{"username": "alice"}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Too short
        data = '{"username": "al"}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

        # Too long
        data = '{"username": "this_is_a_very_long_username_that_exceeds_limit"}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_array_size_in_expectations(self):
        """Test min_items and max_items in expectations."""
        expectations = [
            {"path": "tags", "min_items": 1, "max_items": 5}
        ]

        # Valid
        data = '{"tags": ["python", "ai", "json"]}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Empty (violates min_items)
        data = '{"tags": []}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

        # Too many
        data = '{"tags": ["a", "b", "c", "d", "e", "f"]}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_optional_path(self):
        """Test non-required path validation."""
        expectations = [
            {"path": "optional_field", "required": False, "type": "string"}
        ]

        # Valid without field
        data = '{"other_field": 123}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Valid with field
        data = '{"optional_field": "value"}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Invalid type when present
        data = '{"optional_field": 123}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_multiple_expectations(self):
        """Test multiple expectations together."""
        expectations = [
            {"path": "users[*].email", "required": True, "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"},
            {"path": "users[*].status", "in": ["active", "inactive"]},
            {"path": "metadata.version", "pattern": r"^\d+\.\d+\.\d+$"}
        ]

        # Valid
        data = '''{
            "users": [
                {"email": "alice@example.com", "status": "active"},
                {"email": "bob@example.com", "status": "inactive"}
            ],
            "metadata": {"version": "1.2.3"}
        }'''
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

    def test_deeply_nested_path(self):
        """Test deeply nested path validation."""
        expectations = [
            {"path": "data.user.profile.address.city", "required": True, "type": "string"}
        ]

        # Valid
        data = '''{"data": {
            "user": {
                "profile": {
                    "address": {
                        "city": "San Francisco"
                    }
                }
            }
        }}'''
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

    def test_nested_array_wildcard(self):
        """Test nested array wildcards."""
        expectations = [
            {"path": "users[*].orders[*].total", "type": "number", "minimum": 0}
        ]

        # Valid
        data = '''{
            "users": [
                {"orders": [{"total": 100.0}, {"total": 50.0}]},
                {"orders": [{"total": 75.5}]}
            ]
        }'''
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Invalid - negative total
        data = '''{
            "users": [
                {"orders": [{"total": 100.0}, {"total": -10.0}]}
            ]
        }'''
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_equals_constraint(self):
        """Test exact value matching with equals."""
        expectations = [
            {"path": "api_version", "equals": "v2"}
        ]

        # Valid
        data = '{"api_version": "v2"}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Invalid
        data = '{"api_version": "v3"}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid

    def test_type_validation_in_expectations(self):
        """Test type checking in expectations."""
        expectations = [
            {"path": "count", "type": "integer"},
            {"path": "score", "type": "number"},
            {"path": "name", "type": "string"},
            {"path": "active", "type": "boolean"}
        ]

        # Valid
        data = '{"count": 10, "score": 95.5, "name": "test", "active": true}'
        result = validate_ai_json(data, expectations=expectations)
        assert result.json_valid

        # Invalid type
        data = '{"count": "ten", "score": 95.5, "name": "test", "active": true}'
        result = validate_ai_json(data, expectations=expectations)
        assert not result.json_valid
