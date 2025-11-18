"""
Basic usage examples for ai-json-cleanroom.

This script demonstrates common use cases for cleaning and validating
AI-generated JSON outputs.
"""

from ai_json_cleanroom import validate_ai_json, ValidateOptions

# Example 1: Clean mixed markdown and JSON
print("=" * 60)
print("Example 1: Extract from markdown")
print("=" * 60)

markdown_response = """Sure! Here's the user data you requested:

[Code fence with JSON]
{
  'name': "Alice Johnson",
  active: True,
  "email": "alice@example.com",
  "age": 30,
}
[End fence]

Let me know if you need anything else!"""

result = validate_ai_json(markdown_response)
print(f"Valid: {result.json_valid}")
print(f"Data: {result.data}")
print(f"Source: {result.info.get('source')}")
print()

# Example 2: Repair common mistakes
print("=" * 60)
print("Example 2: Automatic repair")
print("=" * 60)

messy_json = """
{
  'name': 'Bob Smith',
  age: 25,
  // User is active
  active: True,
  tags: ["python", "ai",],
}
"""

result = validate_ai_json(messy_json)
print(f"Valid: {result.json_valid}")
print(f"Data: {result.data}")
if result.warnings:
    print(f"Repairs applied: {result.warnings[0].detail.get('applied')}")
print()

# Example 3: Schema validation
print("=" * 60)
print("Example 3: Schema validation")
print("=" * 60)

schema = {
    "type": "object",
    "required": ["name", "email"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"},
        "age": {"type": "integer", "minimum": 0, "maximum": 150}
    }
}

good_data = '{"name": "Charlie", "email": "charlie@test.com", "age": 28}'
bad_data = '{"name": "", "email": "invalid-email", "age": 200}'

result_good = validate_ai_json(good_data, schema=schema)
print(f"Good data valid: {result_good.json_valid}")

result_bad = validate_ai_json(bad_data, schema=schema)
print(f"Bad data valid: {result_bad.json_valid}")
print("Errors:")
for error in result_bad.errors:
    print(f"  - {error.path}: {error.message}")
print()

# Example 4: Truncation detection
print("=" * 60)
print("Example 4: Truncation detection")
print("=" * 60)

truncated = '{"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age":'

result = validate_ai_json(truncated)
print(f"Truncated: {result.likely_truncated}")
print(f"Reasons: {result.errors[0].detail.get('truncation_reasons') if result.errors else 'N/A'}")
print()

# Example 5: Path expectations
print("=" * 60)
print("Example 5: Path-based expectations")
print("=" * 60)

expectations = [
    {"path": "users[*].email", "required": True, "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"},
    {"path": "users[*].status", "in": ["active", "inactive"]}
]

data_with_users = """
{
  "users": [
    {"name": "Alice", "email": "alice@test.com", "status": "active"},
    {"name": "Bob", "email": "bob@test.com", "status": "inactive"}
  ]
}
"""

result = validate_ai_json(data_with_users, expectations=expectations)
print(f"Valid: {result.json_valid}")
print(f"All users have valid emails and status: {result.json_valid}")
print()

# Example 6: Custom options
print("=" * 60)
print("Example 6: Custom validation options")
print("=" * 60)

options = ValidateOptions(
    fix_single_quotes=True,
    quote_unquoted_keys=True,
    strip_js_comments=True,
    normalize_curly_quotes="auto",
    max_total_repairs=100
)

result = validate_ai_json(messy_json, options=options)
print(f"Valid: {result.json_valid}")
print(f"Backend used: {result.info.get('parse_backend')}")
print(f"Curly quotes normalized: {result.info.get('curly_quotes_normalization_used')}")
print()

print("=" * 60)
print("All examples completed!")
print("=" * 60)
