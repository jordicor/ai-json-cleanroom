"""
Example: Advanced retry logic patterns with ai-json-cleanroom.

This example demonstrates intelligent retry strategies based on
specific validation failures and truncation detection.
"""

from ai_json_cleanroom import validate_ai_json, ValidateOptions
import time
from typing import Optional, Dict, Any, Callable


class RetryStrategy:
    """Smart retry strategy based on validation results."""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.attempts = 0

    def should_retry(self, result) -> tuple[bool, str]:
        """Determine if retry is needed and why."""
        if result.json_valid:
            return False, "success"

        if result.likely_truncated:
            return True, "truncation"

        if result.errors:
            # Check error types
            error_codes = [e.code for e in result.errors]

            if "parse_error" in error_codes:
                return True, "parse_error"
            if "missing_required" in error_codes:
                return True, "missing_required"
            if "type_mismatch" in error_codes:
                return True, "type_mismatch"

        return True, "validation_failed"

    def build_retry_prompt(self, original_prompt: str, result, reason: str) -> str:
        """Build improved prompt based on failure reason."""
        feedback_parts = [original_prompt]

        if reason == "truncation":
            feedback_parts.append("\n\nIMPORTANT: Your previous response was cut off mid-way.")
            feedback_parts.append("Please ensure you return COMPLETE, valid JSON.")

        elif reason == "parse_error":
            feedback_parts.append("\n\nThe JSON you provided could not be parsed.")
            feedback_parts.append("Common issues:")
            feedback_parts.append("- Use double quotes, not single quotes")
            feedback_parts.append("- Remove trailing commas")
            feedback_parts.append("- Escape special characters")
            feedback_parts.append("\nPlease return valid, parseable JSON.")

        elif reason == "missing_required":
            missing_fields = [
                e.path for e in result.errors
                if e.code == "missing_required"
            ]
            feedback_parts.append(f"\n\nYour JSON is missing required fields: {', '.join(missing_fields)}")
            feedback_parts.append("Please include ALL required fields.")

        elif reason == "type_mismatch":
            type_errors = [
                f"  - {e.path}: {e.message}"
                for e in result.errors
                if e.code == "type_mismatch"
            ]
            feedback_parts.append("\n\nType mismatches found:")
            feedback_parts.extend(type_errors)
            feedback_parts.append("\nPlease correct the data types.")

        else:
            # Generic error feedback
            error_messages = [f"  - {e.path}: {e.message}" for e in result.errors]
            feedback_parts.append("\n\nValidation errors:")
            feedback_parts.extend(error_messages)
            feedback_parts.append("\nPlease fix these issues.")

        return '\n'.join(feedback_parts)

    def get_delay(self) -> float:
        """Calculate delay with exponential backoff."""
        return self.base_delay * (2 ** self.attempts)


