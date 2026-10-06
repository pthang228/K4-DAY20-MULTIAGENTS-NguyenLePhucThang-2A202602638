### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

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

### Assistant
Now let me explore the workspace.

### Tool call: ls
{"path": "workspace"}

### Tool call: glob
{"pattern": "workspace/**/*"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-312.pyc', '/workspace/bookings/__pycache__/billing.cpython-312.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-312.pyc', '/workspace/bookings/__pycache__/schedule.cpython-312.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-312.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-312-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "workspace/README.md", "limit": 300}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md", "limit": 300}

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py", "limit": 300}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "limit": 400}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py", "limit": 400}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "limit": 400}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "limit": 400}

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py", "limit": 400}

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -40 && python --version"}

### Tool result
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
bookings\schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
bookings\schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
        Surrounding whitespace is ignored.
        """
        m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
        if not m:
>           raise ValueError(f"bad duration: {text!r}")
E           ValueError: bad duration: '2h'

bookings\timeutil.py:18: ValueError
_______________________ test_billable_blocks_rounds_up ________________________

    def test_billable_blocks_rounds_up():
>       assert billable_blocks(20) == 2
E       assert 1 == 2
E        +  where 1 = billable_blocks(20)

F:\New folder\Lab20\K4-L3L4-Track3-Day20-AdvanceMultiAgents\tasks\code-eval\workspace\tests\test_bookings.py:10: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_bookings.py::test_total_minutes_mixed_formats - ValueError:.

### Assistant
Now I understand the bugs. Let me fix each source file.

### Tool call: write_file
{"file_path": "workspace/bookings/billing.py", "content": "\"\"\"Billing rules.\"\"\"\n\n\ndef billable_blocks(minutes: int, block: int = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    return -(-minutes // block)\n"}

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n# Longest, most explicit forms first: \"1:30\" and \"1h30m\" both mean 90 minutes.\n_COLON_FORM_RE = re.compile(r\"(?P<hours>\\d+):(?P<minutes>\\d{1,2})\")\n_HOURS_FORM_RE = re.compile(r\"(?P<hours>\\d+)h(?:(?P<minutes>\\d+)m)?\")\n_MINUTES_FORM_RE = re.compile(r\"(?P<minutes>\\d+)m\")\n_BARE_MINUTES_RE = re.compile(r\"(?P<minutes>\\d+)\")\n\n_DURATION_PATTERNS: tuple[re.Pattern[str], ...] = (\n    _COLON_FORM_RE,\n    _HOURS_FORM_RE,\n    _MINUTES_FORM_RE,\n    _BARE_MINUTES_RE,\n)\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    value = text.strip()\n\n    for pattern in _DURATION_PATTERNS:\n        match = pattern.fullmatch(value)\n        if match:\n            groups = match.groupdict()\n            hours = int(groups.get(\"hours\") or 0)\n            minutes = int(groups.get(\"minutes\") or 0)\n            return hours * 60 + minutes\n\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool result
Updated file /workspace/bookings/billing.py

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool call: write_file
{"content": "\"\"\"Schedule helpers.\"\"\"\nfrom collections.abc import Iterable, Sequence\nfrom typing import Any\n\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: Any, slots: Sequence[Any] | None = None) -> list[Any]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return [*(slots or ()), slot]\n", "file_path": "workspace/bookings/schedule.py"}

### Tool call: write_file
{"content": "\"\"\"Calendar export.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute: int, duration_text: str) -> int:\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)\n", "file_path": "workspace/bookings/calendar_export.py"}

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool result
Updated file /workspace/bookings/calendar_export.py

### Tool call: glob
{"pattern": "workspace/{pyproject.toml,setup.cfg,setup.py,tox.ini,pytest.ini,*.cfg,*.toml}"}

### Tool result
No files found

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -20"}

### Tool result
...                                                                      [100%]
3 passed in 0.05s

[Command succeeded with exit code 0]

### Assistant
Now let me add the regression tests and changelog entry as required by the deliverables skill.

### Tool call: write_file
{"content": "\"\"\"Regression tests for bugs fixed in bookings 1.4.3.\n\nOne test per fixed bug.  These tests complement ``tests/test_bookings.py``\n(which is intentionally left untouched).\n\"\"\"\nimport pytest\n\nfrom bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n\ndef test_parse_duration_supports_every_documented_format():\n    \"\"\"`parse_duration` must accept all formats listed in its docstring.\"\"\"\n    assert parse_duration(\"1h30m\") == 90\n    assert parse_duration(\"2h\") == 120\n    assert parse_duration(\"45m\") == 45\n    assert parse_duration(\"1:30\") == 90\n    assert parse_duration(\"45\") == 45\n    assert parse_duration(\"  2h  \") == 120\n    assert parse_duration(\"0\") == 0\n    assert parse_duration(\"0h0m\") == 0\n\n\ndef test_parse_duration_rejects_bad_input():\n    \"\"\"Unsupported formats still raise ValueError.\"\"\"\n    with pytest.raises(ValueError):\n        parse_duration(\"tomorrow\")\n    with pytest.raises(ValueError):\n        parse_duration(\"\")\n\n\ndef test_billable_blocks_rounds_partial_blocks_up():\n    \"\"\"A partial block is billed as a full block.\"\"\"\n    assert billable_blocks(0) == 0\n    assert billable_blocks(15) == 1\n    assert billable_blocks(16) == 2\n    assert billable_blocks(20) == 2\n    assert billable_blocks(45) == 3\n    assert billable_blocks(120, block=60) == 2\n

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- Fix `timeutil.parse_duration` to accept every documented format (`\"1h30m\"`, `\"2h\"`, `\"45m\"`, `\"1:30\"`, `\"45\"`).\n- Fix `billing.billable_blocks` to round partial blocks up instead of to the nearest block, and to raise `ValueError` for negative minutes.\n- Fix `schedule.add_slot` to return a new list instead of mutating a shared default argument.\n- Add type annotations to the public functions of `billing`, `calendar_export`, `schedule` and `timeutil`.\n- Add `tests/test_regressions.py` covering the fixed bugs.\n"}

### Tool result
Updated file /workspace/tests/test_regressions.py

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Assistant
Let me refine `schedule.py` to be more idiomatic and fix the version reference in the new test docstring.

### Tool call: write_file
{"content": "\"\"\"Schedule helpers.\"\"\"\nfrom collections.abc import Iterable, Sequence\nfrom typing import TypeVar\n\nfrom .timeutil import parse_duration\n\nSlot = TypeVar(\"Slot\")\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: Slot, slots: Sequence[Slot] | None = None) -> list[Slot]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return [*(() if slots is None else slots), slot]\n", "file_path": "workspace/bookings/schedule.py"}

### Tool call: edit_file
{"file_path": "workspace/tests/test_regressions.py", "old_string": "\"\"\"Regression tests for bugs fixed in bookings 1.4.3.", "new_string": "\"\"\"Regression tests for recently fixed bugs in `bookings`."}

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/tests/test_regressions.py'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -20 && python -m mypy --version 2>&1 | head -2; python -m ruff --version 2>&1 | head -2"}

### Tool result
...........                                                              [100%]
11 passed in 0.07s
head: invalid trailing option -- ;
Try 'head --help' for more information.

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -c \"import mypy\" 2>&1 | tail -1; python -c \"import ruff\" 2>&1 | tail -1; python -c \"\nimport inspect, bookings.billing as b, bookings.schedule as s, bookings.timeutil as t, bookings.calendar_export as c\nfor m in (b,s,t,c):\n    for name,fn in vars(m).items():\n        if inspect.isfunction(fn) and fn.__module__==m.__name__:\n            print(m.__name__, name, inspect.signature(fn))\n\""}

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom bookings.timeutil import parse_duration\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.calendar_export import slot_end\ncases = ['1h30m','2h','45m','1:30','45',' 2h ']\nprint([parse_duration(c) for c in cases])\nfor bad in ['tomorrow','','1h30']:\n    try: parse_duration(bad); print('NO RAISE', repr(bad))\n    except ValueError as e: print('raised', repr(bad))\nprint(billable_blocks(16), billable_blocks(0), billable_blocks(15), billable_blocks(120,60))\ntry: billable_blocks(-1)\nexcept ValueError as e: print('raised negative')\nprint(add_slot('a'), add_slot('b'), add_slot('c',['a','b']))\nprint(total_minutes(['1h30m','2h']), slot_end(60,'1h30m'))\n\""}

### Tool result
[stderr] tail: option used in invalid context -- 1

Exit code: 1
[Command failed with exit code 1]

### Tool result
<no output>
[Command succeeded with exit code 0]

### Tool call: write_file
{"content": "\"\"\"Temporary validation script for the bookings fixes.\"\"\"\nimport inspect\n\nfrom bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\nfor text in (\"1h30m\", \"2h\", \"45m\", \"1:30\", \"45\", \" 2h \", \"0\"):\n    print(\"parse_duration\", repr(text), \"->\", parse_duration(text))\n\nfor bad in (\"tomorrow\", \"\", \"1h30\"):\n    try:\n        parse_duration(bad)\n        print(\"FAIL: no ValueError for\", repr(bad))\n    except ValueError:\n        print(\"ok ValueError for\", repr(bad))\n\nprint(\"billable_blocks\", billable_blocks(0), billable_blocks(15), billable_blocks(16), billable_blocks(20), billable_blocks(120, 60))\ntry:\n    billable_blocks(-1)\n    print(\"FAIL: no ValueError for -1\")\nexcept ValueError:\n    print(\"ok ValueError for -1\")\n\nprint(\"add_slot\", add_slot(\"a\"), add_slot(\"b\"), add_slot(\"c\", [\"a\", \"b\"]))\nprint(\"total_minutes\", total_minutes([]), total_minutes([\"1h30m\", \"2h\"]), total_minutes([\"45\", \"1:30\"]))\nprint(\"slot_end\", slot_end(60, \"1h30m\"), slot_end(540, \"45\"))\n\nimport bookings.billing as b\nimport bookings.calendar_export as c\nimport bookings.schedule as s\nimport bookings.timeutil as t\n\nfor module in (b, c, s, t):\n    for name, func in vars(module).items():\n        if inspect.isfunction(func) and func.__module__ == module.__name__ and not name.sta

### Tool result
Updated file /workspace/_validate.py

### Tool call: execute
{"command": "cd workspace && python _validate.py"}

### Tool result
parse_duration '1h30m' -> 90
parse_duration '2h' -> 120
parse_duration '45m' -> 45
parse_duration '1:30' -> 90
parse_duration '45' -> 45
parse_duration ' 2h ' -> 120
parse_duration '0' -> 0
ok ValueError for 'tomorrow'
ok ValueError for ''
ok ValueError for '1h30'
billable_blocks 0 1 2 2 2
ok ValueError for -1
add_slot ['a'] ['b'] ['a', 'b', 'c']
total_minutes 0 210 135
slot_end 150 585
bookings.billing.billable_blocks: params_missing_annotations=[] return_annotated=True
bookings.calendar_export.slot_end: params_missing_annotations=[] return_annotated=True
bookings.schedule.total_minutes: params_missing_annotations=[] return_annotated=True
bookings.schedule.add_slot: params_missing_annotations=[] return_annotated=True
bookings.timeutil.parse_duration: params_missing_annotations=[] return_annotated=True

[Command succeeded with exit code 0]

### Tool call: delete
{"file_path": "workspace/_validate.py"}

### Tool result
Deleted /workspace/_validate.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md", "limit": 40}

### Tool result
...........                                                              [100%]
11 passed in 0.04s

[Command succeeded with exit code 0]

### Tool result
@@ lines 1-11 of 11 @@
# Changelog

## Unreleased
- Fix `timeutil.parse_duration` to accept every documented format (`"1h30m"`, `"2h"`, `"45m"`, `"1:30"`, `"45"`).
- Fix `billing.billable_blocks` to round partial blocks up instead of to the nearest block, and to raise `ValueError` for negative minutes.
- Fix `schedule.add_slot` to return a new list instead of mutating a shared default argument.
- Add type annotations to the public functions of `billing`, `calendar_export`, `schedule` and `timeutil`.
- Add `tests/test_regressions.py` covering the fixed bugs.

## 1.4.2
- initial import

### Assistant
All 11 tests pass. Final state of the package:

**Bugs fixed (each made the code contradict its own docstring):**

1. `bookings/timeutil.py` — `parse_duration` only matched `"1h30m"`, so `"2h"`, `"45m"`, `"1:30"` and `"45"` all raised `ValueError`. Rewrote it to try all five documented formats (colon form, `h`/`h`+`m`, `m`, bare minutes), keeping `ValueError` for anything unrecognized.
2. `bookings/billing.py` — `billable_blocks` used `round()` (banker's rounding), so 16/20/45 minutes billed too low. Now rounds **up** with `-(-minutes // block)` and raises `ValueError` for negative minutes as documented.
3. `bookings/schedule.py` — `add_slot` appended to a mutable default argument, so repeated calls leaked state between callers. It now returns a brand-new list and never mutates the caller's input.

**Conventions applied (Acme review bot):** added full type annotations (every parameter plus return value) to all public functions in `billing.py`, `calendar_export.py`, `schedule.py` and `timeutil.py`; added `tests/test_regressions.py` with one test per fixed bug plus edge cases (do not modify existing tests); recorded every fix in `CHANGELOG.md` under `## Unreleased`.

**Files created/changed:** `workspace/bookings/billing.py`, `workspace/bookings/schedule.py`, `workspace/bookings/timeutil.py`, `workspace/bookings/calendar_export.py` (annotations only), `workspace/tests/test_regressions.py` (new), `workspace/CHANGELOG.md`. Existing tests were left untouched.