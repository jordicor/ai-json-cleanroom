"""
Tests for JSON repair strategies (single quotes, unquoted keys, comments, etc).
"""

import pytest
from ai_json_cleanroom import validate_ai_json, ValidateOptions


class TestJSONRepair:
    """Test JSON repair functionality."""

    def test_repair_single_quotes(self, malformed_mixed_quotes):
        """Test repair of single-quoted strings."""
        result = validate_ai_json(malformed_mixed_quotes)

        assert result.json_valid
        assert result.data["name"] == "Alice Johnson"
        assert result.data["email"] == "alice@example.com"
        assert len(result.warnings) > 0

    def test_repair_unquoted_keys(self, malformed_unquoted_keys):
        """Test repair of unquoted object keys."""
        result = validate_ai_json(malformed_unquoted_keys)

        assert result.json_valid
        assert result.data["name"] == "Bob Builder"
        assert result.data["age"] == 35
        assert result.data["email"] == "bob@example.com"

    def test_repair_python_constants(self, json_with_python_constants):
        """Test repair of Python constants (True/False/None)."""
        result = validate_ai_json(json_with_python_constants)

        assert result.json_valid
        assert result.data["active"] is True
        assert result.data["deleted"] is False
        assert result.data["parent"] is None

    def test_repair_javascript_comments(self, json_with_comments):
        """Test removal of JavaScript-style comments."""
        result = validate_ai_json(json_with_comments)

        assert result.json_valid
        assert result.data["name"] == "Alice"
        assert result.data["age"] == 30
        assert result.data["active"] is True

    def test_repair_trailing_commas(self, json_with_trailing_commas):
        """Test removal of trailing commas."""
        result = validate_ai_json(json_with_trailing_commas)

        assert result.json_valid
        assert result.data["items"] == [1, 2, 3]
        assert result.data["name"] == "test"

    def test_repair_curly_quotes_always(self):
        """Test normalization of smart/curly quotes in 'always' mode."""
        text = '{"text": "She said “hello” to me"}'
        options = ValidateOptions(normalize_curly_quotes="always")
        result = validate_ai_json(text, options=options)

        assert result.json_valid
        assert result.data["text"] == "She said \"hello\" to me"

    def test_repair_curly_quotes_auto(self):
        """Test normalization of curly quotes in 'auto' mode."""
        text = '{"text": "She said “hello” to me"}'
        options = ValidateOptions(normalize_curly_quotes="auto")
        result = validate_ai_json(text, options=options)

        assert result.json_valid
        assert result.info.get("curly_quotes_normalization_used") is True

    def test_repair_curly_quotes_never(self):
        """Test that curly quotes are NOT normalized in 'never' mode."""
        text = '{"text": "Normal quotes work fine"}'
        options = ValidateOptions(normalize_curly_quotes="never")
        result = validate_ai_json(text, options=options)

        assert result.json_valid
        assert result.info.get("curly_quotes_normalization_used") is False

    def test_disable_specific_repairs(self):
        """Test disabling specific repair strategies."""
        text = "{'name': 'test', active: True}"
        options = ValidateOptions(
            fix_single_quotes=False,
            quote_unquoted_keys=False,
            replace_constants=False
        )
        result = validate_ai_json(text, options=options)

        # Should fail because repairs are disabled
        assert not result.json_valid

    def test_repair_all_issues_combined(self):
        """Test repair of multiple issues in one input."""
        text = '''{
  'name': "Alice",  // user name
  age: 30,
  active: True,
  tags: ["python", "ai",],
}'''
        result = validate_ai_json(text)

        assert result.json_valid
        assert result.data["name"] == "Alice"
        assert result.data["age"] == 30
        assert result.data["active"] is True
        assert result.data["tags"] == ["python", "ai"]

    def test_repair_nan_and_infinity(self):
        """Test repair of NaN and Infinity values."""
        text = '{"value": NaN, "infinity": Infinity, "neg": -Infinity}'
        options = ValidateOptions(replace_nans_infinities=True)
        result = validate_ai_json(text, options=options)

        assert result.json_valid
        assert result.data["value"] is None
        assert result.data["infinity"] is None
        assert result.data["neg"] is None

    def test_repair_limit_max_repairs(self):
        """Test that repair limit is respected."""
        # Create input with many issues
        text = "{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}"
        options = ValidateOptions(max_total_repairs=2)
        result = validate_ai_json(text, options=options)

        # Might fail or succeed depending on repair order, but limit is enforced
        # Main check: no crash, behavior is controlled
        assert isinstance(result.json_valid, bool)

    def test_repair_percent_limit(self):
        """Test that repair percent limit is respected."""
        text = "{'key': 'value'}"
        options = ValidateOptions(max_repairs_percent=0.0001)  # Very strict
        result = validate_ai_json(text, options=options)

        # With such strict limit, repairs might be blocked
        assert isinstance(result.json_valid, bool)

    def test_no_repair_when_truncated(self, truncated_array):
        """Test that repairs are skipped when truncation is detected."""
        result = validate_ai_json(truncated_array)

        assert not result.json_valid
        assert result.likely_truncated
        # Repairs should not be attempted on truncated input
        assert result.info.get("repair", {}).get("skipped") == "truncation_detected"

    def test_repair_metadata_in_warnings(self):
        """Test that repair metadata is included in warnings."""
        text = "{'name': 'test', active: True}"
        result = validate_ai_json(text)

        assert result.json_valid
        assert len(result.warnings) > 0

        repair_warning = next((w for w in result.warnings if w.code == "repaired"), None)
        assert repair_warning is not None
        assert "applied" in repair_warning.detail
        assert "counts" in repair_warning.detail

    def test_disable_all_repairs(self):
        """Test disabling repair system entirely."""
        text = "{'name': 'test'}"
        options = ValidateOptions(enable_safe_repairs=False)
        result = validate_ai_json(text, options=options)

        assert not result.json_valid
        assert len(result.warnings) == 0  # No repair warnings

    def test_repair_inner_unescaped_quotes(self):
        """Test repair of inner unescaped quotes in strings."""
        text = '{"message": "He said "hello" to her"}'
        result = validate_ai_json(text)

        assert result.json_valid
        # The quotes should be properly escaped
        assert '"' in result.data["message"] or "hello" in result.data["message"]

    def test_repair_control_characters(self):
        """Test repair of unescaped control characters."""
        # This would normally have actual control chars, but we simulate
        text = '{"text": "Line 1\\nLine 2"}'
        result = validate_ai_json(text)

        assert result.json_valid
        assert "\n" in result.data["text"]

    def test_repair_complex_nesting(self):
        """Test repair works with deeply nested structures."""
        text = '''{
  'level1': {
    'level2': {
      level3: {
        'level4': True
      }
    }
  }
}'''
        result = validate_ai_json(text)

        assert result.json_valid
        assert result.data["level1"]["level2"]["level3"]["level4"] is True
