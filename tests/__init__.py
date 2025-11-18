"""
Test suite for ai-json-cleanroom.

This directory contains comprehensive tests for all components of the library.

Test modules:
- test_json_engine: Tests for JSON parsing engine (orjson vs stdlib)
- test_extraction: Tests for JSON extraction from mixed text
- test_repair: Tests for JSON repair strategies
- test_truncation: Tests for truncation detection
- test_schema_validation: Tests for JSON Schema validation
- test_path_expectations: Tests for path-based validation
- benchmark_json_vs_orjson: Performance benchmarks

Run all tests:
    pytest tests/

Run specific test:
    pytest tests/test_extraction.py

Run with coverage:
    pytest --cov=ai_json_cleanroom tests/

Run benchmarks:
    python tests/benchmark_json_vs_orjson.py
"""
