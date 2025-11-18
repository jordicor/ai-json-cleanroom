"""
Tests for truncation detection.
"""

import pytest
from ai_json_cleanroom import validate_ai_json, detect_truncation


class TestTruncationDetection:
    """Test detection of truncated JSON outputs."""

    def test_detect_truncated_array(self, truncated_array):
        """Test detection of truncated array."""
        result = validate_ai_json(truncated_array)

        assert not result.json_valid
        assert result.likely_truncated
        assert len(result.errors) > 0

        # Check truncation reasons
        if result.errors:
            detail = result.errors[0].detail
            if detail and "truncation_reasons" in detail:
                reasons = detail["truncation_reasons"]
                assert "unclosed_braces_or_brackets" in reasons or \
                       "unterminated_string" in reasons or \
                       "suspicious_trailing_character" in reasons

    def test_detect_truncated_object(self, truncated_object):
        """Test detection of truncated object."""
        result = validate_ai_json(truncated_object)

        assert not result.json_valid
        assert result.likely_truncated

    def test_detect_truncation_function_directly(self):
        """Test direct usage of detect_truncation function."""
        truncated = '{"data": [{"id": 1}, {"id": 2}, {"i'
        is_truncated, reasons = detect_truncation(truncated)

        assert is_truncated
        assert len(reasons) > 0
        assert any(r in reasons for r in [
            "unclosed_braces_or_brackets",
            "unterminated_string",
            "suspicious_trailing_character"
        ])

    def test_truncated_at_colon(self):
        """Test detection of truncation at colon."""
        text = '{"status": "ok", "count":'
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_truncated_at_comma(self):
        """Test detection of truncation at comma."""
        text = '{"items": [1, 2, 3,'
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_truncated_at_opening_brace(self):
        """Test detection of truncation at opening brace."""
        text = '{"data": {'
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_truncated_at_opening_bracket(self):
        """Test detection of truncation at opening bracket."""
        text = '{"items": ['
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_truncated_with_ellipsis(self):
        """Test detection of truncation with ellipsis."""
        text = '{"users": [{"id": 1}, {"id": 2}...'
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_truncated_unterminated_string(self):
        """Test detection of unterminated string."""
        text = '{"name": "Alice", "bio": "She is a developer who'
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_not_truncated_valid_json(self):
        """Test that valid JSON is not flagged as truncated."""
        text = '{"status": "ok", "code": 200}'
        result = validate_ai_json(text)

        assert result.json_valid
        assert not result.likely_truncated

    def test_not_truncated_complete_structure(self):
        """Test that complete structures are not flagged."""
        text = '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], "count": 2}'
        result = validate_ai_json(text)

        assert result.json_valid
        assert not result.likely_truncated

    def test_truncation_with_unbalanced_braces(self):
        """Test truncation detection with unbalanced braces."""
        text = '{"a": {"b": {"c": "value"}'  # Missing closing braces
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_truncation_with_unbalanced_brackets(self):
        """Test truncation detection with unbalanced brackets."""
        text = '{"items": [1, 2, [3, 4, [5, 6'  # Missing closing brackets
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_truncation_reasons_detailed(self):
        """Test that truncation reasons are detailed and helpful."""
        test_cases = [
            ('{"test":', ["suspicious_trailing_character", "unclosed_braces_or_brackets"]),
            ('{"arr": [', ["suspicious_trailing_character", "unclosed_braces_or_brackets"]),
            ('{"a": 1, "b"', ["unclosed_braces_or_brackets"]),
            ('...', ["ellipsis_or_continuation_marker"]),
        ]

        for text, expected_reasons in test_cases:
            is_truncated, reasons = detect_truncation(text)
            if is_truncated:
                # At least one expected reason should be present
                assert any(er in reasons for er in expected_reasons), \
                    f"Expected one of {expected_reasons}, got {reasons} for '{text}'"

    def test_no_repair_on_truncated(self):
        """Test that repair is not attempted on truncated input."""
        text = '{"name": "test", "value":'
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated
        # Repair should be skipped
        repair_info = result.info.get("repair", {})
        if repair_info:
            assert repair_info.get("skipped") == "truncation_detected"

    def test_truncation_in_markdown_fence(self):
        """Test truncation detection within markdown code fence."""
        text = '''Here's the data:

```json
{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "na
```'''
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated

    def test_partial_key_truncation(self):
        """Test detection of truncation in the middle of a key."""
        text = '{"user_name": "Alice", "user_em'
        result = validate_ai_json(text)

        assert not result.json_valid
        assert result.likely_truncated
