"""
Example: Handling streaming AI responses with ai-json-cleanroom.

This example demonstrates best practices for validating JSON
from streaming API responses.
"""

from ai_json_cleanroom import validate_ai_json, detect_truncation
import time


def simulate_streaming_chunks(json_data: str, chunk_size: int = 10):
    """Simulate streaming API response by yielding chunks."""
    for i in range(0, len(json_data), chunk_size):
        yield json_data[i:i + chunk_size]
        time.sleep(0.01)  # Simulate network delay


def example_basic_streaming():
    """Basic streaming collection and validation."""
    print("=" * 70)
    print("Example 1: Basic Streaming Collection")
    print("=" * 70 + "\n")

    # Simulate streaming response
    full_json = '''Sure! Here's the data:

```json
{
  "users": [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
  ],
  "count": 2
}
```

Done!'''

    print("Collecting streaming chunks...")
    chunks = []

    for chunk in simulate_streaming_chunks(full_json):
        chunks.append(chunk)
        print(".", end="", flush=True)

    full_output = ''.join(chunks)
    print(f"\n\nCollected {len(chunks)} chunks ({len(full_output)} bytes)")

    # Validate complete output
    result = validate_ai_json(full_output)

    if result.json_valid:
        print("OK: Valid JSON received from stream!")
        print(f"Users: {result.data['count']}")
        print(f"Source: {result.info.get('source')}")
    else:
        print(f"ERROR: Validation failed: {result.errors}")


def example_progressive_validation():
    """Progressive validation - check each chunk for completeness."""
    print("\n" + "=" * 70)
    print("Example 2: Progressive Validation (Check for Truncation)")
    print("=" * 70 + "\n")

    # Simulate streaming that gets cut off
    incomplete_json = '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name":'

    print("Simulating incomplete stream...")
    chunks = []

    for chunk in simulate_streaming_chunks(incomplete_json):
        chunks.append(chunk)
        current = ''.join(chunks)

        # Periodically check for truncation signals
        if len(chunks) % 10 == 0:
            is_truncated, reasons = detect_truncation(current)
            if is_truncated:
                print(f"\nWARNING: Truncation detected after {len(chunks)} chunks!")
                print(f"Reasons: {reasons}")
                break
        print(".", end="", flush=True)

    full_output = ''.join(chunks)
    print(f"\n\nCollected {len(chunks)} chunks")

    # Validate
    result = validate_ai_json(full_output)

    if result.likely_truncated:
        print("OK: Truncation correctly detected!")
        print(f"You can request retry with higher token limit")
    elif result.json_valid:
        print("OK: Complete valid JSON received")
    else:
        print(f"ERROR: Other validation errors: {result.errors}")


def example_buffer_validation():
    """Buffer-based validation for large streams."""
    print("\n" + "=" * 70)
    print("Example 3: Buffer-Based Validation (Large Streams)")
    print("=" * 70 + "\n")

    # Large JSON response
    large_json = '''{
  "data": [''' + ',\n    '.join([
        f'{{"id": {i}, "value": "item_{i}"}}'
        for i in range(100)
    ]) + '''
  ],
  "total": 100
}'''

    print(f"Streaming large JSON ({len(large_json)} bytes)...")

    buffer = []
    chunk_count = 0

    for chunk in simulate_streaming_chunks(large_json, chunk_size=50):
        buffer.append(chunk)
        chunk_count += 1

        # Show progress
        if chunk_count % 20 == 0:
            print(f"  Received {chunk_count} chunks ({len(''.join(buffer))} bytes)...")

    full_output = ''.join(buffer)
    print(f"\nOK: Stream complete: {chunk_count} chunks")

    # Validate
    result = validate_ai_json(full_output)

    if result.json_valid:
        print(f"OK: Valid JSON with {len(result.data['data'])} items")
        print(f"Total: {result.data['total']}")
    else:
        print(f"ERROR: Validation failed: {result.errors}")


def example_real_world_pattern():
    """Real-world pattern: OpenAI streaming with validation."""
    print("\n" + "=" * 70)
    print("Example 4: Real-World Streaming Pattern")
    print("=" * 70 + "\n")

    print("""
This pattern works with OpenAI, Anthropic, and other streaming APIs:

```python
from openai import OpenAI
from ai_json_cleanroom import validate_ai_json

client = OpenAI()

# Collect streaming chunks
chunks = []
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Generate user JSON"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        chunks.append(chunk.choices[0].delta.content)

# Validate complete output
full_output = ''.join(chunks)
result = validate_ai_json(full_output)

if result.json_valid:
    print(f"Success: {result.data}")
elif result.likely_truncated:
    print("Truncated - retry with higher max_tokens")
else:
    print(f"Errors: {result.errors}")
```

Key points:
1. Collect ALL chunks first before validation
2. Check for truncation if validation fails
3. Use truncation detection to decide if retry is needed
4. Don't try to parse incomplete JSON mid-stream
    """)


def example_error_recovery():
    """Error recovery strategy for streaming."""
    print("\n" + "=" * 70)
    print("Example 5: Error Recovery Strategy")
    print("=" * 70 + "\n")

    def validate_stream(stream_data: str, attempt: int = 1, max_attempts: int = 3):
        """Validate streaming data with retry logic."""
        result = validate_ai_json(stream_data)

        if result.json_valid:
            print(f"OK: Success on attempt {attempt}")
            return result.data

        if result.likely_truncated:
            print(f"WARNING: Attempt {attempt}: Truncated response")
            if attempt < max_attempts:
                print("   -> Recommendation: Increase max_tokens and retry")
                return None  # Signal for retry
            else:
                print("   -> Max attempts reached")
                return None

        # Other validation errors
        print(f"ERROR: Attempt {attempt}: Validation errors:")
        for error in result.errors:
            print(f"   - {error.message}")
        return None

    # Test cases
    test_cases = [
        ("Truncated", '{"data": [{"id": 1}, {"id": 2, "na'),
        ("Valid", '{"data": [{"id": 1}, {"id": 2}], "count": 2}'),
        ("Malformed", "{'data': [1, 2, 3,]}")
    ]

    for label, stream_data in test_cases:
        print(f"\nTesting {label}:")
        result = validate_stream(stream_data)
        if result:
            print(f"   Data: {result}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AI JSON Cleanroom - Streaming Response Examples")
    print("=" * 70 + "\n")

    # Run all examples
    example_basic_streaming()
    example_progressive_validation()
    example_buffer_validation()
    example_real_world_pattern()
    example_error_recovery()

    print("\n" + "=" * 70)
    print("All streaming examples complete!")
    print("=" * 70 + "\n")
