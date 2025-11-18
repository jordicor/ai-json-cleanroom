"""
Example: Using ai-json-cleanroom with Anthropic Claude API.

This example demonstrates handling Claude's chatty responses and
markdown-wrapped JSON outputs.
"""

import os
from ai_json_cleanroom import validate_ai_json

# Note: This example requires the anthropic package
# Install with: pip install anthropic

try:
    import anthropic
except ImportError:
    print("This example requires the 'anthropic' package.")
    print("Install with: pip install anthropic")
    exit(1)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define schema for validation
product_schema = {
    "type": "object",
    "required": ["name", "price", "category"],
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
        },
        "price": {
            "type": "number",
            "minimum": 0
        },
        "category": {
            "type": "string",
            "enum": ["electronics", "books", "clothing", "food", "other"]
        },
        "description": {
            "type": "string"
        },
        "in_stock": {
            "type": "boolean"
        }
    }
}


def generate_product_data(product_name: str, max_retries: int = 3):
    """Generate product data with Claude and validate."""
    prompt = f"Generate product information for '{product_name}' as a JSON object. Include name, price (numeric), category (must be one of: electronics, books, clothing, food, other), description, and in_stock (boolean)."

    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1}/{max_retries}")

        # Call Claude API
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract text from Claude's response
        raw_output = message.content[0].text
        print(f"Raw Claude output ({len(raw_output)} chars):")
        print(f"{raw_output[:150]}..." if len(raw_output) > 150 else raw_output)

        # Validate and clean with Cleanroom
        result = validate_ai_json(raw_output, schema=product_schema)

        if result.json_valid:
            print("\nOK: Valid JSON received!")
            print(f"Extraction source: {result.info.get('source')}")

            # Show any repairs that were applied
            if result.warnings:
                print("\nRepairs applied:")
                for warning in result.warnings:
                    if warning.code == "repaired":
                        repairs = warning.detail.get("applied", [])
                        for repair in repairs:
                            print(f"  - {repair}")

            return result.data

        # Handle errors
        if result.likely_truncated:
            print("\nWARNING: Response was truncated")
            print(f"Truncation reasons: {result.errors[0].detail.get('truncation_reasons', [])}")
            # Increase max_tokens for next attempt
            prompt = f"{prompt}\n\nIMPORTANT: Previous response was cut off. Please provide complete JSON."
        else:
            print(f"\nERROR: Validation failed with {len(result.errors)} errors:")
            for error in result.errors:
                print(f"   - {error.path}: {error.message}")

            # Build specific feedback
            error_messages = [f"- {e.path}: {e.message}" for e in result.errors]
            feedback = "\n".join(error_messages)
            prompt = f"{prompt}\n\nYour previous JSON had these issues:\n{feedback}\n\nPlease fix and return valid JSON."

    raise ValueError(f"Failed to generate valid product data after {max_retries} attempts")


def extract_from_chatty_claude():
    """Demonstrate extraction from Claude's verbose responses."""
    print("\n" + "=" * 70)
    print("Example: Handling Claude's Chatty Responses")
    print("=" * 70)

    # Simulate a typical Claude response (verbose with markdown)
    chatty_response = """I'll help you create that product data! Here's the information formatted as JSON:

```json
{
  "name": "Wireless Bluetooth Headphones",
  "price": 79.99,
  "category": "electronics",
  "description": "High-quality wireless headphones with noise cancellation and 30-hour battery life",
  "in_stock": true
}
```

This JSON structure includes all the key product information. The price is in USD, and the product is currently available in stock. Let me know if you need any adjustments!"""

    print("\nClaude's verbose response:")
    print(chatty_response)

    # Clean and validate
    result = validate_ai_json(chatty_response, schema=product_schema)

    if result.json_valid:
        print("\nOK: Successfully extracted JSON from chatty response!")
        print(f"\nExtracted data:")
        for key, value in result.data.items():
            print(f"  {key}: {value}")
        print(f"\nSource: {result.info.get('source')}")  # Will be 'code_fence'
    else:
        print(f"ERROR: Failed: {result.errors}")


def handle_streaming_response():
    """Demonstrate collecting and validating streaming Claude responses."""
    print("\n" + "=" * 70)
    print("Example: Handling Streaming Responses")
    print("=" * 70)

    print("\nStreaming product data from Claude...")

    # Collect streaming chunks
    chunks = []
    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Generate JSON for a product: Organic Green Tea. Include name, price (numeric), category (must be one of: electronics, books, clothing, food, other), description, and in_stock (boolean)."
            }
        ]
    ) as stream:
        for text in stream.text_stream:
            chunks.append(text)
            print(text, end="", flush=True)

    # Validate complete output
    full_output = ''.join(chunks)
    print(f"\n\nValidating complete response...")

    result = validate_ai_json(full_output, schema=product_schema)

    if result.json_valid:
        print("OK: Valid JSON received from stream!")
        print(f"\nProduct: {result.data['name']}")
        print(f"Price: ${result.data['price']}")
        print(f"Category: {result.data['category']}")
    elif result.likely_truncated:
        print("WARNING: Stream was truncated - increase max_tokens")
    else:
        print(f"ERROR: Validation errors: {result.errors}")


# Example usage
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AI JSON Cleanroom + Anthropic Claude Examples")
    print("=" * 70)

    # Example 1: Extract from chatty response
    extract_from_chatty_claude()

    # Example 2: Generate with retry logic
    print("\n" + "=" * 70)
    print("Example: Generate Product Data with Retry Logic")
    print("=" * 70)

    try:
        product_data = generate_product_data("Mechanical Keyboard")
        print("\n" + "=" * 70)
        print("Final validated product data:")
        print("=" * 70)
        for key, value in product_data.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"\nERROR: {e}")

    # Example 3: Handle streaming (requires API key)
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            handle_streaming_response()
        except Exception as e:
            print(f"\nWARNING: Streaming example error: {e}")
    else:
        print("\nWARNING: Set ANTHROPIC_API_KEY to run streaming example")

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70 + "\n")
