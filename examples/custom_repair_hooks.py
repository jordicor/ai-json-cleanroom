"""
Example: Custom repair hooks for domain-specific JSON transformations.

This example demonstrates how to add custom repair logic for
handling domain-specific patterns in AI-generated JSON.
"""

from ai_json_cleanroom import validate_ai_json, ValidateOptions


def repair_undefined_values(text: str, options: ValidateOptions):
    """
    Custom repair hook: Replace 'UNDEFINED' with null.

    AI models sometimes use placeholder values like UNDEFINED, N/A, etc.
    This hook normalizes them to JSON null.

    Args:
        text: Current text being repaired
        options: ValidateOptions instance (can access configuration)

    Returns:
        tuple: (modified_text, changes_count, metadata_dict)
    """
    original = text
    modified = text

    # Replace standalone UNDEFINED
    modified = modified.replace(': UNDEFINED', ': null')
    modified = modified.replace(':UNDEFINED', ':null')
    modified = modified.replace('"UNDEFINED"', 'null')

    # Count changes
    changes = len(original) - len(modified) + (len(modified) - len(original))
    changes = original.count('UNDEFINED') - modified.count('UNDEFINED')

    metadata = {
        "undefined_replaced": changes
    }

    return modified, changes, metadata


def repair_date_format(text: str, options: ValidateOptions):
    """
    Custom repair hook: Normalize date formats.

    AI models might output dates in inconsistent formats.
    This hook normalizes common variations.
    """
    import re

    modified = text
    changes = 0
    metadata = {"date_formats_normalized": []}

    # Pattern: MM/DD/YYYY -> YYYY-MM-DD
    pattern = r'"(\d{2})/(\d{2})/(\d{4})"'
    matches = re.findall(pattern, modified)
    for match in matches:
        old_format = f'"{match[0]}/{match[1]}/{match[2]}"'
        new_format = f'"{match[2]}-{match[0]}-{match[1]}"'
        modified = modified.replace(old_format, new_format, 1)
        changes += 1
        metadata["date_formats_normalized"].append({
            "from": old_format,
            "to": new_format
        })

    return modified, changes, metadata


def repair_currency_symbols(text: str, options: ValidateOptions):
    """
    Custom repair hook: Remove currency symbols and convert to numbers.

    AI models often include $ symbols in numeric fields.
    """
    import re

    modified = text
    changes = 0
    metadata = {"currency_conversions": []}

    # Pattern: "$1,234.56" -> 1234.56
    pattern = r'"\$([0-9,]+\.?\d*)"'

    def replace_currency(match):
        nonlocal changes
        original_value = match.group(0)
        numeric_value = match.group(1).replace(',', '')
        changes += 1
        metadata["currency_conversions"].append({
            "from": original_value,
            "to": numeric_value
        })
        return numeric_value

    modified = re.sub(pattern, replace_currency, modified)

    return modified, changes, metadata


def repair_boolean_strings(text: str, options: ValidateOptions):
    """
    Custom repair hook: Convert string booleans to actual booleans.

    Handle cases like "yes"/"no", "Y"/"N", "1"/"0" as booleans.
    """
    modified = text
    changes = 0
    metadata = {"boolean_conversions": []}

    replacements = {
        '": "yes"': '": true',
        '": "no"': '": false',
        '": "Yes"': '": true',
        '": "No"': '": false',
        '": "YES"': '": true',
        '": "NO"': '": false',
        '": "Y"': '": true',
        '": "N"': '": false',
        '": "1"': '": true',
        '": "0"': '": false',
    }

    for old, new in replacements.items():
        if old in modified:
            count = modified.count(old)
            modified = modified.replace(old, new)
            changes += count
            if count > 0:
                metadata["boolean_conversions"].append({
                    "pattern": old,
                    "count": count
                })

    return modified, changes, metadata


