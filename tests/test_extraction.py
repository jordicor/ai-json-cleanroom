"""
Tests for JSON extraction from mixed text (markdown, code fences, etc).
"""

import pytest
from ai_json_cleanroom import validate_ai_json, extract_json_payload, ValidateOptions


class TestJSONExtraction:
    """Test extraction of JSON from various text formats."""

    def test_extract_from_markdown_json_fence(self, markdown_wrapped_json):
        """Test extraction from markdown ```json code fence."""
        result = validate_ai_json(markdown_wrapped_json)

        assert result.json_valid
        assert result.data["name"] == "Charlie"
        assert result.data["email"] == "charlie@example.com"
        assert result.info.get("source") == "code_fence"

    def test_extract_from_generic_fence(self):
        """Test extraction from generic ``` code fence."""
        text = '''Here's the data:

```
{"status": "ok", "code": 200}
```

Done!'''
        result = validate_ai_json(text)

        assert result.json_valid
        assert result.data["status"] == "ok"
        assert result.data["code"] == 200

    def test_extract_from_mixed_text(self):
        """Test extraction from text with JSON embedded."""
        text = 'The API returned {"success": true, "message": "Data saved"} which is good.'
        result = validate_ai_json(text)

        assert result.json_valid
        assert result.data["success"] is True
        assert result.data["message"] == "Data saved"
        assert result.info.get("source") == "balanced_block"

    def test_extract_array_from_text(self):
        """Test extraction of JSON array from mixed text."""
        text = 'The items are [{"id": 1}, {"id": 2}, {"id": 3}] in the list.'
        result = validate_ai_json(text)

        assert result.json_valid
        assert isinstance(result.data, list)
        assert len(result.data) == 3
        assert result.data[0]["id"] == 1

    def test_chatty_ai_response(self, ai_chatty_response):
        """Test extraction from typical chatty AI response."""
        result = validate_ai_json(ai_chatty_response)

        assert result.json_valid
        assert result.data["name"] == "Alice Johnson"
        assert result.data["active"] is True
        assert result.data["email"] == "alice@example.com"

    def test_multiple_json_blocks_takes_first(self):
        """Test that first valid JSON block is extracted when multiple exist."""
        text = '''First: {"type": "first", "value": 1}

Second: {"type": "second", "value": 2}'''
        result = validate_ai_json(text)

        assert result.json_valid
        assert result.data["type"] == "first"
        assert result.data["value"] == 1

    def test_nested_braces_in_strings(self):
        """Test extraction handles nested braces in strings correctly."""
        text = 'Data: {"message": "Use {braces} in text", "valid": true}'
        result = validate_ai_json(text)

        assert result.json_valid
        assert "{braces}" in result.data["message"]
        assert result.data["valid"] is True

    def test_extract_with_surrounding_text(self):
        """Test extraction with verbose surrounding text."""
        text = '''I understand you want user data. Let me provide that now.

Here is the JSON response you requested:

```json
{
  "user_id": 12345,
  "username": "alice",
  "status": "active"
}
```

I hope this helps! Let me know if you need any modifications to the data structure.'''
        result = validate_ai_json(text)

        assert result.json_valid
        assert result.data["user_id"] == 12345
        assert result.data["username"] == "alice"

    def test_no_extraction_when_strict(self):
        """Test that extraction is disabled in strict mode."""
        text = 'Result: {"status": "ok"}'
        options = ValidateOptions(strict=True, extract_json=False)
        result = validate_ai_json(text, options=options)

        # Should fail to parse because extraction is disabled
        assert not result.json_valid

    def test_extract_json_payload_function(self):
        """Test direct usage of extract_json_payload function."""
        text = '```json\n{"test": true}\n```'
        payload, info = extract_json_payload(text)

        assert payload is not None
        assert '{"test": true}' in payload
        assert info.get("source") == "code_fence"

    def test_extract_with_code_fence_language_variants(self):
        """Test extraction from code fences with various language tags."""
        test_cases = [
            '```json\n{"type": "json"}\n```',
            '```JSON\n{"type": "JSON"}\n```',
            '```javascript\n{"type": "js"}\n```',
            '```js\n{"type": "js"}\n```'
        ]

        for text in test_cases:
            result = validate_ai_json(text)
            assert result.json_valid
            assert "type" in result.data

    def test_balanced_block_extraction(self):
        """Test balanced block extraction without code fences."""
        text = 'The configuration is {"debug": false, "port": 8080, "host": "localhost"} for the server.'
        result = validate_ai_json(text)

        assert result.json_valid
        assert result.data["debug"] is False
        assert result.data["port"] == 8080
        assert result.info.get("source") == "balanced_block"

    def test_extract_from_html_like_content(self):
        """Test extraction from content with HTML-like tags."""
        text = '<response>{"status": "success", "data": [1, 2, 3]}</response>'
        result = validate_ai_json(text)

        assert result.json_valid
        assert result.data["status"] == "success"
        assert result.data["data"] == [1, 2, 3]

    def test_no_json_found(self):
        """Test behavior when no JSON is found in text."""
        text = "This is just plain text with no JSON at all."
        result = validate_ai_json(text)

        assert not result.json_valid
        assert len(result.errors) > 0

    def test_incomplete_code_fence(self):
        """Test handling of incomplete code fence."""
        text = '```json\n{"status": "ok"}\n'  # Missing closing ```
        result = validate_ai_json(text)

        # Should still extract the JSON
        assert result.json_valid
        assert result.data["status"] == "ok"
