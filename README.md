# AI JSON Cleanroom

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

**Your AI returns broken JSON? Put this in between.**

Works with any AI model: ChatGPT, Claude, Gemini, Llama. Zero setup.

Automatically extracts JSON from markdown/text, repairs common AI mistakes, validates structure.
Returns clean data when successful, detailed feedback for retries when not.

**Quick Links:** [Fast Track (2 min)](#fast-track-integration-in-3-steps) • [Why This Tool?](#why-you-need-this) • [Code Example](#quick-start) • [Install](#installation) • [Full Documentation ↓](#features)

---

## Fast Track: Integration in 3 Steps

**Want to start using this right away?** Here's how:

1. **Download** the `ai_json_cleanroom.py` file to your project
2. **Tell your AI coding assistant**:
   > "When I receive JSON from an AI response, process it through `validate_ai_json()` from `ai_json_cleanroom.py` first"
3. **Done.** Your AI assistant (ChatGPT, Claude, Copilot, Cursor) will handle the integration

Ready in 2 minutes. Works immediately.

[Show me the code →](#quick-start) • [Why do I need this? →](#why-you-need-this)

---

## Why You Need This

**The situation:** You request JSON from your AI. Sometimes you receive:

| What you get | What breaks |
|-------------|-------------|
| `Sure! Here's the JSON: {"name": "Alice"}` | Extra text crashes `json.loads()` |
| `{'name': 'Alice'}` | Python quotes instead of JSON |
| `{"users": [{"id": 1}, {"i` | Truncated mid-response (token limit) |

**Current solution:** Try/catch blocks, regex patterns, manual fixes, repeated API calls.

**This tool:** Handles all cases automatically. One function call.

[See all common problems →](#the-problem-in-real-life)

---

## Installation

```bash
# Standard installation
git clone https://github.com/jordicor/ai-json-cleanroom.git
cd ai-json-cleanroom
pip install -e .

# Optional: 3.6x faster parsing
pip install orjson
```

**Ready.** Import and use: `from ai_json_cleanroom import validate_ai_json`

---

## Quick Start

```python
from ai_json_cleanroom import validate_ai_json

# Anything your AI returns (messy, wrapped, incomplete)
ai_response = "Here's your data:\n```json\n{'name': 'Alice', age: 30}  // Python-style syntax\n```\n"

# One line to clean and validate
result = validate_ai_json(ai_response)

if result.json_valid:
    print(result.data)  # Clean: {'name': 'Alice', 'age': 30}
else:
    print(result.errors)  # Detailed error information
```

**Done.** No configuration needed. It works out of the box.

Check `result.warnings` to see what was fixed automatically.

---

### What Just Happened?

The cleaner automatically:
- Found the JSON inside markdown code fence
- Fixed single quotes to double quotes
- Added quotes to the unquoted key `age`
- Removed the inline comment
- Validated the final structure

Processing time: ~1ms. Zero configuration required.

**Useful tip:** Check `result.likely_truncated` to detect when the AI hit its token limit. This saves unnecessary retry API calls.

---

## You're All Set

**That's everything you need.** The tool works immediately with smart defaults.

Everything below is optional documentation for:
- Understanding how the tool works internally
- Advanced configuration options
- Framework integrations (LangChain, Instructor, etc.)
- Your AI assistant to read and understand the full API

**For most users:** The sections above are sufficient. Start building.

**Want to learn more?** Continue reading below.

**💡 Found this useful?** Star the repo ⭐ to help others discover it!

---

## Why This Tool Exists

If you've worked with AI models, you know the frustration. You ask for JSON, and what do you get?

Sometimes it's wrapped in a friendly explanation. Sometimes it has Python-style single quotes. Sometimes it just... stops mid-array because it hit the token limit. And your `json.loads()` crashes. Again.

This is a common scenario when working with AI models. That's why AI JSON Cleanroom exists: to handle the messy reality of AI outputs so you can focus on building.

## The Problem (In Real Life)

Here's what actually happens when you ask an AI model for JSON:

| Your Request | What You Expect | What You Actually Get | Why It Happens |
|--------------|-----------------|----------------------|----------------|
| "Return user data as JSON" | `{"name": "Alice"}` | `Sure! Here's the JSON:`<br>`{"name": "Alice"}` | AI models are trained to be helpful and conversational |
| "Give me valid JSON only" | `{"active": true}` | `{'active': True}` | Model confusion between Python and JSON syntax |
| "Return a large dataset" | Complete JSON | `{"data": [{"id": 1}, {"id": 2}, {"i` | Token limit reached mid-generation |
| "Format as JSON object" | `{"text": "He said \"hi\""}` | `{"text": "He said "hi""}` | Improper quote escaping |
| "Output JSON with comments" | Valid JSON | `{name: "Alice", age: 30}` | JavaScript object literal syntax |
| "Generate configuration" | Clean JSON | `{"items": [1, 2, 3,]}` | Trailing commas (valid in JS/Python, not JSON) |

**Why existing solutions fall short:**

- **`json.loads()`**: Throws exceptions on malformed input, no context provided
- **LangChain parsers**: Validate structure but don't repair common AI mistakes
- **Instructor/Pydantic**: Excellent for type mapping, but require clean JSON first
- **Custom regex**: Brittle, incomplete, and maintenance-heavy

---

## The Solution

AI JSON Cleanroom is a production-ready, zero-dependency (stdlib only) JSON cleaner designed specifically for AI outputs. It acts as a **post-processing layer** that extracts, repairs, validates, and provides structured feedback.

**Key Benefits:**

- **Smart Extraction** - Automatically finds JSON in markdown, code blocks, or mixed text
- **Conservative Repair** - Fixes common AI mistakes without corrupting your data
- **Truncation Detection** - Knows when output was cut off (saves you API calls!)
- **Schema Validation** - Validate structure with JSON Schema or simple path rules
- **Non-Throwing API** - Always returns a result, never crashes your pipeline
- **Performance** - 3.6x faster parsing with optional `orjson` (but works fine without it)
- **Granular Control** - Choose exactly which repairs to apply (or use smart defaults)

> **Pro Tip:** Start with default options - they handle 95% of AI quirks. Only customize when you hit specific issues.

---

## When Does This Tool Help You?

### You're in the right place if:

**Your code crashes when parsing the AI's response**
- You ask the AI for JSON data
- The AI returns something that *looks* like JSON
- But `json.loads()` throws an error and your script stops
- You're tired of try-except blocks that don't tell you what went wrong

**The AI wraps the JSON in extra text**
- Instead of just `{"name": "Alice"}`, you get: "Here's the data you requested: `{"name": "Alice"}` Let me know if you need anything else!"
- Your parser fails because there's text before/after the actual JSON
- You've tried telling the AI "return ONLY JSON" but it keeps adding explanations anyway
- You don't want to write regex patterns to extract the JSON part

**The response is incomplete and you don't know why**
- Sometimes the JSON just... stops: `{"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "a`
- Your code crashes with confusing error messages
- You retry multiple times, same problem
- **The issue**: AIs have a maximum length they can respond (token limit). When they hit it, they stop mid-sentence
- This tool detects when JSON was cut off and tells you immediately - so you know to ask for a shorter response or increase the limit

**The JSON "looks right" but still fails to parse**
- You can see the data structure clearly
- But Python complains about "invalid syntax" or "expecting property name"
- **Common hidden issues**:
  - Mixed quote styles: `{'name': "Alice"}` (Python allows both, JSON only allows double quotes)
  - Trailing commas: `[1, 2, 3,]` (JavaScript/Python allow this, JSON doesn't)
  - Comments: `{"name": "Alice" // her name}` (many languages allow comments, JSON doesn't)
  - Python booleans: `{"active": True}` instead of `{"active": true}`
- These are easy mistakes for AIs to make, and hard to spot by eye

**You're working with different AI models or providers**
- GPT has different quirks than Claude, which has different quirks than Llama
- Each one "breaks" JSON in its own special way
- You don't want to write different parsing logic for each model
- You want one solution that handles them all

**You need to know what was changed**
- When something gets fixed automatically, you want to know what was fixed
- Not just "it works now" without explanation
- You might need to log the changes or decide if they're acceptable
- Every fix this tool makes is reported, so you stay in control

**You want something that just works**
- No spending hours reading documentation to set it up
- No installing a dozen dependencies that might conflict with your other packages
- You just want to fix your JSON parsing problem and move on with your project
- Single file, drop it in your project, import it, done

### What this tool does

It takes the messy response from an AI and:
1. **Finds** the JSON part (even if wrapped in text or markdown code blocks)
2. **Fixes** common issues (quotes, commas, Python vs JSON syntax)
3. **Tells you** if the response was cut off (so you don't waste time retrying)
4. **Reports** everything it changed (so you know what happened)
5. **Validates** the structure (optional - you can define rules for what fields should exist)

Think of it as a safety net between the AI's response and your code. The AI does its best, but when it messes up, this catches it.

---

## Features

### 1. Smart Extraction

Automatically extracts JSON from various formats:

```python
from ai_json_cleanroom import validate_ai_json

# From markdown code fence (AI models often wrap JSON in ```json blocks)
markdown_output = 'Here is the data:\n```json\n{"status": "success"}\n```\n'
result = validate_ai_json(markdown_output)
# Extracted: {"status": "success"}

# From mixed text
mixed_output = 'The result is {"status": "success"} as requested.'
result = validate_ai_json(mixed_output)
# Extracted: {"status": "success"}

# From generic code fence
generic_fence = '```\n{"status": "success"}\n```'
result = validate_ai_json(generic_fence)
# Extracted: {"status": "success"}
```

### 2. Conservative Repair

Fixes common AI mistakes with configurable safeguards:

```python
from ai_json_cleanroom import validate_ai_json, ValidateOptions

# Single quotes → double quotes
result = validate_ai_json("{'name': 'Alice'}")
# Repaired: {"name": "Alice"}

# Python constants → JSON
result = validate_ai_json('{"active": True, "value": None}')
# Repaired: {"active": true, "value": null}

# Unquoted keys → quoted keys
result = validate_ai_json('{name: "Alice", age: 30}')
# Repaired: {"name": "Alice", "age": 30}

# Comments removal
result = validate_ai_json('''
{
  "name": "Alice",  // user name
  /* age field */ "age": 30
}
''')
# Repaired: {"name": "Alice", "age": 30}

# Trailing commas
result = validate_ai_json('{"items": [1, 2, 3,]}')
# Repaired: {"items": [1, 2, 3]}

# Inner unescaped quotes
result = validate_ai_json('{"text": "She said "hello" to me"}')
# Repaired: {"text": "She said \"hello\" to me"}
```

**Safeguards:**
- Maximum modifications limit (default: 200 changes or 2% of input size)
- Disabled if truncation detected
- Incremental parse-check after each repair pass
- Detailed repair metadata in `result.info`

### 3. Truncation Detection

Identifies incomplete outputs before wasting retries:

```python
from ai_json_cleanroom import validate_ai_json

truncated = '{"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age":'

result = validate_ai_json(truncated)
print(result.likely_truncated)  # True
print(result.errors[0].message)
# "No JSON payload found in input."
print(result.errors[0].detail)
# {'truncation_reasons': ['unclosed_braces_or_brackets', 'suspicious_trailing_character']}
```

**Detection signals:**
- Unclosed strings
- Unbalanced braces/brackets
- Suspicious trailing characters (`,`, `:`, `{`, `[`)
- Ellipsis at end (`...`)

### 4. Schema Validation

Validate against JSON Schema subset:

```python
from ai_json_cleanroom import validate_ai_json

schema = {
    "type": "object",
    "required": ["name", "email"],
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "email": {
            "type": "string",
            "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        },
        "tags": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"}
        }
    },
    "additionalProperties": False
}

result = validate_ai_json(ai_output, schema=schema)

if not result.json_valid:
    for error in result.errors:
        print(f"{error.code}: {error.message} at {error.path}")
```

**Supported schema keywords:**
- Types: `object`, `array`, `string`, `number`, `integer`, `boolean`, `null`
- Object: `required`, `properties`, `patternProperties`, `additionalProperties`
- Array: `items`, `additionalItems`, `minItems`, `maxItems`, `uniqueItems`
- String: `minLength`, `maxLength`, `pattern`
- Number: `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `multipleOf`
- Combinators: `anyOf`, `oneOf`, `allOf`
- Constraints: `enum`, `const`, `allow_empty`

### 5. Path-Based Expectations

Validate specific paths with wildcard support:

```python
from ai_json_cleanroom import validate_ai_json

expectations = [
    {
        "path": "users[*].email",
        "required": True,
        "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"
    },
    {
        "path": "users[*].status",
        "required": True,
        "in": ["active", "pending", "inactive"]
    },
    {
        "path": "metadata.version",
        "required": True,
        "type": "string",
        "pattern": r"^\d+\.\d+\.\d+$"
    },
    {
        "path": "items[*].price",
        "minimum": 0,
        "type": "number"
    }
]

result = validate_ai_json(ai_output, expectations=expectations)
```

**Expectation options:**
- `path`: JSONPath-like with wildcards (`[*]` for arrays, `*` for object values)
- `required`: Whether path must exist (default: `True`)
- `type`: Expected type(s)
- `equals`: Exact value match
- `in`: Value must be in list
- `pattern`: Regex pattern for strings
- `min_length`, `max_length`: String length constraints
- `min_items`, `max_items`: Array size constraints
- `minimum`, `maximum`: Numeric bounds

### 6. Non-Throwing API

Always returns a `ValidationResult` - never crashes:

```python
from ai_json_cleanroom import validate_ai_json

result = validate_ai_json(any_input)

# Always safe to access
print(f"Valid: {result.json_valid}")
print(f"Truncated: {result.likely_truncated}")
print(f"Errors: {len(result.errors)}")
print(f"Warnings: {len(result.warnings)}")
print(f"Data: {result.data}")  # None if invalid
print(f"Info: {result.info}")  # Extraction/parsing metadata

# Structured error handling
for error in result.errors:
    print(f"Code: {error.code}")
    print(f"Path: {error.path}")
    print(f"Message: {error.message}")
    print(f"Detail: {error.detail}")
```

---

## Understanding the Configuration Options

Not sure which options to enable? This guide explains each repair strategy with practical examples.

### When to Use Each Repair Strategy

#### `fix_single_quotes` (Default: True)
**What it does:** Converts Python-style single quotes `'text'` to JSON double quotes `"text"`

**When to keep it ON:**
- Working with GPT models (they often mix Python/JSON syntax)
- Processing outputs from code-generation models
- General use - this is safe and commonly needed

**When to turn it OFF:**
- Your AI model never uses single quotes (rare)
- You're processing pure JSON from a non-AI source

**Example scenario:**
```python
# GPT often returns this mix:
input = "{'name': 'Alice', \"age\": 30}"  # Mixed quotes

# With fix_single_quotes=True:
# ✅ Becomes: {"name": "Alice", "age": 30}

# With fix_single_quotes=False:
# ❌ Parse fails on single quotes
```

#### `quote_unquoted_keys` (Default: True)
**What it does:** Adds quotes to JavaScript-style unquoted object keys

**When to keep it ON:**
- Working with models trained on JavaScript/TypeScript code
- Processing outputs that might include object literals
- Claude models (sometimes output JS-style objects)

**When to turn it OFF:**
- Strict JSON-only environment
- You want to detect and reject JS-style syntax

**Real-world example:**
```python
# Claude sometimes returns:
input = "{name: 'Alice', age: 30, active: true}"

# With quote_unquoted_keys=True:
# ✅ Becomes: {"name": "Alice", "age": 30, "active": true}
```

#### `replace_constants` (Default: True)
**What it does:** Converts Python/JS constants (`True`/`False`/`None`) to JSON (`true`/`false`/`null`)

**When to keep it ON:**
- Always, unless you have a specific reason not to
- Essential for Python-trained models

**Example:**
```python
# Models often mix languages:
input = '{"active": True, "deleted": False, "parent": None}'

# With replace_constants=True:
# ✅ Becomes: {"active": true, "deleted": false, "parent": null}
```

#### `strip_js_comments` (Default: True)
**What it does:** Removes JavaScript-style comments (`//` and `/* */`)

**When to keep it ON:**
- Models that explain their JSON with comments
- When processing configuration-style outputs

**Example:**
```python
input = '''
{
  "name": "Alice",  // user name
  /* age field */ "age": 30
}
'''
# ✅ Comments are safely removed
```

#### `normalize_curly_quotes` (Default: "always")
**What it does:** Handles smart/typographic quotes that break JSON parsing

**Options:**
- `"always"` - Convert smart quotes before parsing (safest)
- `"auto"` - Only convert if initial parse fails (balanced approach)
- `"never"` - Keep smart quotes as-is (when you want to preserve them)

**When to use each:**
- `"always"`: Default choice, handles copy-paste from documents
- `"auto"`: When performance matters and smart quotes are rare
- `"never"`: When processing content where quote style matters

**Example:**
```python
# From copy-paste or models trained on web text:
input = '{"text": "She said "hello" to me"}'  # Smart quotes

# With normalize_curly_quotes="always":
# ✅ Becomes: {"text": "She said \"hello\" to me"}
```

#### `enable_safe_repairs` (Default: True)
**What it does:** Master toggle for all repair strategies

**When to turn OFF:**
- You want to validate only, not repair
- Debugging to see raw parsing errors
- You have your own repair logic

#### `max_total_repairs` and `max_repairs_percent` (Defaults: 200, 0.02)
**What they do:** Safety limits to prevent over-correction

**When to increase:**
- Very messy outputs from older models
- Known high-error scenarios

**When to decrease:**
- You want stricter validation
- Suspicious of too many modifications

**Example configuration:**
```python
from ai_json_cleanroom import validate_ai_json, ValidateOptions

# For very messy outputs:
options = ValidateOptions(
    max_total_repairs=500,      # Allow more fixes
    max_repairs_percent=0.05    # Allow 5% of content to be modified
)

# For strict validation:
options = ValidateOptions(
    max_total_repairs=10,       # Minimal fixes only
    max_repairs_percent=0.001   # Less than 0.1% modifications
)
```

> 📝 **Note:** Start with defaults. They're battle-tested on thousands of real AI outputs. Only adjust if you have specific issues.

---

## Real-World Integrations

### With OpenAI Structured Outputs

#### The Challenge
Even with OpenAI's JSON mode, you're not guaranteed clean JSON. Why? The model might still:
- Wrap JSON in markdown code fences (happens ~15% of the time)
- Get truncated if your request is too large
- Add "helpful" explanatory text before or after

#### The Solution
Use Cleanroom as a safety net - it adds virtually no overhead when JSON is clean, but saves you when it's not:

```python
from openai import OpenAI
from ai_json_cleanroom import validate_ai_json

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5.1-2025-11-13",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
        {"role": "user", "content": "Generate user profile for Alice Johnson, age 30"}
    ],
    response_format={"type": "json_object"}
)

# Clean and validate the response
result = validate_ai_json(
    response.choices[0].message.content,
    schema={
        "type": "object",
        "required": ["name", "age"],
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0}
        }
    }
)

if result.json_valid:
    user_data = result.data
    print(f"User: {user_data['name']}, Age: {user_data['age']}")
else:
    # Use structured feedback for retry
    error_msg = "\n".join([e.message for e in result.errors])
    print(f"Validation failed:\n{error_msg}")
    # Optionally retry with feedback
```

#### Pro Tips:
**Token Limit Handling:** If you get truncation, Cleanroom tells you immediately - no need to waste API calls trying to parse incomplete JSON

**Retry Strategy:** Use the specific error messages for targeted retry prompts

**Cost Savings:** Check `result.likely_truncated` before retrying with higher token limits

### With Anthropic Claude

#### The Challenge
Claude loves to be helpful. It often:
- Wraps JSON in markdown code fences with explanations
- Adds conversational text before and after
- Uses varied quote styles depending on context

#### The Solution
Cleanroom handles Claude's chattiness automatically:

```python
import anthropic
from ai_json_cleanroom import validate_ai_json

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Generate a JSON object with user info for Alice, age 30"
        }
    ]
)

# Claude might return:
# "Here's the user data:\n```json\n{\"name\": \"Alice\", \"age\": 30}\n```\nLet me know if you need anything else!"

result = validate_ai_json(message.content[0].text)

if result.json_valid:
    print(f"Extracted data: {result.data}")
    print(f"Extraction source: {result.info['source']}")  # 'code_fence'
else:
    if result.likely_truncated:
        print("Response was truncated, increasing max_tokens...")
    else:
        print(f"Validation errors: {result.errors}")
```

### With LangChain

Use Cleanroom as a pre-processor before LangChain's parsers:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputParser
from ai_json_cleanroom import validate_ai_json, ValidateOptions
import json

# Initialize LangChain LLM
llm = ChatOpenAI(model="gpt-5.1", temperature=0)

# Create prompt
prompt = ChatPromptTemplate.from_template(
    "Generate a JSON object with information about {topic}. Return only valid JSON."
)

# Get LLM response
chain = prompt | llm
response = chain.invoke({"topic": "Python programming"})

# Step 1: Clean with ai-json-cleanroom
cleaned = validate_ai_json(
    response.content,
    options=ValidateOptions(
        enable_safe_repairs=True,
        extract_json=True
    )
)

if cleaned.json_valid:
    # Step 2: Pass to LangChain parser if needed
    parser = JsonOutputParser()
    # Convert back to string for LangChain parser
    structured = parser.parse(json.dumps(cleaned.data))
    print(structured)

    # Or use cleaned.data directly
    print(cleaned.data)
else:
    print(f"Cleaning failed: {cleaned.errors}")
    if cleaned.likely_truncated:
        print("Retry with higher max_tokens")
```

### With Instructor (Pydantic)

Cleanroom and Instructor work perfectly together - clean first, then map to Pydantic models:

```python
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
from ai_json_cleanroom import validate_ai_json

# Define Pydantic model
class User(BaseModel):
    name: str = Field(description="User's full name")
    age: int = Field(ge=0, le=150, description="User's age")
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    tags: list[str] = Field(default_factory=list)

# Get raw AI output (without Instructor's patching)
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-5.1",
    messages=[
        {"role": "user", "content": "Generate user info for Alice, 30 years old"}
    ]
)

raw_output = response.choices[0].message.content

# Step 1: Clean with ai-json-cleanroom
result = validate_ai_json(raw_output)

if result.json_valid:
    # Step 2: Map to Pydantic with Instructor
    try:
        user = User(**result.data)
        print(f"User: {user.name}, Age: {user.age}, Email: {user.email}")
    except Exception as e:
        print(f"Pydantic validation failed: {e}")
else:
    print(f"JSON cleaning failed: {result.errors}")
```

**Alternative with Instructor's client:**

```python
import instructor
from openai import OpenAI
from ai_json_cleanroom import validate_ai_json

# Patch OpenAI client with Instructor
client = instructor.from_openai(OpenAI())

# If Instructor fails, fallback to Cleanroom
try:
    user = client.chat.completions.create(
        model="gpt-5.1",
        response_model=User,
        messages=[{"role": "user", "content": "Generate user info"}]
    )
except Exception as e:
    # Fallback: get raw response and clean manually
    raw_response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[{"role": "user", "content": "Generate user info as JSON"}]
    )
    result = validate_ai_json(raw_response.choices[0].message.content)
    if result.json_valid:
        user = User(**result.data)
```

### With Streaming Outputs

Handle streaming responses by collecting chunks first:

```python
from openai import OpenAI
from ai_json_cleanroom import validate_ai_json

client = OpenAI()

# Collect streaming chunks
chunks = []
stream = client.chat.completions.create(
    model="gpt-5.1",
    messages=[{"role": "user", "content": "Generate user JSON"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        chunks.append(chunk.choices[0].delta.content)

# Validate complete output
full_output = ''.join(chunks)
result = validate_ai_json(full_output)

if result.likely_truncated:
    print("Stream was truncated, consider retrying with higher limits")
    print(f"Truncation reasons: {result.errors[0].detail.get('truncation_reasons')}")
elif result.json_valid:
    print(f"Valid JSON received: {result.data}")
else:
    print(f"Validation errors: {result.errors}")
```

### Retry Logic with Structured Feedback

Use validation errors to provide specific feedback for retries:

```python
from ai_json_cleanroom import validate_ai_json
import openai

def generate_with_retry(prompt, schema, max_retries=3):
    """Generate JSON with automatic retry on validation failure."""
    client = openai.OpenAI()

    for attempt in range(max_retries):
        response = client.chat.completions.create(
            model="gpt-5.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that returns valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        result = validate_ai_json(
            response.choices[0].message.content,
            schema=schema
        )

        if result.json_valid:
            return result.data

        # Build feedback for retry
        if result.likely_truncated:
            prompt = f"{prompt}\n\nIMPORTANT: Your previous response was truncated. Please ensure the complete JSON is returned."
        else:
            error_messages = [f"- {e.path}: {e.message}" for e in result.errors]
            feedback = "\n".join(error_messages)
            prompt = f"{prompt}\n\nYour previous JSON had these issues:\n{feedback}\n\nPlease fix these and return valid JSON."

    raise ValueError(f"Failed to generate valid JSON after {max_retries} attempts")

# Usage
schema = {
    "type": "object",
    "required": ["name", "email", "age"],
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string", "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"},
        "age": {"type": "integer", "minimum": 0}
    }
}

user_data = generate_with_retry(
    "Generate a user profile for Alice Johnson",
    schema=schema
)
print(user_data)
```

---

## Common Scenarios & Solutions

### Scenario 1: "My AI model keeps adding explanations"

**The Problem:** You explicitly ask for JSON only, but get:
```
I'll help you with that! Here's the JSON data:
{"status": "success"}
Let me know if you need anything else!
```

**The Solution:**
```python
# Cleanroom automatically extracts the JSON part
result = validate_ai_json(chatty_response)
print(result.data)  # Just the JSON: {"status": "success"}
print(result.info['source'])  # Tells you where it found it: 'balanced_block'
```

### Scenario 2: "Token limits are cutting off my JSON"

**The Problem:** Large responses get truncated:
```json
{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "na
```

**The Solution:**
```python
result = validate_ai_json(truncated_response)

if result.likely_truncated:
    # You know exactly what happened
    print("Response truncated - reasons:", result.errors[0].detail['truncation_reasons'])
    # Output: ['unclosed_braces_or_brackets', 'unterminated_string']

    # Smart retry with higher token limit
    retry_with_higher_limit()
```

### Scenario 3: "Mixed quote styles are breaking everything"

**The Problem:** Your AI model mixes Python and JSON syntax:
```python
output = "{'users': [\"Alice\", \"Bob\"], 'count': 2}"
```

**The Solution:**
```python
result = validate_ai_json(output)
# Automatically fixes to: {"users": ["Alice", "Bob"], "count": 2}
```

### Scenario 4: "I need to validate specific fields exist"

**The Problem:** You need certain fields but don't want full schema validation.

**The Solution:** Use path expectations:
```python
expectations = [
    {"path": "users[*].email", "required": True},
    {"path": "metadata.version", "pattern": r"^\d+\.\d+\.\d+$"}
]

result = validate_ai_json(ai_output, expectations=expectations)
# Validates that all users have emails and version is semver
```

### Scenario 5: "The JSON has comments and I want to keep the information"

**The Problem:** AI model adds helpful comments that contain important context:
```json
{
  "temperature": 0.7,  // Higher for creativity
  "max_tokens": 100   // Keep responses concise
}
```

**The Solution:**
```python
# First, extract with comments preserved to see them
raw_response = ai_output

# Clean for parsing
result = validate_ai_json(raw_response)

# The comments are removed for valid JSON
print(result.data)  # {"temperature": 0.7, "max_tokens": 100}

# If you need the comments, parse them separately from raw_response
```

### Scenario 6: "Different AI models fail in different ways"

**The Problem:** GPT uses Python syntax, Claude wraps in markdown, Gemini truncates.

**The Solution:** One configuration handles all:
```python
from ai_json_cleanroom import validate_ai_json

# Same code for ALL models
def clean_any_ai_output(output):
    result = validate_ai_json(output)  # Default options handle everything

    if result.json_valid:
        return result.data
    elif result.likely_truncated:
        raise ValueError("Output truncated - increase token limit")
    else:
        raise ValueError(f"Could not parse: {result.errors}")

# Works with GPT, Claude, Gemini, Llama, etc.
```

> ⚠️ **Important:** Truncation detection always runs first. If JSON is truncated, repairs are skipped to avoid corrupting partial data.

---

## Troubleshooting Guide

### "Why isn't my JSON being repaired?"

**Possible causes and solutions:**

1. **Truncation detected**
   - Cleanroom disables repairs for truncated input (safety measure)
   - Solution: Get complete output first, then retry

2. **Repair limit reached**
   - Default limit: 200 changes or 2% of input size
   - Solution: Increase limits if needed:
   ```python
   options = ValidateOptions(
       max_total_repairs=500,  # Raise limit
       max_repairs_percent=0.05  # Allow 5% modifications
   )
   ```

3. **Specific repair disabled**
   - Check your options - maybe `fix_single_quotes=False`?
   - Solution: Enable the specific repair you need

### "The parser says JSON is invalid but it looks fine to me"

**Common hidden issues:**
- Invisible Unicode characters (zero-width spaces, etc.)
- Smart quotes from copy-paste: `"text"` vs `"text"`
- Line breaks inside strings without proper escaping

**Diagnosis:**
```python
result = validate_ai_json(your_input, options=ValidateOptions(
    normalize_curly_quotes="always"  # Fixes smart quotes
))
print(result.errors)  # See specific character positions
```

### "It works with GPT but fails with Claude"

**Issue:** Different models have different quirks.

**Solution:** Check the extraction source:
```python
result = validate_ai_json(claude_output)
print(f"Found JSON in: {result.info['source']}")
# 'code_fence' = markdown block
# 'balanced_block' = found in text
# 'raw' = was already clean
```

### "Performance is slow with large outputs"

**Solutions:**
1. **Install orjson:** `pip install orjson` for 3.6x speedup
2. **Disable unnecessary repairs:**
   ```python
   options = ValidateOptions(
       strip_js_comments=False,  # If you never have comments
       normalize_curly_quotes="never"  # If you never have smart quotes
   )
   ```

### "I want to see what was changed"

**Solution:** Check warnings and info:
```python
result = validate_ai_json(messy_json)

# See all repairs applied
for warning in result.warnings:
    if warning.code == "repaired":
        print(f"Repairs applied: {warning.detail['applied']}")
        print(f"Number of changes: {warning.detail['counts']}")

# See extraction details
print(f"Extraction method: {result.info['source']}")
print(f"Parser used: {result.info['parse_backend']}")
```

### "Schema validation is rejecting valid data"

**Common issues:**
1. **Pattern escaping:** Remember to use raw strings for regex: `r"^\d+$"`
2. **Type mismatches:** JSON numbers include floats - use `"type": "number"` not `"integer"` unless you're sure
3. **Required fields:** Double-check field names are exact matches

**Debug approach:**
```python
# Start without schema to see actual structure
result = validate_ai_json(output)
print(json.dumps(result.data, indent=2))

# Then add schema gradually
schema = {"type": "object"}  # Start simple
# Add requirements one by one
```

---

## API Reference

### `validate_ai_json()`

Main validation function with comprehensive options.

```python
def validate_ai_json(
    input_data: Union[str, bytes, Dict, List],
    schema: Optional[Dict[str, Any]] = None,
    expectations: Optional[List[Dict[str, Any]]] = None,
    options: Optional[ValidateOptions] = None
) -> ValidationResult:
    """
    Validate AI output against JSON parseability, schema, and expectations.

    Args:
        input_data: String, bytes, or already-parsed dict/list
        schema: JSON Schema subset for validation
        expectations: List of path-based validation rules
        options: Configuration for parsing, extraction, and repair

    Returns:
        ValidationResult with json_valid, errors, warnings, data, and info
    """
```

### `ValidationResult`

Result object returned by `validate_ai_json()`.

```python
@dataclass
class ValidationResult:
    json_valid: bool              # True if parsing and validation succeeded
    likely_truncated: bool         # True if input appears truncated
    errors: List[ValidationIssue]  # Validation errors
    warnings: List[ValidationIssue] # Non-blocking warnings
    data: Optional[Union[Dict, List]] # Parsed JSON if valid, else None
    info: Dict[str, Any]          # Extraction/parsing metadata

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
```

**Metadata in `info`:**
- `source`: How JSON was found (`"raw"`, `"code_fence"`, `"balanced_block"`, `"object"`)
- `extraction`: Details about extraction process
- `parse_backend`: Which parser was used (`"orjson"` or `"json"`)
- `curly_quotes_normalization_used`: Whether typographic quotes were normalized
- `repair`: Details about applied repairs (if any)

### `ValidationIssue`

Individual validation error or warning.

```python
@dataclass
class ValidationIssue:
    code: ErrorCode               # Error type (enum)
    path: str                     # JSONPath where error occurred
    message: str                  # Human-readable description
    detail: Optional[Dict[str, Any]] # Additional context

    def to_dict(self) -> Dict[str, Any]:
        """Convert issue to dictionary."""
```

### `ValidateOptions`

Configuration for validation behavior.

```python
@dataclass
class ValidateOptions:
    # Extraction options
    strict: bool = False
    extract_json: bool = True
    allow_json_in_code_fences: bool = True
    allow_bare_top_level_scalars: bool = False
    tolerate_trailing_commas: bool = True
    stop_on_first_error: bool = False

    # Repair options
    enable_safe_repairs: bool = True
    allow_json5_like: bool = True  # Master toggle for JSON5-like repairs
    replace_constants: bool = True  # True/False/None → true/false/null
    replace_nans_infinities: bool = True  # NaN/Infinity → null
    max_total_repairs: int = 200
    max_repairs_percent: float = 0.02  # 2% of input size

    # Granular repair control (new in v1.1)
    normalize_curly_quotes: str = "always"  # "always"|"auto"|"never"
    fix_single_quotes: bool = True
    quote_unquoted_keys: bool = True
    strip_js_comments: bool = True

    # Custom repair hooks (new in v1.1)
    custom_repair_hooks: Optional[List[Callable]] = None
```

**Curly quotes normalization modes:**
- `"always"` (default): Normalize typographic quotes before parsing
- `"auto"`: Try parsing first; only normalize if parse fails
- `"never"`: Never normalize (preserves typographic quotes as-is)

### `ErrorCode`

Enumeration of validation error types.

```python
class ErrorCode(str, Enum):
    PARSE_ERROR = "parse_error"
    TRUNCATED = "truncated"
    MISSING_REQUIRED = "missing_required"
    TYPE_MISMATCH = "type_mismatch"
    ENUM_MISMATCH = "enum_mismatch"
    CONST_MISMATCH = "const_mismatch"
    NOT_ALLOWED_EMPTY = "not_allowed_empty"
    ADDITIONAL_PROPERTY = "additional_property"
    PATTERN_MISMATCH = "pattern_mismatch"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    MIN_ITEMS = "min_items"
    MAX_ITEMS = "max_items"
    MINIMUM = "minimum"
    MAXIMUM = "maximum"
    REPAIRED = "repaired"  # Warning: repair was applied
    # ... and more
```

### Helper Functions

```python
def extract_json_payload(
    text: str,
    options: Optional[ValidateOptions] = None
) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Extract JSON string from raw text.

    Returns:
        (payload, info) - Payload is raw JSON string or None
    """

def detect_truncation(s: str) -> Tuple[bool, List[str]]:
    """
    Heuristic truncation detector.

    Returns:
        (likely_truncated, reasons)
    """
```

---

## CLI Usage - Interactive Testing

The CLI isn't just for automation - it's perfect for debugging AI outputs during development.

### Quick Testing During Development

```bash
# Got weird output from your AI model? Test it immediately:
echo '{"name": "test"}' | python ai_json_cleanroom.py --input -

# Testing a saved AI response:
python ai_json_cleanroom.py --input gpt_response.txt

# See exactly what gets fixed:
python ai_json_cleanroom.py --input messy.json --verbose

# Output shows:
# Fixed 3 single-quoted strings
# Quoted 2 unquoted keys
# Normalized 4 curly quotes
# Removed 2 trailing commas

# Validate inline text
python ai_json_cleanroom.py --input '{"name": "Alice", "age": 30}'

# With JSON Schema validation
python ai_json_cleanroom.py --input response.txt --schema schema.json

# With expectations
python ai_json_cleanroom.py --input response.txt --expectations expectations.json
```

### Understanding Repair Behavior

```bash
# See what would be fixed without actually fixing:
python ai_json_cleanroom.py --input data.json --dry-run

# Test different repair strategies:
python ai_json_cleanroom.py --input data.json \
  --normalize-curly-quotes never \
  --no-fix-single-quotes \
  --verbose  # See the difference

# Process multiple files:
for file in responses/*.json; do
    echo "Processing $file..."
    python ai_json_cleanroom.py --input "$file" --output-clean
done
```

### Options

```bash
# Disable extraction (input must be pure JSON)
python ai_json_cleanroom.py --input data.json --no-extract

# Disable repair stage
python ai_json_cleanroom.py --input response.txt --no-repair

# Disable specific repair passes
python ai_json_cleanroom.py --input response.txt \
  --no-fix-single-quotes \
  --no-quote-unquoted-keys \
  --no-strip-comments

# Control curly quotes normalization
python ai_json_cleanroom.py --input response.txt \
  --normalize-curly-quotes auto  # always|auto|never

# Adjust repair limits
python ai_json_cleanroom.py --input response.txt \
  --max-repairs 500 \
  --repairs-percent 0.05

# Strict mode (stop on first error)
python ai_json_cleanroom.py --input response.txt --strict

# Control output format
python ai_json_cleanroom.py --input response.txt \
  --indent 4 \
  --ensure-ascii
```

### Output Format

The CLI outputs a JSON result with validation details:

```json
{
  "json_valid": true,
  "likely_truncated": false,
  "errors": [],
  "warnings": [
    {
      "code": "repaired",
      "path": "$",
      "message": "Input JSON was repaired by conservative heuristics.",
      "detail": {
        "applied": ["single_quoted_to_double_quoted", "replace_constants"],
        "counts": {
          "single_quoted_strings_converted": 3,
          "replace_constants": {"true_false_none": 2}
        }
      }
    }
  ],
  "data": {
    "name": "Alice",
    "age": 30,
    "active": true
  },
  "info": {
    "source": "code_fence",
    "parse_backend": "orjson",
    "curly_quotes_normalization_used": true
  }
}
```

---

## Advanced Configuration

### Granular Repair Control

Fine-tune which repair strategies to apply:

```python
from ai_json_cleanroom import validate_ai_json, ValidateOptions

options = ValidateOptions(
    # Master toggle (backward compatibility)
    allow_json5_like=True,

    # Individual repair passes (new in v1.1)
    fix_single_quotes=True,        # 'foo' → "foo"
    quote_unquoted_keys=True,      # {foo: 1} → {"foo": 1}
    strip_js_comments=True,        # Remove // and /* */ comments

    # Python/JS constants
    replace_constants=True,        # True/False/None → true/false/null
    replace_nans_infinities=True,  # NaN/Infinity → null

    # Curly quotes handling
    normalize_curly_quotes="auto", # "always"|"auto"|"never"

    # Safety limits
    max_total_repairs=200,
    max_repairs_percent=0.02
)

result = validate_ai_json(ai_output, options=options)
```

### Custom Repair Hooks

Add domain-specific repair logic:

```python
from ai_json_cleanroom import validate_ai_json, ValidateOptions

def my_custom_repair(text: str, options: ValidateOptions):
    """
    Custom repair function.

    Args:
        text: Current text being repaired
        options: ValidateOptions instance

    Returns:
        (modified_text, changes_count, metadata_dict)
    """
    modified = text
    changes = 0
    metadata = {}

    # Example: Replace specific domain patterns
    if "UNDEFINED" in modified:
        modified = modified.replace("UNDEFINED", "null")
        changes += modified.count("null") - text.count("null")
        metadata["undefined_replacements"] = changes

    return modified, changes, metadata

# Use custom hook
options = ValidateOptions(
    custom_repair_hooks=[my_custom_repair]
)

result = validate_ai_json(ai_output, options=options)

# Check if custom hook was applied
if "custom_hook:my_custom_repair" in result.info.get("repair", {}).get("applied", []):
    print("Custom repair was applied")
```

### Path Expectations with Wildcards

Validate complex nested structures:

```python
from ai_json_cleanroom import validate_ai_json

# Validate API response structure
expectations = [
    # All users must have email and it must match pattern
    {
        "path": "data.users[*].email",
        "required": True,
        "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"
    },

    # All users must have valid status
    {
        "path": "data.users[*].status",
        "required": True,
        "in": ["active", "pending", "inactive", "banned"]
    },

    # Nested array validation
    {
        "path": "data.users[*].orders[*].total",
        "type": "number",
        "minimum": 0
    },

    # Metadata version must be semver
    {
        "path": "metadata.api_version",
        "required": True,
        "pattern": r"^\d+\.\d+\.\d+$"
    },

    # Optional field with constraints when present
    {
        "path": "data.users[*].phone",
        "required": False,
        "pattern": r"^\+?[\d\s\-\(\)]+$"
    }
]

result = validate_ai_json(ai_output, expectations=expectations)

# Get specific path errors
for error in result.errors:
    if error.code == "path_not_found":
        print(f"Missing required path: {error.path}")
    elif error.code == "pattern_mismatch":
        print(f"Pattern mismatch at {error.path}: {error.message}")
```

### Handling Repairs Metadata

Track exactly what was repaired:

```python
from ai_json_cleanroom import validate_ai_json

result = validate_ai_json(messy_ai_output)

if result.warnings:
    for warning in result.warnings:
        if warning.code == "repaired":
            applied_repairs = warning.detail.get("applied", [])
            counts = warning.detail.get("counts", {})

            print("Applied repairs:")
            for repair in applied_repairs:
                print(f"  - {repair}")

            print("\nRepair counts:")
            for repair_type, count in counts.items():
                print(f"  - {repair_type}: {count}")

# Check repair info
if "repair" in result.info:
    repair_info = result.info["repair"]
    print(f"Total repairs applied: {len(repair_info.get('applied', []))}")

    if "skipped" in repair_info:
        print(f"Repairs skipped: {repair_info['skipped']}")
```

---

## Performance

### Benchmarks

Performance comparison with stdlib `json` vs `orjson`:

| Operation | stdlib json | orjson | Speedup |
|-----------|------------|--------|---------|
| Parse (simple) | 1.8 µs | 0.4 µs | **4.35x** |
| Parse (complex) | 20.2 µs | 8.3 µs | **2.42x** |
| Dump (simple) | 2.1 µs | 0.2 µs | **10.83x** |
| Dump (complex) | 23.8 µs | 2.2 µs | **11.04x** |

*Benchmarks on Python 3.11.5, Intel Core i9-11900K @ 3.50GHz*

### Repair Overhead

Repair operations add minimal overhead:

| Scenario | Time | Notes |
|----------|------|-------|
| Clean JSON (no repairs) | ~1 µs | Direct parse with orjson |
| Markdown extraction + parse | 84 µs | Full validation pipeline |
| Multiple repairs + parse | 218 µs | Fix quotes, constants, trailing commas |

*Average times from validation pipeline benchmarks (1000 iterations)*

### When to Use orjson

Install `orjson` for production use when:
- Processing high volumes of AI outputs
- Latency matters (API endpoints, real-time systems)
- Large JSON payloads (>10KB)

```bash
pip install orjson
```

The library automatically uses `orjson` when available, with transparent fallback to stdlib `json`.

---

## Should I Use This Tool?

### Quick Decision Guide

**Use AI JSON Cleanroom if you:**
- Work with any AI model (GPT, Claude, Gemini, Llama)
- Receive JSON wrapped in explanations or markdown
- Face token limit truncations
- Need detailed error messages for retries
- Want one solution for all AI quirks
- Value zero dependencies

**You might not need it if you:**
- Only work with clean, guaranteed JSON
- Control token generation completely (using guidance, lm-format-enforcer)
- Never hit token limits
- Your AI model never adds explanatory text

### Comparison with What You're Using Now

Instead of a complex feature matrix, here's what matters:

**Your Current Approach** → **With Cleanroom**
- `try: json.loads()` → Always get a result, never crashes
- Regex extraction → Automatic markdown/fence detection
- Custom retry logic → Structured errors for targeted retries
- "Is it truncated?" → Immediate truncation detection with reasons
- Multiple fix attempts → One call handles everything
- Scattered error handling → Unified validation pipeline

### Works Great With Other Tools

**Cleanroom + Instructor (Pydantic):**
```python
# 1. Clean with Cleanroom
result = validate_ai_json(ai_output)
# 2. Map to Pydantic model
if result.json_valid:
    user = UserModel(**result.data)
```

**Cleanroom + LangChain:**
```python
# Use as pre-processor before LangChain parsers
cleaned = validate_ai_json(response.content)
if cleaned.json_valid:
    chain_result = parser.parse(json.dumps(cleaned.data))
```

**Cleanroom + Your Custom Logic:**
```python
# Get clean data, then apply your business rules
result = validate_ai_json(ai_response)
if result.json_valid:
    your_custom_processor(result.data)
```

### The Bottom Line

If you've ever written code like this:
```python
# This is a common scenario...
try:
    data = json.loads(ai_output)
except:
    # Try to extract JSON with regex
    match = re.search(r'\{.*\}', ai_output, re.DOTALL)
    if match:
        try:
            # Fix quotes maybe?
            fixed = match.group().replace("'", '"')
            data = json.loads(fixed)
        except:
            # Give up
            raise ValueError("Can't parse AI output")
```

Then yes, you need this tool. It handles all of that (and much more) in one line:
```python
result = validate_ai_json(ai_output)  # Done.
```

---

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

If you consider this tool useful, please, *consider starring the repo! ⭐* to help others find it
