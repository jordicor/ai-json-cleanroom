"""
AI JSON Cleanroom - Robust post-processing layer for AI-generated JSON.

Main exports:
    validate_ai_json: Main validation function
    ValidationResult: Result object
    ValidationIssue: Individual error/warning
    ValidateOptions: Configuration options
    ErrorCode: Error type enumeration
    extract_json_payload: Extract JSON from text
    detect_truncation: Detect truncated JSON
"""

from ai_json_cleanroom import (
    validate_ai_json,
    validate_loose_json,
    make_loose_json_validate_options,
    ValidationResult,
    ValidationIssue,
    ValidateOptions,
    ErrorCode,
    extract_json_payload,
    detect_truncation,
)

__version__ = "1.2.0"
__all__ = [
    "validate_ai_json",
    "validate_loose_json",
    "make_loose_json_validate_options",
    "ValidationResult",
    "ValidationIssue",
    "ValidateOptions",
    "ErrorCode",
    "extract_json_payload",
    "detect_truncation",
]
