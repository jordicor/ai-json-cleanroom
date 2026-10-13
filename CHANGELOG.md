# Changelog

## 1.2.0 - 2026-10-13

- Reject duplicate JSON keys, including nested and Unicode-escaped duplicates,
  without exposing the duplicated key/value in the error or letting repairs hide it.
- Accept explicit null schema types and improve malformed-schema handling.
- Bound schema complexity and guard recursion; reject oversized regexes and nested
  variable-width quantifiers. Regex validation is not a complete resource sandbox.
- Add `validate_loose_json` and fresh options for extracting AI JSON without a schema.
- Add opt-in field/item cleanup with warnings, caller-object preservation and safe
  combinator probing. Recheck cleaned data so removal cannot invalidate the result.
- Preserve legacy rejection of extra fields/items by default, including CLI usage
  and positional `ValidateOptions` arguments.
- Keep the single-file package free of required runtime dependencies.
- Parsing now uses stdlib JSON for duplicate-key detection. Optional orjson remains
  available for serialization; previous parsing-speed claims no longer apply.
- Correct CLI documentation to show supported flags.

See the README for cleanup/combinator behavior and input limits.
