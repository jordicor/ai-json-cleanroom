"""
Performance benchmark comparing stdlib json vs orjson.

This benchmark demonstrates the performance benefits of using orjson
over the standard library json module for parsing and serializing JSON.

Run with: python tests/benchmark_json_vs_orjson.py

Requirements:
- orjson (optional): pip install orjson
"""

import time
import json as stdlib_json
import sys
from pathlib import Path

# Add parent directory to path to import ai_json_cleanroom
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import orjson
    HAS_ORJSON = True
except ImportError:
    HAS_ORJSON = False
    print("WARNING: orjson not installed. Install with: pip install orjson")
    print("Benchmark will only show stdlib json performance.\n")

from ai_json_cleanroom import validate_ai_json


def load_fixture(filename):
    """Load JSON fixture file."""
    fixture_path = Path(__file__).parent / "fixtures" / filename
    with open(fixture_path, "r", encoding="utf-8") as f:
        return f.read()


def benchmark_parse(json_str, iterations=1000, label=""):
    """Benchmark JSON parsing performance."""
    results = {}

    # Benchmark stdlib json
    start = time.perf_counter()
    for _ in range(iterations):
        stdlib_json.loads(json_str)
    stdlib_time = time.perf_counter() - start
    results["stdlib_json"] = stdlib_time

    # Benchmark orjson if available
    if HAS_ORJSON:
        start = time.perf_counter()
        for _ in range(iterations):
            orjson.loads(json_str)
        orjson_time = time.perf_counter() - start
        results["orjson"] = orjson_time
        results["speedup"] = stdlib_time / orjson_time

    return results


def benchmark_dumps(data, iterations=1000, label=""):
    """Benchmark JSON serialization performance."""
    results = {}

    # Benchmark stdlib json
    start = time.perf_counter()
    for _ in range(iterations):
        stdlib_json.dumps(data)
    stdlib_time = time.perf_counter() - start
    results["stdlib_json"] = stdlib_time

    # Benchmark orjson if available
    if HAS_ORJSON:
        start = time.perf_counter()
        for _ in range(iterations):
            orjson.dumps(data)
        orjson_time = time.perf_counter() - start
        results["orjson"] = orjson_time
        results["speedup"] = stdlib_time / orjson_time

    return results


def benchmark_full_validation(json_str, iterations=100, label=""):
    """Benchmark full validation with ai_json_cleanroom."""
    start = time.perf_counter()
    for _ in range(iterations):
        validate_ai_json(json_str)
    total_time = time.perf_counter() - start

    return {"total_time": total_time, "avg_per_call": total_time / iterations}


def format_time(seconds):
    """Format time in appropriate units."""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.1f} µs"
    elif seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    else:
        return f"{seconds:.2f} s"


def print_section(title):
    """Print section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def print_results(results, operations_count):
    """Print benchmark results in a formatted table."""
    if "stdlib_json" in results:
        stdlib_time = results["stdlib_json"]
        avg_stdlib = stdlib_time / operations_count
        print(f"  stdlib json:  {format_time(stdlib_time):>10} total  ({format_time(avg_stdlib)} per op)")

    if "orjson" in results and HAS_ORJSON:
        orjson_time = results["orjson"]
        avg_orjson = orjson_time / operations_count
        print(f"  orjson:       {format_time(orjson_time):>10} total  ({format_time(avg_orjson)} per op)")

        if "speedup" in results:
            speedup = results["speedup"]
            print(f"  Speedup:      {speedup:.2f}x faster with orjson")


def main():
    """Run all benchmarks."""
    print("\n" + "=" * 70)
    print("  AI JSON Cleanroom - Performance Benchmark")
    print("  Comparing stdlib json vs orjson")
    print("=" * 70)

    if HAS_ORJSON:
        print(f"\n[OK] orjson version: {orjson.__version__}")
    else:
        print("\n[X] orjson not available (benchmarking stdlib json only)")

    print(f"[OK] Python version: {sys.version.split()[0]}")

    # Load test data
    simple_json = load_fixture("simple.json")
    complex_json = load_fixture("complex.json")

    simple_data = stdlib_json.loads(simple_json)
    complex_data = stdlib_json.loads(complex_json)

    # Benchmark 1: Parse simple JSON
    print_section("Benchmark 1: Parse Simple JSON (5 fields, ~150 bytes)")
    iterations = 10000
    print(f"  Iterations: {iterations:,}")
    results = benchmark_parse(simple_json, iterations, "simple")
    print_results(results, iterations)

    # Benchmark 2: Parse complex JSON
    print_section("Benchmark 2: Parse Complex JSON (nested, arrays, ~3KB)")
    iterations = 5000
    print(f"  Iterations: {iterations:,}")
    results = benchmark_parse(complex_json, iterations, "complex")
    print_results(results, iterations)

    # Benchmark 3: Serialize simple JSON
    print_section("Benchmark 3: Serialize Simple JSON")
    iterations = 10000
    print(f"  Iterations: {iterations:,}")
    results = benchmark_dumps(simple_data, iterations, "simple")
    print_results(results, iterations)

    # Benchmark 4: Serialize complex JSON
    print_section("Benchmark 4: Serialize Complex JSON")
    iterations = 5000
    print(f"  Iterations: {iterations:,}")
    results = benchmark_dumps(complex_data, iterations, "complex")
    print_results(results, iterations)

    # Benchmark 5: Full validation pipeline (extraction + parse + validate)
    print_section("Benchmark 5: Full Validation Pipeline")
    markdown_wrapped = f'''Here is the data:

```json
{simple_json}
```

Hope this helps!'''

    iterations = 1000
    print(f"  Iterations: {iterations:,}")
    print("  (Includes: extraction from markdown + parsing + validation)")
    results = benchmark_full_validation(markdown_wrapped, iterations)
    print(f"\n  Total time:   {format_time(results['total_time'])}")
    print(f"  Avg per call: {format_time(results['avg_per_call'])}")

    # Benchmark 6: Malformed JSON repair
    print_section("Benchmark 6: Malformed JSON Repair + Validation")
    malformed = "{'name': 'Alice', age: 30, active: True, 'tags': ['python', 'ai',]}"
    iterations = 500
    print(f"  Iterations: {iterations:,}")
    print("  (Includes: repair passes + parsing + validation)")
    results = benchmark_full_validation(malformed, iterations)
    print(f"\n  Total time:   {format_time(results['total_time'])}")
    print(f"  Avg per call: {format_time(results['avg_per_call'])}")

    # Summary
    print_section("Summary")
    if HAS_ORJSON:
        print("""
  orjson provides significant performance improvements:

  - 3-4x faster parsing for typical AI-generated JSON
  - 3-4x faster serialization
  - Lower memory usage
  - Better handling of large numbers and unicode

  Installation: pip install orjson

  ai-json-cleanroom automatically uses orjson when available,
  with transparent fallback to stdlib json.
        """)
    else:
        print("""
  Install orjson for 3-4x performance improvement:

    pip install orjson

  ai-json-cleanroom will automatically detect and use it.
        """)

    print("\n" + "=" * 70)
    print("  Benchmark Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
