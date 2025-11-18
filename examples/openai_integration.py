"""
Example: Using ai-json-cleanroom with OpenAI API.

This example demonstrates how to use Cleanroom as a safety layer
when working with OpenAI's structured outputs.
"""

import os
from ai_json_cleanroom import validate_ai_json

# Note: This example requires the openai package
# Install with: pip install openai

try:
    from openai import OpenAI
except ImportError:
    print("This example requires the 'openai' package.")
    print("Install with: pip install openai")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define schema for validation
user_schema = {
    "type": "object",
    "required": ["name", "age", "email"],
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        },
        "email": {
            "type": "string",
            "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"
        },
        "occupation": {
            "type": "string"
        }
    },
    "additionalProperties": False
}

def generate_user_profile(name: str, age: int, max_retries: int = 3):
    """Generate a user profile with retry logic."""
    prompt = f"Generate a user profile for {name}, age {age}. Return valid JSON."

    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1}/{max_retries}")

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-5.1-2025-11-13",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates user profiles in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"}
        )

        raw_output = response.choices[0].message.content
        print(f"Raw output: {raw_output[:100]}...")

        # Validate and clean with Cleanroom
        result = validate_ai_json(raw_output, schema=user_schema)

        if result.json_valid:
            print("OK: Valid JSON received!")
            return result.data

        # Handle errors
        if result.likely_truncated:
            print("WARNING: Response was truncated")
            prompt = f"{prompt}\n\nIMPORTANT: Previous response was truncated. Please provide complete JSON."
        else:
            print(f"ERROR: Validation failed with {len(result.errors)} errors:")
            for error in result.errors:
                print(f"   - {error.path}: {error.message}")

            # Build feedback for retry
            error_messages = [f"- {e.path}: {e.message}" for e in result.errors]
            feedback = "\n".join(error_messages)
            prompt = f"{prompt}\n\nYour previous JSON had these issues:\n{feedback}\n\nPlease fix and return valid JSON."

    raise ValueError(f"Failed to generate valid profile after {max_retries} attempts")

# Example usage
if __name__ == "__main__":
    print("Generating user profile with OpenAI + Cleanroom validation...")

    try:
        user_data = generate_user_profile("Alice Johnson", 30)
        print("\n" + "=" * 60)
        print("Final validated data:")
        print("=" * 60)
        for key, value in user_data.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"\nERROR: {e}")
