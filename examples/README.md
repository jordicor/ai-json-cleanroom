# Examples - AI JSON Cleanroom

Practical, ready-to-run examples demonstrating real-world usage patterns with AI JSON Cleanroom.

## Quick Start

All examples are standalone Python scripts that can be run directly:

```bash
# Run any example
python examples/basic_usage.py
python examples/openai_integration.py
python examples/anthropic_claude.py
```

## Example Index

### 📚 **basic_usage.py** - Fundamentals
**Best for:** First-time users, learning core features

Demonstrates:
- Extract JSON from markdown code fences
- Automatic repair of common mistakes
- Schema validation
- Truncation detection
- Path-based expectations
- Custom validation options

```bash
python examples/basic_usage.py
```

**No API keys required** - uses mock data

---

### 🤖 **openai_integration.py** - OpenAI Integration
**Best for:** Using with GPT-3.5, GPT-4, GPT-4o models

Demonstrates:
- Integration with OpenAI Chat API
- Retry logic with validation feedback
- Schema validation for OpenAI responses
- Handling JSON mode quirks
- Error recovery strategies

```bash
# Requires: pip install openai
# Set: OPENAI_API_KEY environment variable
python examples/openai_integration.py
```

**Requirements:**
- `openai` package
- `OPENAI_API_KEY` environment variable

---

### 💬 **anthropic_claude.py** - Anthropic Claude Integration
**Best for:** Using with Claude 3, Claude 3.5 models

Demonstrates:
- Handling Claude's chatty/verbose responses
- Extracting JSON from markdown-wrapped output
- Streaming response collection
- Retry with Claude-specific feedback
- Schema validation for Claude outputs

```bash
# Requires: pip install anthropic
# Set: ANTHROPIC_API_KEY environment variable
python examples/anthropic_claude.py
```

**Requirements:**
- `anthropic` package
- `ANTHROPIC_API_KEY` environment variable

---

### 🌊 **streaming_responses.py** - Streaming Patterns
**Best for:** Working with streaming APIs (OpenAI, Anthropic, etc.)

Demonstrates:
- Collecting streaming chunks
- Progressive truncation detection
- Buffer-based validation
- Best practices for stream processing
- Error recovery for incomplete streams
- Real-world streaming patterns

```bash
python examples/streaming_responses.py
```

**No API keys required** - simulates streaming with delays

**Key patterns:**
```python
# Basic pattern
chunks = []
for chunk in stream:
    chunks.append(chunk.content)

full_output = ''.join(chunks)
result = validate_ai_json(full_output)
```

---

### 🔄 **retry_logic_advanced.py** - Intelligent Retries
**Best for:** Production systems needing robust error handling

Demonstrates:
- Smart retry strategies based on error types
- Exponential backoff
- Building improved prompts from validation errors
- Progressive refinement
- Custom retry decision logic
- Truncation-aware retries

```bash
python examples/retry_logic_advanced.py
```

**No API keys required** - uses mock generators

**Key concepts:**
- Detect *why* validation failed
- Provide specific feedback in retry prompts
- Different retry limits for different error types
- Graceful degradation

---

### 🔧 **custom_repair_hooks.py** - Domain-Specific Repairs
**Best for:** Advanced users with specific data transformation needs

Demonstrates:
- Creating custom repair hooks
- Domain-specific transformations
- Currency symbol removal
- Date format normalization
- Boolean string conversion
- Null variant handling
- Medical data normalization example

```bash
python examples/custom_repair_hooks.py
```

**No API keys required**

**Use cases:**
- Industry-specific data formats (medical, financial, etc.)
- Custom placeholder replacement
- Proprietary data conventions
- Legacy system integration

---

## Usage Patterns by Scenario

### Scenario 1: Simple Cleanup
**"I just need to parse AI output reliably"**

→ Start with `basic_usage.py`

### Scenario 2: Production API Integration
**"Integrating with OpenAI/Claude for production system"**

→ Use `openai_integration.py` or `anthropic_claude.py`
→ Add retry logic from `retry_logic_advanced.py`

### Scenario 3: Streaming Data
**"Processing streaming responses from AI APIs"**

→ Use `streaming_responses.py`

### Scenario 4: Complex Validation
**"Need strict schema compliance and retry on failure"**

→ Combine:
  - Schema validation from `basic_usage.py`
  - Retry logic from `retry_logic_advanced.py`
  - Error handling from integration examples

### Scenario 5: Custom Data Format
**"AI outputs domain-specific formats (medical, financial, etc.)"**

→ Use `custom_repair_hooks.py` as template
→ Create hooks for your specific patterns

---

## Common Patterns

### Pattern: Extract from Chatty AI

