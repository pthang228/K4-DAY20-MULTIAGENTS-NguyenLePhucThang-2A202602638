### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


Execution boundary: inspect and modify only relative paths under workspace/ and, when present, read skill instructions only under skills/. Never inspect parent, home, temporary, repository, or other absolute paths, and never search for hidden checks, evaluator code, or undisclosed conventions. Do not repeat a command whose result is already sufficient. Once the requested outputs are complete, validate them once and stop.

### Assistant
I'll start by exploring the workspace structure.

### Tool call: ls
{"path": "workspace"}

### Tool call: glob
{"pattern": "**/*", "path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-312.pyc', '/workspace/bookings/__pycache__/billing.cpython-312.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-312.pyc', '/workspace/bookings/__pycache__/schedule.cpython-312.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-312.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-312-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

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
{"file_path": "workspace/bookings/__init__.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

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
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

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

### Tool call: ls
{"path": "skills"}

### Tool call: execute
{"command": "ls -la"}

### Tool result
Error: Path '/skills': path_not_found

### Tool result
total 0
drwxr-xr-x 1 ADMIN 197121 0 Oct  6 12:37 .
drwxr-xr-x 1 ADMIN 197121 0 Sep 10 13:08 ..
drwxr-xr-x 1 ADMIN 197121 0 Oct  6 11:49 workspace

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -40"}

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
Now let me look at the current implementations and run the tests (done). Let me apply fixes.

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n# Each pattern must match the whole duration string (\"fullmatch\").\n# Patterns are tried in order; the first one that matches wins.\n_FORMATS = (\n    re.compile(r\"(?P<hours>\\d+)h(?P<minutes>\\d+)m\"),\n    re.compile(r\"(?P<hours>\\d+):(?P<minutes>\\d+)\"),\n    re.compile(r\"(?P<hours>\\d+)h\"),\n    re.compile(r\"(?P<minutes>\\d+)m\"),\n    re.compile(r\"(?P<minutes>\\d+)\"),\n)\n\n\ndef parse_duration(text: str) -> int:\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    stripped = text.strip()\n    for pattern in _FORMATS:\n        match = pattern.fullmatch(stripped)\n        if match is not None:\n            parts = match.groupdict()\n            return int(parts.get(\"hours\") or 0) * 60 + int(\n                parts.get(\"minutes\") or 0\n            )\n    raise ValueError(f\"bad duration: {text!r}\")\n"}

### Tool call: write_file
{"file_path": "workspace/bookings/billing.py", "content": "\"\"\"Billing rules.\"\"\"\nimport math\n\n\ndef billable_blocks(minutes: float, block: float = 15) -> int:\n    \"\"\"Number of billable blocks for a booking.\n\n    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    return math.ceil(minutes / block)\n"}

### Tool call: write_file
{"file_path": "workspace/bookings/schedule.py", "content": "\"\"\"Schedule helpers.\"\"\"\nfrom typing import Iterable, List, Optional\n\nfrom .timeutil import parse_duration\n\n\ndef total_minutes(durations: Iterable[str]) -> int:\n    \"\"\"Total minutes of a list of duration strings.\"\"\"\n    return sum(parse_duration(d) for d in durations)\n\n\ndef add_slot(slot: str, slots: Optional[Iterable[str]] = None) -> List[str]:\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return [*(slots or []), slot]\n"}

### Tool call: write_file
{"file_path": "workspace/bookings/calendar_export.py", "content": "\"\"\"Calendar export.\"\"\"\nfrom .timeutil import parse_duration\n\n\ndef slot_end(start_minute: int, duration_text: str) -> int:\n    \"\"\"Minute of the day at which a slot ends.\"\"\"\n    return start_minute + parse_duration(duration_text)\n"}

### Tool result
Updated file /workspace/bookings/timeutil.py

### Tool result
Updated file /workspace/bookings/billing.py

### Tool result
Updated file /workspace/bookings/schedule.py

### Tool result
Updated file /workspace/bookings/calendar_export.py

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -10"}

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom bookings.timeutil import parse_duration\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.calendar_export import slot_end\nfor t in ['1h30m','2h','45m','1:30','45',' 2h ','0m','2h0m']:\n    print(repr(t), parse_duration(t))\nfor bad in ['', 'x', '1x', '-5m', 'h']:\n    try:\n        parse_duration(bad); print('NO RAISE', repr(bad))\n    except ValueError as e: print('ok raise', repr(bad))\nprint(billable_blocks(16), billable_blocks(15), billable_blocks(0), billable_blocks(20), billable_blocks(45))\ntry:\n    billable_blocks(-1); print('NO RAISE neg')\nexcept ValueError: print('ok neg raise')\nprint(add_slot('a'), add_slot('b'))\nprint(add_slot('c', ['x','y']))\nprint(total_minutes(['1h30m','2h']), slot_end(600,'1h30m'))\nprint(add_slot('a') == ['a'])\n\""}

### Tool result
...                                                                      [100%]
3 passed in 0.05s

[Command succeeded with exit code 0]

### Tool result
<no output>
[Command succeeded with exit code 0]

### Tool call: write_file
{"content": "from bookings.timeutil import parse_duration\nfrom bookings.billing import billable_blocks\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.calendar_export import slot_end\n\nfor t in ['1h30m', '2h', '45m', '1:30', '45', ' 2h ', '0m', '2h0m']:\n    print(repr(t), parse_duration(t))\nfor bad in ['', 'x', '1x', '-5m', 'h']:\n    try:\n        parse_duration(bad)\n        print('NO RAISE', repr(bad))\n    except ValueError:\n        print('ok raise', repr(bad))\nprint(billable_blocks(16), billable_blocks(15), billable_blocks(0),\n      billable_blocks(20), billable_blocks(45))\ntry:\n    billable_blocks(-1)\n    print('NO RAISE neg')\nexcept ValueError:\n    print('ok neg raise')\nprint(add_slot('a'), add_slot('b'))\nprint(add_slot('c', ['x', 'y']))\nprint(total_minutes(['1h30m', '2h']), slot_end(600, '1h30m'))\n", "file_path": "workspace/_check.py"}

### Tool result
Updated file /workspace/_check.py

### Tool call: execute
{"command": "cd workspace && python _check.py"}

### Tool result
'1h30m' 90
'2h' 120
'45m' 45
'1:30' 90
'45' 45
' 2h ' 120
'0m' 0
'2h0m' 120
ok raise ''
ok raise 'x'
ok raise '1x'
ok raise '-5m'
ok raise 'h'
2 1 0 2 3
ok neg raise
['a'] ['b']
['x', 'y', 'c']
210 690

[Command succeeded with exit code 0]

### Assistant
All docstring behaviors verified. Cleaning up the temporary check script.

### Tool call: delete
{"file_path": "workspace/_check.py"}

### Tool result
Deleted /workspace/_check.py

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- Fix `parse_duration` to accept all documented formats (`1h30m`, `2h`, `45m`,\n  `1:30`, `45`, ignoring surrounding whitespace).\n- Fix `billable_blocks` to always round up and to reject negative minutes.\n- Fix `add_slot` so separate calls no longer share state.\n"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -5"}