def repair_null_strings(text: str, options: ValidateOptions):
    """
    Custom repair hook: Convert various null representations to JSON null.

    Handles: "null", "NULL", "None", "nil", "N/A", "n/a"
    """
    modified = text
    changes = 0

    null_patterns = [
        (': "null"', ': null'),
        (': "NULL"', ': null'),
        (': "None"', ': null'),
        (': "nil"', ': null'),
        (': "NIL"', ': null'),
        (': "N/A"', ': null'),
        (': "n/a"', ': null'),
        (':"null"', ':null'),
        (':"NULL"', ':null'),
        (':"None"', ':null'),
    ]

    for old, new in null_patterns:
        count = modified.count(old)
        if count > 0:
            modified = modified.replace(old, new)
            changes += count

    metadata = {"null_strings_normalized": changes}

    return modified, changes, metadata


def example_basic_custom_hook():
    """Example 1: Basic custom repair hook."""
    print("=" * 70)
    print("Example 1: Replace UNDEFINED with null")
    print("=" * 70 + "\n")

    # AI output with UNDEFINED placeholders
    ai_output = '''
    {
        "name": "Alice",
        "age": 30,
        "phone": UNDEFINED,
        "address": {
            "street": "123 Main St",
            "apartment": UNDEFINED
        }
    }
    '''

    print("Input (with UNDEFINED):")
    print(ai_output)

    # Use custom hook
    options = ValidateOptions(
        custom_repair_hooks=[repair_undefined_values]
    )

    result = validate_ai_json(ai_output, options=options)

    if result.json_valid:
        print("\nOK: Successfully repaired!")
        print(f"Output: {result.data}")

        # Check repair metadata
        if result.warnings:
            for warning in result.warnings:
                if warning.code == "repaired":
                    print(f"\nRepairs applied: {warning.detail.get('applied', [])}")
    else:
        print(f"ERROR: Failed: {result.errors}")


def example_multiple_hooks():
    """Example 2: Multiple custom hooks working together."""
    print("\n" + "=" * 70)
    print("Example 2: Multiple Custom Hooks")
    print("=" * 70 + "\n")

    # AI output with multiple issues
    ai_output = '''
    {
        "user": "Alice",
        "balance": "$1,234.56",
        "created_date": "01/15/2024",
        "verified": "yes",
        "phone": "N/A",
        "premium": "no"
    }
    '''

    print("Input (with currency, dates, boolean strings, N/A):")
    print(ai_output)

    # Use multiple hooks
    options = ValidateOptions(
        custom_repair_hooks=[
            repair_currency_symbols,
            repair_date_format,
            repair_boolean_strings,
            repair_null_strings
        ]
    )

    result = validate_ai_json(ai_output, options=options)

    if result.json_valid:
        print("\nOK: Successfully repaired with multiple hooks!")
        print(f"Output: {result.data}")
    else:
        print(f"ERROR: Failed: {result.errors}")


def example_conditional_repair():
    """Example 3: Conditional repair based on context."""
    print("\n" + "=" * 70)
    print("Example 3: Conditional Repair Hook")
    print("=" * 70 + "\n")

    def repair_product_codes(text: str, options: ValidateOptions):
        """Only repair if it looks like a product catalog."""
        # Check if this looks like product data
        if '"product' not in text.lower() and '"sku' not in text.lower():
            # Not product data, skip this repair
            return text, 0, {"skipped": "not_product_data"}

        # Apply product-specific repairs
        import re
        modified = text

        # Normalize SKU format: ABC123 -> ABC-123
        pattern = r'"([A-Z]{3})(\d{3})"'
        modified = re.sub(pattern, r'"\1-\2"', modified)

        changes = len(re.findall(pattern, text))
        metadata = {"sku_formats_normalized": changes}

        return modified, changes, metadata

    # Product data
    product_json = '''
    {
        "product_id": "ABC123",
        "name": "Widget",
        "sku": "XYZ789"
    }
    '''

    print("Input (product data):")
    print(product_json)

    options = ValidateOptions(
        custom_repair_hooks=[repair_product_codes]
    )

    result = validate_ai_json(product_json, options=options)

    if result.json_valid:
        print(f"\nOK: Repaired: {result.data}")
    else:
        print(f"ERROR: Failed: {result.errors}")