def generate_with_smart_retry(
    generator_func: Callable[[str], str],
    prompt: str,
    schema: Optional[Dict[str, Any]] = None,
    expectations: Optional[list] = None,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Generate JSON with intelligent retry logic.

    Args:
        generator_func: Function that takes prompt and returns AI output
        prompt: Initial prompt
        schema: Optional JSON schema for validation
        expectations: Optional path-based expectations
        max_retries: Maximum retry attempts

    Returns:
        Validated JSON data

    Raises:
        ValueError: If all retries fail
    """
    strategy = RetryStrategy(max_retries=max_retries)
    current_prompt = prompt

    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1}/{max_retries}")

        # Generate AI output
        try:
            ai_output = generator_func(current_prompt)
        except Exception as e:
            print(f"ERROR: Generator error: {e}")
            if attempt < max_retries - 1:
                time.sleep(strategy.get_delay())
                continue
            raise

        # Validate
        result = validate_ai_json(ai_output, schema=schema, expectations=expectations)

        # Check if successful
        if result.json_valid:
            print(f"OK: Success on attempt {attempt + 1}!")
            return result.data

        # Determine retry strategy
        should_retry, reason = strategy.should_retry(result)

        if not should_retry or attempt == max_retries - 1:
            print(f"ERROR: Failed after {attempt + 1} attempts")
            print(f"Reason: {reason}")
            print(f"Errors: {[e.message for e in result.errors]}")
            raise ValueError(f"Validation failed: {reason}")

        # Build improved prompt for retry
        print(f"WARNING: Retry needed: {reason}")
        current_prompt = strategy.build_retry_prompt(prompt, result, reason)
        strategy.attempts = attempt + 1

        # Wait before retry
        delay = strategy.get_delay()
        print(f"Waiting {delay:.1f}s before retry...")
        time.sleep(delay)

    raise ValueError(f"Failed after {max_retries} attempts")


def example_truncation_retry():
    """Example: Retry on truncation."""
    print("=" * 70)
    print("Example 1: Retry on Truncation")
    print("=" * 70 + "\n")

    attempt_count = [0]

    def mock_generator(prompt: str) -> str:
        """Simulate AI that truncates on first attempt."""
        attempt_count[0] += 1
        if attempt_count[0] == 1:
            # First attempt: truncated
            return '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "na'
        else:
            # Retry: complete
            return '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], "count": 2}'

    try:
        data = generate_with_smart_retry(
            mock_generator,
            "Generate user list JSON",
            schema={
                "type": "object",
                "required": ["users", "count"],
                "properties": {
                    "users": {"type": "array"},
                    "count": {"type": "integer"}
                }
            }
        )
        print(f"\nFinal data: {data}")
        print(f"Total attempts: {attempt_count[0]}")
    except Exception as e:
        print(f"Error: {e}")


def example_missing_field_retry():
    """Example: Retry when required fields are missing."""
    print("\n" + "=" * 70)
    print("Example 2: Retry on Missing Required Fields")
    print("=" * 70 + "\n")

    attempt_count = [0]

    def mock_generator(prompt: str) -> str:
        """Simulate AI that forgets fields."""
        attempt_count[0] += 1
        if attempt_count[0] == 1:
            # First attempt: missing email
            return '{"name": "Alice", "age": 30}'
        else:
            # Retry: complete
            return '{"name": "Alice", "age": 30, "email": "alice@example.com"}'

    schema = {
        "type": "object",
        "required": ["name", "email", "age"],
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "age": {"type": "integer"}
        }
    }

    try:
        data = generate_with_smart_retry(
            mock_generator,
            "Generate user profile",
            schema=schema
        )
        print(f"\nFinal data: {data}")
        print(f"Total attempts: {attempt_count[0]}")
    except Exception as e:
        print(f"Error: {e}")


def example_type_mismatch_retry():
    """Example: Retry when types don't match."""
    print("\n" + "=" * 70)
    print("Example 3: Retry on Type Mismatch")
    print("=" * 70 + "\n")

    attempt_count = [0]

    def mock_generator(prompt: str) -> str:
        """Simulate AI that gets types wrong."""
        attempt_count[0] += 1
        if attempt_count[0] == 1:
            # First attempt: age as string
            return '{"name": "Alice", "age": "30", "email": "alice@example.com"}'
        else:
            # Retry: correct types
            return '{"name": "Alice", "age": 30, "email": "alice@example.com"}'

    schema = {
        "type": "object",
        "required": ["name", "age", "email"],
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string"}
        }
    }

    try:
        data = generate_with_smart_retry(
            mock_generator,
            "Generate user profile with correct types",
            schema=schema
        )
        print(f"\nFinal data: {data}")
        print(f"Total attempts: {attempt_count[0]}")
    except Exception as e:
        print(f"Error: {e}")


def example_progressive_refinement():
    """Example: Progressive refinement with feedback."""
    print("\n" + "=" * 70)
    print("Example 4: Progressive Refinement")
    print("=" * 70 + "\n")

    attempt_count = [0]
    responses = [
        # Attempt 1: Multiple issues
        "{'name': 'Alice', age: '30', 'tags': ['python', 'ai',]}",
        # Attempt 2: Fixed quotes and types, but trailing comma
        '{"name": "Alice", "age": 30, "tags": ["python", "ai",]}',
        # Attempt 3: Perfect
        '{"name": "Alice", "age": 30, "tags": ["python", "ai"]}'
    ]

    def mock_generator(prompt: str) -> str:
        """Return progressively better JSON."""
        idx = min(attempt_count[0], len(responses) - 1)
        attempt_count[0] += 1
        return responses[idx]

    schema = {
        "type": "object",
        "required": ["name", "age", "tags"],
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "tags": {"type": "array", "items": {"type": "string"}}
        }
    }

    try:
        data = generate_with_smart_retry(
            mock_generator,
            "Generate user profile",
            schema=schema,
            max_retries=5
        )
        print(f"\nFinal data: {data}")
        print(f"Total attempts: {attempt_count[0]}")
    except Exception as e:
        print(f"Error: {e}")


def example_custom_retry_logic():
    """Example: Custom retry decision logic."""
    print("\n" + "=" * 70)
    print("Example 5: Custom Retry Logic")
    print("=" * 70 + "\n")

    def custom_retry_func(result, attempt: int, max_attempts: int):
        """Custom retry decision function."""
        if result.json_valid:
            return False, None

        # Always retry truncation
        if result.likely_truncated:
            return True, "Response was truncated - requesting complete output"

        # Retry parse errors up to 2 times
        if any(e.code == "parse_error" for e in result.errors) and attempt < 2:
            return True, "Parse error - requesting better formatted JSON"

        # Don't retry schema validation errors after attempt 2
        if attempt >= 2:
            return False, "Max schema validation retries reached"

        return True, "Retrying with improved prompt"

    print("""
Custom retry logic allows you to:
- Set different retry limits for different error types
- Provide custom feedback messages
- Implement complex business rules
- Integrate with monitoring/logging

Example implementation shown above.
    """)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AI JSON Cleanroom - Advanced Retry Logic Examples")
    print("=" * 70 + "\n")

    # Run examples
    example_truncation_retry()
    example_missing_field_retry()
    example_type_mismatch_retry()
    example_progressive_refinement()
    example_custom_retry_logic()

    print("\n" + "=" * 70)
    print("All retry examples complete!")
    print("=" * 70 + "\n")
