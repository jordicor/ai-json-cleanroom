"""
Tests for JSON Schema validation.
"""

import pytest
from ai_json_cleanroom import validate_ai_json, ErrorCode


class TestSchemaValidation:
    """Test JSON Schema validation functionality."""

    def test_simple_type_validation(self):
        """Test basic type validation."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "active": {"type": "boolean"}
            }
        }

        # Valid data
        data = '{"name": "Alice", "age": 30, "active": true}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Invalid type
        data = '{"name": "Alice", "age": "thirty", "active": true}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.TYPE_MISMATCH for e in result.errors)

    def test_required_fields(self):
        """Test required field validation."""
        schema = {
            "type": "object",
            "required": ["name", "email"],
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"}
            }
        }

        # Valid with required fields
        data = '{"name": "Alice", "email": "alice@example.com"}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Missing required field
        data = '{"name": "Alice"}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.MISSING_REQUIRED for e in result.errors)

    def test_string_constraints(self):
        """Test string minLength, maxLength, and pattern."""
        schema = {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 20
                },
                "email": {
                    "type": "string",
                    "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"
                }
            }
        }

        # Valid
        data = '{"username": "alice", "email": "alice@example.com"}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Too short username
        data = '{"username": "al", "email": "alice@example.com"}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.MIN_LENGTH for e in result.errors)

        # Invalid email pattern
        data = '{"username": "alice", "email": "not-an-email"}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.PATTERN_MISMATCH for e in result.errors)

    def test_number_constraints(self):
        """Test number minimum and maximum."""
        schema = {
            "type": "object",
            "properties": {
                "age": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 150
                },
                "score": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 100.0
                }
            }
        }

        # Valid
        data = '{"age": 30, "score": 85.5}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Age too high
        data = '{"age": 200, "score": 85.5}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.MAXIMUM for e in result.errors)

        # Score negative
        data = '{"age": 30, "score": -10.0}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.MINIMUM for e in result.errors)

    def test_array_validation(self):
        """Test array items and size constraints."""
        schema = {
            "type": "object",
            "properties": {
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 5
                }
            }
        }

        # Valid
        data = '{"tags": ["python", "ai", "json"]}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Empty array (violates minItems)
        data = '{"tags": []}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.MIN_ITEMS for e in result.errors)

        # Too many items
        data = '{"tags": ["a", "b", "c", "d", "e", "f"]}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.MAX_ITEMS for e in result.errors)

    def test_enum_validation(self):
        """Test enum constraint."""
        schema = {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["active", "inactive", "pending"]
                }
            }
        }

        # Valid
        data = '{"status": "active"}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Invalid enum value
        data = '{"status": "deleted"}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.ENUM_MISMATCH for e in result.errors)

    def test_nested_object_validation(self):
        """Test validation of nested objects."""
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "required": ["name", "email"],
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"}
                    }
                }
            }
        }

        # Valid
        data = '{"user": {"name": "Alice", "email": "alice@example.com"}}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Missing nested required field
        data = '{"user": {"name": "Alice"}}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.MISSING_REQUIRED for e in result.errors)

    def test_additional_properties_false(self):
        """Test additionalProperties: false."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "additionalProperties": False
        }

        # Valid
        data = '{"name": "Alice"}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Has additional property
        data = '{"name": "Alice", "age": 30}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.ADDITIONAL_PROPERTY for e in result.errors)

    def test_anyof_validation(self):
        """Test anyOf combinator."""
        schema = {
            "type": "object",
            "properties": {
                "value": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "integer"}
                    ]
                }
            }
        }

        # String (valid)
        data = '{"value": "test"}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Integer (valid)
        data = '{"value": 42}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Boolean (invalid - not in anyOf)
        data = '{"value": true}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid

    def test_complex_schema(self, complex_json):
        """Test validation against complex schema."""
        schema = {
            "type": "object",
            "required": ["users", "metadata"],
            "properties": {
                "metadata": {
                    "type": "object",
                    "required": ["version"],
                    "properties": {
                        "version": {
                            "type": "string",
                            "pattern": r"^\d+\.\d+\.\d+$"
                        }
                    }
                },
                "users": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["id", "username", "profile"],
                        "properties": {
                            "id": {"type": "integer", "minimum": 1},
                            "username": {"type": "string", "minLength": 1},
                            "profile": {
                                "type": "object",
                                "required": ["email"],
                                "properties": {
                                    "email": {
                                        "type": "string",
                                        "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        import json
        result = validate_ai_json(json.dumps(complex_json), schema=schema)
        assert result.json_valid

    def test_unique_items(self):
        """Test uniqueItems constraint."""
        schema = {
            "type": "object",
            "properties": {
                "tags": {
                    "type": "array",
                    "uniqueItems": True
                }
            }
        }

        # Valid (unique items)
        data = '{"tags": ["python", "ai", "json"]}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Invalid (duplicate items)
        data = '{"tags": ["python", "ai", "python"]}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid

    def test_const_validation(self):
        """Test const constraint."""
        schema = {
            "type": "object",
            "properties": {
                "api_version": {
                    "const": "v2"
                }
            }
        }

        # Valid
        data = '{"api_version": "v2"}'
        result = validate_ai_json(data, schema=schema)
        assert result.json_valid

        # Invalid
        data = '{"api_version": "v3"}'
        result = validate_ai_json(data, schema=schema)
        assert not result.json_valid
        assert any(e.code == ErrorCode.CONST_MISMATCH for e in result.errors)