def example_hook_order_matters():
    """Example 4: Demonstrate that hook order matters."""
    print("\n" + "=" * 70)
    print("Example 4: Hook Execution Order")
    print("=" * 70 + "\n")

    def hook_step1(text: str, options: ValidateOptions):
        """First transformation."""
        modified = text.replace('PLACEHOLDER1', 'TEMP')
        changes = text.count('PLACEHOLDER1')
        return modified, changes, {"step": 1}

    def hook_step2(text: str, options: ValidateOptions):
        """Second transformation."""
        modified = text.replace('TEMP', '"actual_value"')
        changes = text.count('TEMP')
        return modified, changes, {"step": 2}

    ai_output = '{"field": PLACEHOLDER1}'

    print(f"Input: {ai_output}")
    print("\nHooks will transform: PLACEHOLDER1 -> TEMP -> 'actual_value'")

    options = ValidateOptions(
        custom_repair_hooks=[hook_step1, hook_step2]  # Order matters!
    )

    result = validate_ai_json(ai_output, options=options)

    if result.json_valid:
        print(f"\nOK: Result: {result.data}")
        print("\nNote: Hooks executed in order: step1 then step2")
    else:
        print(f"ERROR: Failed: {result.errors}")


def example_real_world_scenario():
    """Example 5: Real-world medical data scenario."""
    print("\n" + "=" * 70)
    print("Example 5: Real-World Medical Data Repair")
    print("=" * 70 + "\n")

    def repair_medical_data(text: str, options: ValidateOptions):
        """Handle medical data quirks."""
        import re
        modified = text
        changes = 0
        metadata = {}

        # Blood pressure format: "120/80" -> {"systolic": 120, "diastolic": 80}
        bp_pattern = r'"blood_pressure":\s*"(\d+)/(\d+)"'
        matches = re.findall(bp_pattern, modified)
        for match in matches:
            old = f'"blood_pressure": "{match[0]}/{match[1]}"'
            new = f'"blood_pressure": {{"systolic": {match[0]}, "diastolic": {match[1]}}}'
            modified = modified.replace(old, new, 1)
            changes += 1

        # Temperature: "98.6°F" -> 98.6
        temp_pattern = r'"temperature":\s*"([\d.]+)°[FC]"'
        modified = re.sub(temp_pattern, r'"temperature": \1', modified)
        changes += len(re.findall(temp_pattern, text))

        # Yes/No to boolean for test results
        modified = re.sub(r'"result":\s*"positive"', '"result": true', modified)
        modified = re.sub(r'"result":\s*"negative"', '"result": false', modified)

        metadata["repairs"] = "medical_data_normalized"
        return modified, changes, metadata

    # AI-generated medical record
    ai_output = '''
    {
        "patient": "John Doe",
        "blood_pressure": "120/80",
        "temperature": "98.6°F",
        "covid_test": {
            "result": "negative",
            "date": "01/15/2024"
        }
    }
    '''

    print("Input (medical data with quirks):")
    print(ai_output)

    options = ValidateOptions(
        custom_repair_hooks=[repair_medical_data, repair_date_format]
    )

    result = validate_ai_json(ai_output, options=options)

    if result.json_valid:
        print("\nOK: Medical data normalized!")
        print(f"Output: {result.data}")
    else:
        print(f"ERROR: Failed: {result.errors}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AI JSON Cleanroom - Custom Repair Hooks Examples")
    print("=" * 70 + "\n")

    # Run examples
    example_basic_custom_hook()
    example_multiple_hooks()
    example_conditional_repair()
    example_hook_order_matters()
    example_real_world_scenario()

    print("\n" + "=" * 70)
    print("All custom repair hook examples complete!")
    print("=" * 70 + "\n")

    print("""
Key Takeaways:

1. Custom hooks allow domain-specific transformations
2. Hooks execute in the order they're provided
3. Return (modified_text, changes_count, metadata_dict)
4. Hooks can be conditional based on content
5. Combine multiple hooks for complex repairs
6. Use for: currency, dates, booleans, null variants, etc.

Create hooks for your specific use case!
    """)