### Tool result
...                                                                      [100%]
3 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
All tests pass. Summary of changes:

**Bugs found and fixed (all in `workspace/bookings/`):**

1. **`timeutil.py` — `parse_duration`** only matched `"1h30m"`, contradicting its docstring (which documents `"2h"`, `"45m"`, `"1:30"`, `"45"`, and whitespace tolerance). Now it strips whitespace and tries a tuple of compiled `re.fullmatch` patterns in order (`h+m`, `h:mm`, `h`, `m`, bare minutes), defaulting missing components to 0, and still raises `ValueError` for anything unrecognized.

2. **`billing.py` — `billable_blocks`** used `round()` (banker's rounding, so `20/15 → 1`), but the docstring says always round **up** and raise on negative minutes. Now uses `math.ceil(minutes / block)` and raises `ValueError` when `minutes < 0`.

3. **`schedule.py` — `add_slot`** used a mutable default argument (`slots=[]`) and mutated it in place, so calls shared state and it returned the default list rather than a new one. Now the default is `None` and it returns a brand-new list via `[*(slots or []), slot]`, preserving caller-supplied slots without mutating them.

4. **`calendar_export.py` — `slot_end`** was already correct; I left the logic unchanged (it now correctly handles all formats via the fixed `parse_duration`).

I also added type hints for clarity, documented the new behavior in `CHANGELOG.md`, and verified every documented example plus edge cases (`""`, `"x"`, negatives, `billable_blocks(16/15/0)`, repeated `add_slot` calls, caller-supplied slot lists). `tests/` was not touched, a