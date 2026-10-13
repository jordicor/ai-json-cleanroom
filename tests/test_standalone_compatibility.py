"""Public defaults, loose JSON helpers and single-file CLI portability."""

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from ai_json_cleanroom import (
    ErrorCode,
    ValidateOptions,
    make_loose_json_validate_options,
    validate_ai_json,
    validate_loose_json,
)


@pytest.mark.parametrize(
    "payload,schema,code",
    [
        (
            '{"a": 1, "extra": 2}',
            {"type": "object", "properties": {"a": {"type": "integer"}}, "additionalProperties": False},
            ErrorCode.ADDITIONAL_PROPERTY,
        ),
        ("[1, 2]", {"type": "array", "items": [{"type": "integer"}], "additionalItems": False}, ErrorCode.ADDITIONAL_ITEMS),
    ],
)
def test_default_api_rejects_undeclared_fields_and_items(payload, schema, code):
    result = validate_ai_json(payload, schema=schema)
    assert not result.json_valid
    assert result.data is None
    assert code in {error.code for error in result.errors}


def test_positional_options_still_disable_repairs():
    # The seventh positional argument was enable_safe_repairs before 1.2.
    options = ValidateOptions(False, True, True, True, False, False, False)
    assert not validate_ai_json("{'name': 'Alice'}", options=options).json_valid


@pytest.mark.parametrize(
    "payload,schema,code",
    [
        (
            {"required_value": 1},
            {"required": ["required_value"], "properties": {}, "additionalProperties": False},
            ErrorCode.MISSING_REQUIRED,
        ),
        ([1, 2], {"minItems": 2, "items": [{"type": "integer"}], "additionalItems": False}, ErrorCode.MIN_ITEMS),
    ],
)
def test_cleaned_output_must_still_satisfy_schema(payload, schema, code):
    snapshot = json.loads(json.dumps(payload))
    result = validate_ai_json(
        payload,
        schema=schema,
        options=ValidateOptions(additional_properties_behavior="strip"),
    )
    assert not result.json_valid
    assert result.data is None
    assert code in {error.code for error in result.errors}
    assert payload == snapshot


def test_loose_json_repairs_wrapped_output_and_checks_expectations():
    content = "Here is the result:\n```json\n{'name': 'Alice', active: True,}\n```"
    result = validate_loose_json(content, expectations=[{"path": "name", "type": "string"}])
    assert result.json_valid
    assert result.data == {"name": "Alice", "active": True}
    assert not validate_loose_json(content, expectations=[{"path": "missing"}]).json_valid
    assert not validate_loose_json('"scalar"').json_valid
    assert not validate_loose_json('{"id": 1, "id": 2}').json_valid


def test_loose_options_are_independent():
    first = make_loose_json_validate_options()
    first.enable_safe_repairs = False
    second = make_loose_json_validate_options()
    assert validate_ai_json("{'name': 'Alice'}", options=second).json_valid


@pytest.mark.parametrize(
    "extra_args,valid",
    [
        ([], False),
        (["--additional-properties", "fail"], False),
        (["--additional-properties", "strip"], True),
    ],
)
def test_single_file_cli_works_without_site_packages(tmp_path, extra_args, valid):
    module = tmp_path / "ai_json_cleanroom.py"
    shutil.copyfile(Path(__file__).resolve().parents[1] / module.name, module)
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {"a": {"type": "integer"}},
                "additionalProperties": False,
            }
        ),
        encoding="utf-8",
    )
    process = subprocess.run(
        [sys.executable, "-I", "-S", str(module), "--input", "-", "--schema", str(schema)] + extra_args,
        input='{"a": 1, "extra": 2}',
        capture_output=True,
        text=True,
        check=True,
        cwd=tmp_path,
    )
    result = json.loads(process.stdout)
    assert result["json_valid"] is valid
    assert result["data"] == ({"a": 1} if valid else None)
    assert result["info"]["parse_backend"] == "json"
    assert "dump_backend=json" in process.stderr
