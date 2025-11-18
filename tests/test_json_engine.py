"""
Tests for JSONEngine (orjson-first with stdlib fallback).
"""

import pytest
import sys
import json as stdlib_json

from ai_json_cleanroom import validate_ai_json, ValidateOptions


class TestJSONEngine:
    """Test the JSON parsing engine."""

    def test_simple_parse(self, simple_json):
        """Test parsing simple valid JSON."""
        json_str = stdlib_json.dumps(simple_json)
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert result.data == simple_json
        assert result.info.get("parse_backend") in ["orjson", "json"]

    def test_complex_parse(self, complex_json):
        """Test parsing complex nested JSON."""
        json_str = stdlib_json.dumps(complex_json)
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert result.data == complex_json
        assert len(result.data["users"]) == 3
        assert result.data["statistics"]["total_users"] == 3

    def test_orjson_backend_preference(self):
        """Test that orjson is preferred when available."""
        try:
            import orjson
            has_orjson = True
        except ImportError:
            has_orjson = False

        json_str = '{"name": "test", "value": 42}'
        result = validate_ai_json(json_str)

        if has_orjson:
            assert result.info.get("parse_backend") == "orjson"
        else:
            assert result.info.get("parse_backend") == "json"

    def test_unicode_handling(self):
        """Test proper handling of unicode characters."""
        json_str = '{"text": "Hello 世界", "symbol": "*"}'
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert result.data["text"] == "Hello 世界"
        assert result.data["symbol"] == "*"

    def test_large_numbers(self):
        """Test handling of large integer and float values."""
        json_str = '{"big_int": 9007199254740991, "big_float": 1.7976931348623157e+308, "small": 2.2250738585072014e-308}'
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert result.data["big_int"] == 9007199254740991
        assert isinstance(result.data["big_float"], float)
        assert isinstance(result.data["small"], float)

    def test_empty_structures(self):
        """Test parsing of empty objects and arrays."""
        test_cases = [
            ('{}', {}),
            ('[]', []),
            ('{"empty_obj": {}, "empty_arr": []}', {"empty_obj": {}, "empty_arr": []})
        ]

        for json_str, expected in test_cases:
            result = validate_ai_json(json_str)
            assert result.json_valid
            assert result.data == expected

    def test_null_values(self):
        """Test proper handling of null values."""
        json_str = '{"name": "test", "value": null, "nested": {"inner": null}}'
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert result.data["value"] is None
        assert result.data["nested"]["inner"] is None

    def test_boolean_values(self):
        """Test proper handling of boolean values."""
        json_str = '{"active": true, "deleted": false, "flags": [true, false, true]}'
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert result.data["active"] is True
        assert result.data["deleted"] is False
        assert result.data["flags"] == [True, False, True]

    def test_mixed_types_array(self):
        """Test arrays with mixed types."""
        json_str = '{"mixed": [1, "string", true, null, {"key": "value"}, [1, 2, 3]]}'
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert len(result.data["mixed"]) == 6
        assert result.data["mixed"][0] == 1
        assert result.data["mixed"][1] == "string"
        assert result.data["mixed"][2] is True
        assert result.data["mixed"][3] is None
        assert result.data["mixed"][4] == {"key": "value"}
        assert result.data["mixed"][5] == [1, 2, 3]

    def test_deeply_nested_structure(self):
        """Test handling of deeply nested structures."""
        json_str = '{"a": {"b": {"c": {"d": {"e": {"f": {"g": "deep"}}}}}}}'
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert result.data["a"]["b"]["c"]["d"]["e"]["f"]["g"] == "deep"

    def test_special_characters_in_strings(self):
        """Test strings with special characters."""
        json_str = r'{"text": "Line 1\nLine 2\tTabbed", "quote": "He said \"hello\""}'
        result = validate_ai_json(json_str)

        assert result.json_valid
        assert "\n" in result.data["text"]
        assert "\t" in result.data["text"]
        assert '"' in result.data["quote"]

    def test_bytes_input(self):
        """Test parsing from bytes input."""
        json_bytes = b'{"name": "test", "value": 42}'
        result = validate_ai_json(json_bytes)

        assert result.json_valid
        assert result.data == {"name": "test", "value": 42}

    def test_bytearray_input(self):
        """Test parsing from bytearray input."""
        json_bytearray = bytearray(b'{"name": "test", "value": 42}')
        result = validate_ai_json(json_bytearray)

        assert result.json_valid
        assert result.data == {"name": "test", "value": 42}

    def test_already_parsed_dict(self):
        """Test that already-parsed dict/list is accepted."""
        data = {"name": "test", "value": 42}
        result = validate_ai_json(data)

        assert result.json_valid
        assert result.data == data
        assert result.info.get("source") == "object"

    def test_already_parsed_list(self):
        """Test that already-parsed list is accepted."""
        data = [1, 2, 3, {"key": "value"}]
        result = validate_ai_json(data)

        assert result.json_valid
        assert result.data == data
        assert result.info.get("source") == "object"