```python
from ai_json_cleanroom import validate_ai_json

# Works with any AI model's verbose output
chatty_response = """Sure! Here's the data:

```json
{"result": "success"}
```

Hope this helps!"""

result = validate_ai_json(chatty_response)
# result.data = {"result": "success"}
```

### Pattern: Retry with Feedback

```python
def generate_with_retry(prompt, schema, max_retries=3):
    for attempt in range(max_retries):
        ai_output = call_ai_api(prompt)
        result = validate_ai_json(ai_output, schema=schema)

        if result.json_valid:
            return result.data

        # Build feedback for next attempt
        if result.likely_truncated:
            prompt += "\n\nIMPORTANT: Previous response was cut off."
        else:
            errors = [f"- {e.message}" for e in result.errors]
            prompt += f"\n\nFix these:\n" + "\n".join(errors)

    raise ValueError("Failed after retries")
```

### Pattern: Stream + Validate

```python
# Collect streaming chunks
chunks = []
for chunk in streaming_response:
    chunks.append(chunk)

# Validate once complete
full_output = ''.join(chunks)
result = validate_ai_json(full_output)

if result.likely_truncated:
    # Request retry with higher max_tokens
    retry_with_higher_limit()
elif result.json_valid:
    # Success
    process(result.data)
```

### Pattern: Custom Domain Transform

```python
def repair_my_format(text, options):
    # Transform domain-specific patterns
    modified = text.replace("MY_NULL", "null")
    changes = text.count("MY_NULL")
    return modified, changes, {"my_repairs": changes}

options = ValidateOptions(
    custom_repair_hooks=[repair_my_format]
)

result = validate_ai_json(ai_output, options=options)
```

---

## Installation Requirements

### Core Library
```bash
# No dependencies (stdlib only)
pip install -e .
```

### Optional: Fast JSON Parsing
```bash
# Optional faster serialization; parsing still checks duplicate keys
pip install orjson
```

### For OpenAI Examples
```bash
pip install openai
export OPENAI_API_KEY="sk-..."
```

### For Anthropic Examples
```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## Customizing Examples

All examples are designed to be easily modified:

### Change API Model

```python
# OpenAI
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",  # ← Change this
    ...
)

# Anthropic
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # ← Change this
    ...
)
```

### Adjust Schema

```python
# Make stricter
schema = {
    "type": "object",
    "required": ["field1", "field2", "field3"],  # ← Add more
    "additionalProperties": False  # ← Disallow extras
}

# Make looser
schema = {
    "type": "object",
    "properties": {
        "field": {"type": "string"}
    }
    # No required, additionalProperties allowed by default
}
```

### Configure Repairs

```python
from ai_json_cleanroom import ValidateOptions

# Strict (minimal repairs)
options = ValidateOptions(
    fix_single_quotes=True,
    quote_unquoted_keys=False,
    strip_js_comments=False,
    max_total_repairs=10
)

# Permissive (more repairs)
options = ValidateOptions(
    fix_single_quotes=True,
    quote_unquoted_keys=True,
    strip_js_comments=True,
    max_total_repairs=500
)
```

---

## Testing Examples

Run examples to verify your setup:

```bash
# Test all examples (no API keys needed)
python examples/basic_usage.py
python examples/streaming_responses.py
python examples/retry_logic_advanced.py
python examples/custom_repair_hooks.py

# Test with API keys
python examples/openai_integration.py
python examples/anthropic_claude.py
```

---

## Contributing Examples

Have a useful pattern? Contribute an example!

Guidelines:
1. **Standalone** - Should run independently
2. **Documented** - Explain what it demonstrates
3. **Practical** - Show real-world usage
4. **Clear output** - Print results clearly
5. **Error handling** - Show how to handle failures

Example template:

```python
"""
Example: [Your Feature Name]

This example demonstrates [specific use case].
"""

from ai_json_cleanroom import validate_ai_json

def your_example():
    """Clear description."""
    print("=" * 70)
    print("Example: [Name]")
    print("=" * 70)

    # Your code here
    result = validate_ai_json(...)

    if result.json_valid:
        print("OK: Success!")
    else:
        print("ERROR: Failed")

if __name__ == "__main__":
    your_example()
```

---

## Need Help?

- **Getting started?** → Run `basic_usage.py`
- **Specific API?** → Check integration examples
- **Production patterns?** → See retry and streaming examples
- **Custom formats?** → Study `custom_repair_hooks.py`
- **Still stuck?** → Open an issue on GitHub

---

**Next Steps:**
1. Run `basic_usage.py` to understand fundamentals
2. Try integration example for your AI provider
3. Adapt patterns to your use case
4. Build your own examples!

Happy parsing!
