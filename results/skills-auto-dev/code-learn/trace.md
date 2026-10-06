### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


Execution boundary: inspect and modify only relative paths under workspace/ and, when present, read skill instructions only under skills/. Never inspect parent, home, temporary, repository, or other absolute paths, and never search for hidden checks, evaluator code, or undisclosed conventions. Do not repeat a command whose result is already sufficient. Once the requested outputs are complete, validate them once and stop.

### Assistant
I'll start by reading the skill instructions that apply to this task.

### Tool call: read_file
{"file_path": "skills/code-fix-deliverables/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "skills/output-spec-compliance/SKILL.md", "limit": 1000}

### Tool call: read_file
{"file_path": "skills/verify-artifacts-and-environment/SKILL.md", "limit": 1000}

### Tool result
@@ lines 1-11 of 11 @@
---
name: code-fix-deliverables
description: Use when fixing bugs in an existing package whose task also imposes repo-wide constraints such as do-not-modify rules, typing rules, required new files, or a changelog.
---
- Enumerate all repository constraints from the task up front (editing restrictions, typing requirements, required new files, formatting conventions).
- Never modify existing test files; add new test files when regressions must be captured.
- Ensure public functions have type annotations on every parameter and on the return value before finishing.
- Create the required regression-test file with one test function per fixed bug, meeting any stated minimum count.
- Record each fix in the changelog under the mandated heading and using the mandated bullet format.
- Run the full test suite after all edits and confirm it passes.
- Verify each mandatory artifact exists at the required path with the required structure.

### Tool result
@@ lines 1-13 of 13 @@
---
name: output-spec-compliance
description: Use when a task states explicit rules about output files, schemas, units, naming, ordering, or required keys, so every mandated property is satisfied before submission.
---
- Before coding, list every stated rule/constraint as a separate, testable obligation.
- Map each obligation to the exact artifact (file, object, key, field) that must satisfy it.
- Convert quantities to the required unit whenever a unit is specified; emit integer minor units when a value is defined in a smaller unit, and keep rounding consistent.
- Apply required identifier normalization (case, separator style) to every affected value, including keys and counts.
- Sort collections by the specified key(s) and direction, adding a deterministic tie-breaker so order is reproducible.
- Include every mandated top-level field or file header (schema/version tags, generator name, source, row counts) with the exact names given.
- Produce every demanded output artifact, including auxiliary files, not just the primary one.
- After generating outputs, programmatically assert each rule (presence of keys, units, sort order, header row) instead of relying on visual inspection.
- Do not declare completion while any enumerated rule remains unverified.

### Tool result
@@ lines 1-11 of 11 @@
---
name: verify-artifacts-and-environment
description: Use before finishing any task that runs scripts or writes files, to confirm the interpreter, paths, and final artifacts are correct.
---
- Probe which interpreter/commands actually exist instead of assuming an alias is available.
- Confirm required input files exist at the paths you intend to open before running.
- Run scripts from a working directory that makes relative paths valid, or use absolute paths.
- After producing outputs, read them back and confirm they parse and contain the required content.
- Skip any internal validation step that cannot produce visible output; write a script file and run it instead of fighting complex inline quoting.
- Delete only temporary files you created; never remove required deliverables.
- Re-run the final validation command after cleanup to confirm nothing required was removed or broken.

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/inventory"}

### Tool call: ls
{"path": "workspace/tests"}

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_report.py']

### Tool result
@@ lines 1-5 of 5 @@
# inventory

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 0.3.1
- initial import

### Tool call: read_file
{"file_path": "workspace/inventory/__init__.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "workspace/tests/test_report.py"}

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Tool call: glob
{"pattern": "workspace/**/*"}

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -40"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/__init__.cpython-312.pyc', '/workspace/inventory/__pycache__/export.cpython-312.pyc', '/workspace/inventory/__pycache__/pricing.cpython-312.pyc', '/workspace/inventory/__pycache__/report.cpython-312.pyc', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py', '/workspace/tests/__pycache__/test_report.cpython-312-pytest-9.1.1.pyc', '/workspace/tests/test_report.py']

### Tool result
               ^^^^^^^^^^^^^^^^^^

F:\New folder\Lab20\K4-L3L4-Track3-Day20-AdvanceMultiAgents\tasks\code-learn\workspace\tests\test_report.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
inventory\report.py:14: in total_value
    price = parse_price(item["price"])
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

text = '$1,299.50'

    def parse_price(text):
        """Convert a price string to a Decimal.
    
        Supported formats:
          "$1,299.50" -> Decimal("1299.50")
          "  12 "     -> Decimal("12")
          "1299.5"    -> Decimal("1299.5")
          "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
        """
        cleaned = text.strip().replace("$", "")
>       return Decimal(cleaned)
               ^^^^^^^^^^^^^^^^
E       decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

inventory\pricing.py:15: InvalidOperation
_______________________ test_discount_rounding_half_up ________________________

    def test_discount_rounding_half_up():
>       assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")
E       AssertionError: assert Decimal('9.04') == Decimal('9.05')
E        +  where Decimal('9.04') = apply_discount(Decimal('10.05'), 10)
E        +    where Decimal('10.05') = Decimal('10.05')
E        +  and   Decimal('9.05') = Decimal('9.05')

F:\New folder\Lab20\K4-L3L4-Track3-Day20-AdvanceMu

### Assistant
Now let me check the remaining source and fix the bugs against the docstring specs.

### Tool call: write_file
{"file_path": "workspace/inventory/pricing.py", "content": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import ROUND_HALF_UP, Decimal\n\nCENTS = Decimal(\"0.01\")\n\n\ndef parse_price(text: str) -> Decimal:\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip().replace(\"$\", \"\").replace(\",\", \"\")\n    if cleaned.startswith(\"(\") and cleaned.endswith(\")\"):\n        return -Decimal(cleaned[1:-1].strip())\n    return Decimal(cleaned)\n\n\ndef apply_discount(price: Decimal, percent: int) -> Decimal:\n    \"\"\"Return `price` after a percentage discount.\n\n    The result is a Decimal rounded to 2 decimal places using the\n    commercial rule \"round half up\" (0.005 -> 0.01).\n    \"\"\"\n    discounted = price * (100 - percent) / 100\n    return discounted.quantize(CENTS, rounding=ROUND_HALF_UP)\n"}

### Tool call: write_file
{"file_path": "workspace/inventory/export.py", "content": "\"\"\"Export helpers.\"\"\"\nfrom typing import Any\n\nfrom .pricing import parse_price\n\n\ndef to_csv_row(item: dict[str, Any]) -> str:\n    \"\"\"Format one item as a CSV row: name,price,qty (price with 2 decimals).\n\n    A name that contains a comma or a double quote is wrapped in double quotes,\n    and every double quote inside it is doubled (RFC 4180).\n    \"\"\"\n    price = parse_price(item[\"price\"])\n    name = item[\"name\"]\n    if \",\" in name or '\"' in name:\n        name = '\"' + name.replace('\"', '\"\"') + '\"'\n    return f\"{name},{price:.2f},{item['qty']}\"\n"}

### Tool call: write_file
{"file_path": "workspace/inventory/report.py", "content": "\"\"\"Inventory reports.\"\"\"\nfrom decimal import Decimal\nfrom typing import Any\n\nfrom .pricing import apply_discount, parse_price\n\n\ndef total_value(items: list[dict[str, Any]]) -> Decimal:\n    \"\"\"Total value of `items` after per-item discounts.\n\n    Each item is a dict: {\"name\": str, \"price\": str, \"qty\": int, \"discount\": percent (optional)}.\n    \"\"\"\n    total = Decimal(\"0\")\n    for item in items:\n        price = parse_price(item[\"price\"])\n        price = apply_discount(price, item.get(\"discount\", 0))\n        total += price * item[\"qty\"]\n    return total\n\n\ndef low_stock(items: list[dict[str, Any]], threshold: int = 5) -> list[str]:\n    \"\"\"Names of the items whose quantity is strictly below `threshold`.\n\n    The names are sorted alphabetically, ignoring case.\n    \"\"\"\n    names = [item[\"name\"] for item in items if item[\"qty\"] < threshold]\n    return sorted(names, key=str.lower)\n"}

### Tool result
Updated file /workspace/inventory/pricing.py

### Tool result
Updated file /workspace/inventory/export.py

### Tool result
Updated file /workspace/inventory/report.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5"}

### Tool call: write_file
{"content": "from decimal import Decimal\n\nfrom inventory.export import to_csv_row\nfrom inventory.pricing import apply_discount, parse_price\nfrom inventory.report import low_stock, total_value\n\nassert parse_price(\"$1,299.50\") == Decimal(\"1299.50\")\nassert parse_price(\"  12 \") == Decimal(\"12\")\nassert parse_price(\"1299.5\") == Decimal(\"1299.5\")\nassert parse_price(\"(12.00)\") == Decimal(\"-12.00\")\nassert parse_price(\"($1,299.50)\") == Decimal(\"-1299.50\")\n\nassert apply_discount(Decimal(\"10.05\"), 10) == Decimal(\"9.05\")\nassert apply_discount(Decimal(\"0.005\"), 0) == Decimal(\"0.01\")\nassert apply_discount(Decimal(\"100.00\"), 15) == Decimal(\"85.00\")\nassert apply_discount(Decimal(\"10\"), 100) == Decimal(\"0.00\")\nassert apply_discount(Decimal(\"12.00\"), -25) == Decimal(\"15.00\")\nassert apply_discount(Decimal(\"12.00\"), Decimal(\"12.5\")) == Decimal(\"10.50\")\n\nassert total_value([{\"name\": \"pen\", \"price\": \"$2.50\", \"qty\": 4}]) == Decimal(\"10.00\")\nassert total_value([{\"name\": \"laptop\", \"price\": \"$1,299.50\", \"qty\": 2}]) == Decimal(\"2599.00\")\nassert total_value([{\"name\": \"desk\", \"price\": \"100.00\", \"qty\": 1, \"discount\": 15}]) == Decimal(\"85.00\")\n\nassert low_stock([{\"name\": \"pen\", \"qty\": 2}, {\"name\": \"ink\", \"qty\": 9}]) == [\"pen\"]\nassert low_stock([{\"name\": \"b\", \"qty\": 1}, {\"name\": \"A\", \"qty\": 1}, {\"name\": \"c\", \"qty\": 5}]) == [\"A\", \"b\"]\nassert low_stock([{\"name\": \"x

### Tool result
......                                                                   [100%]
6 passed in 0.10s

[Command succeeded with exit code 0]

### Tool result
Updated file /workspace/_check_spec.py

### Tool call: execute
{"command": "cd workspace && python _check_spec.py"}

### Tool result
all docstring checks passed

[Command succeeded with exit code 0]

### Assistant
All spec checks pass. Now cleaning up the temp file, adding a regression test file, and recording fixes in the changelog.

### Tool call: delete
{"file_path": "workspace/_check_spec.py"}

### Tool call: write_file
{"content": "\"\"\"Regression tests for the docstring-spec bugs fixed in the inventory package.\"\"\"\nfrom decimal import Decimal\n\nfrom inventory.export import to_csv_row\nfrom inventory.pricing import apply_discount, parse_price\nfrom inventory.report import low_stock, total_value\n\n\ndef test_parse_price_strips_thousands_separator():\n    assert parse_price(\"$1,299.50\") == Decimal(\"1299.50\")\n\n\ndef test_parse_price_accounting_parentheses_are_negative():\n    assert parse_price(\"(12.00)\") == Decimal(\"-12.00\")\n\n\ndef test_apply_discount_rounds_half_up():\n    assert apply_discount(Decimal(\"10.05\"), 10) == Decimal(\"9.05\")\n\n\ndef test_low_stock_is_strictly_below_threshold():\n    assert low_stock([{\"name\": \"pen\", \"qty\": 2}, {\"name\": \"ink\", \"qty\": 9}]) == [\"pen\"]\n    assert low_stock([{\"name\": \"exact\", \"qty\": 5}], 5) == []\n\n\ndef test_low_stock_sorted_case_insensitively():\n    items = [{\"name\": \"ink\", \"qty\": 1}, {\"name\": \"Pen\", \"qty\": 2}]\n    assert low_stock(items) == [\"ink\", \"Pen\"]\n\n\ndef test_to_csv_row_quotes_names_with_comma_or_quote():\n    assert to_csv_row({\"name\": 'a,b', \"price\": \"2.5\", \"qty\": 4}) == '\"a,b\",2.50,4'\n    assert to_csv_row({\"name\": 'a\"b', \"price\": \"2.5\", \"qty\": 4}) == '\"a\"\"b\",2.50,4'\n", "file_path": "workspace/tests/test_regressions.py"}

### Tool call: write_file
{"content": "# Changelog\n\n## Unreleased\n- Fix `pricing.parse_price` to strip thousands separators (`\"$1,299.50\"`) and to interpret accounting-style parentheses as a negative price (`\"(12.00)\"`).\n- Fix `pricing.apply_discount` to round half up with `ROUND_HALF_UP`, so values such as `10.05` - 10% become `9.05` instead of `9.04`.\n- Fix `report.low_stock` to select only quantities strictly below the threshold and to sort the names alphabetically ignoring case.\n- Fix `export.to_csv_row` to wrap names containing a comma or a double quote in double quotes and to double inner quotes (RFC 4180).\n- Add type annotations to all public function parameters and return values.\n\n## 0.3.1\n- initial import\n", "file_path": "workspace/CHANGELOG.md"}

### Tool result
Deleted /workspace/_check_spec.py

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool result
Updated file /workspace/CHANGELOG.md

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5 && python -m compileall -q inventory >/dev/null && echo COMPILED"}

### Tool call: execute
{"command": "cd workspace && (python -m ruff check inventory tests 2>&1 | tail -20; python -m mypy inventory 2>&1 | tail -10) || true"}

### Tool result
............                                                             [100%]
12 passed in 0.05s

[stderr] The system cannot find the path specified.

Exit code: 1
[Command failed with exit code 1]

### Tool result
tail: option used in invalid context -- 2

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q"}

### Tool call: execute
{"command": "cd workspace && python -m compileall -q inventory && echo COMPILED"}

### Tool result
............                                                             [100%]
12 passed in 0.03s

[Command succeeded with exit code 0]

### Tool result
COMPILED

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m ruff --version; python -m mypy --version; python --version"}

### Tool result
[stderr] ~\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe: No module named ruff

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "cd workspace && python -m mypy --version; python --version"}

### Tool result
[stderr] ~\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe: No module named mypy

Exit code: 1
[Command failed with exit code 1]

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool result
@@ lines 1-29 of 29 @@
"""Price utilities for the inventory package."""
from decimal import ROUND_HALF_UP, Decimal

CENTS = Decimal("0.01")


def parse_price(text: str) -> Decimal:
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "").replace(",", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        return -Decimal(cleaned[1:-1].strip())
    return Decimal(cleaned)


def apply_discount(price: Decimal, percent: int) -> Decimal:
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(CENTS, rounding=ROUND_HALF_UP)

### Tool result
@@ lines 1-17 of 17 @@
"""Export helpers."""
from typing import Any

from .pricing import parse_price


def to_csv_row(item: dict[str, Any]) -> str:
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    name = item["name"]
    if "," in name or '"' in name:
        name = '"' + name.replace('"', '""') + '"'
    return f"{name},{price:.2f},{item['qty']}"

### Tool result
@@ lines 1-27 of 27 @@
"""Inventory reports."""
from decimal import Decimal
from typing import Any

from .pricing import apply_discount, parse_price


def total_value(items: list[dict[str, Any]]) -> Decimal:
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items: list[dict[str, Any]], threshold: int = 5) -> list[str]:
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    names = [item["name"] for item in items if item["qty"] < threshold]
    return sorted(names, key=str.lower)

### Assistant
Done. All 12 tests pass (6 original + 6 new regression tests).

## Fixes (source bugs vs. docstring spec)

**`workspace/inventory/pricing.py`**
- `parse_price`: now strips thousands separators (`"$1,299.50"` → `1299.50`) and handles accounting-style parentheses as negative (`"(12.00)"` → `-12.00`).
- `apply_discount`: now quantizes with `ROUND_HALF_UP` (the docstring's "round half up"), so `10.05` − 10% gives `9.05` instead of the default `ROUND_HALF_EVEN` result `9.04`.
- Added the shared `CENTS` constant and type annotations.

**`workspace/inventory/report.py`**
- `low_stock`: changed `<= threshold` to `< threshold` (spec says *strictly below*) and sorts the returned names case-insensitively (`key=str.lower`), as documented. Previously unsorted.

**`workspace/inventory/export.py`**
- `to_csv_row`: now implements RFC 4180 quoting — a name containing a comma or double quote is wrapped in double quotes with inner quotes doubled.
- Type annotations added.

## Supporting changes
- **`workspace/tests/test_regressions.py`** (new): one test per fixed bug (thousands separator, parentheses, half-up rounding, strict threshold, case-insensitive sort, CSV quoting). Existing tests untouched.
- **`workspace/CHANGELOG.md`**: recorded each fix under `## Unreleased`.
- All public functions now have annotations on every parameter and the return value.

Validation: `cd workspace && python -m pytest tests -q` → `12 passed`; modules compile cleanly. (No `ruff`/`mypy` available in this environmen