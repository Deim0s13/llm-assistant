# Linting Issues Documentation

**Current Status**: 28 linting errors (48% improvement from original 54 errors)

**Last Updated**: $(date)

## Summary

This document catalogs all current linting issues in the codebase, their severity, impact on functionality, and suggested remediation approaches.

## Error Categories

### 1. Import Order Violations (E402) - 19 errors
**Severity**: Low (Cosmetic)
**Impact**: None - code functions normally
**Description**: Import statements are not at the top of the file

**Files Affected**:
- `config/settings_loader.py` (4 errors)
- `main.py` (15 errors)

**Example**:
```python
# ───────────────────────────────────────────────────────── Imports ──
import json  # ← This should be at the very top
import os
from typing import Any
```

**Suggested Fix**: Move all imports to the very top of each file, before any comments or docstrings.

---

### 2. Function Argument Count (PLR0913) - 4 errors
**Severity**: Medium (Code Quality)
**Impact**: None - code functions normally
**Description**: Functions have more than 5 parameters

**Files Affected**:
- `main.py` (3 errors)
- `memory/backends/redis_memory_backend.py` (1 error)

**Example**:
```python
def chat(
    msg: str,
    history: list[dict[str, Any]],
    temperature: float,
    max_new_tokens: int,
    top_p: float,
    top_k: int,           # ← 7th parameter
    repetition_penalty: float,  # ← 8th parameter
) -> tuple[str, list[dict[str, Any]]]:
```

**Suggested Fix**: Group related parameters into configuration objects or use dataclasses.

---

### 3. Import Placement (PLC0415) - 3 errors
**Severity**: Low (Code Quality)
**Impact**: None - code functions normally
**Description**: Import statements are inside functions instead of at module level

**Files Affected**:
- `tests/test_memory_backend.py` (2 errors)
- `tests/test_memory_toggle.py` (1 error)

**Example**:
```python
def restore_settings() -> Generator[None, None, None]:
    # snapshot & restore global SETTINGS so tests don't leak config
    from config.settings_loader import load_settings  # ← Should be at top
```

**Suggested Fix**: Move imports to the top of the file and use conditional imports if needed.

---

### 4. Line Length (E501) - 1 error
**Severity**: Low (Formatting)
**Impact**: None - code functions normally
**Description**: Line exceeds 100 character limit

**Files Affected**:
- `config/settings_loader.py` (1 error)

**Example**:
```python
"blocked_response_template": "I'm unable to respond to that request due to safety policies.",
#                                                                                     ^ 101 chars
```

**Suggested Fix**: Break long lines using parentheses or line continuation.

---

### 5. Duplicate Function (F811) - 1 error
**Severity**: Medium (Code Quality)
**Impact**: Potential confusion, one function shadows the other
**Description**: Function is defined twice with the same name

**Files Affected**:
- `main.py` (1 error)

**Example**:
```python
def count_tokens(text: str) -> int:  # ← First definition
    return len(tokenizer(text, return_tensors="pt").input_ids[0])

# ... later in the file ...

def count_tokens(text: str) -> int:  # ← Second definition (shadows the first)
    """Token count with a safe fallback when tokenizer isn't initialized (CI)."""
    if tokenizer is None:
        return max(1, len(text.split()))
    return len(tokenizer(text, return_tensors="pt").input_ids[0])
```

**Suggested Fix**: Remove the duplicate function definition.

---

## Detailed File Analysis

### config/settings_loader.py
- **4 E402 errors**: Import statements not at top
- **1 E501 error**: Line too long (101 > 100 chars)
- **Total**: 5 errors

**Current State**: Functional but imports are in wrong location
**Fix Difficulty**: Easy (move imports to top, break long line)

### main.py
- **15 E402 errors**: Import statements not at top
- **3 PLR0913 errors**: Functions with too many arguments
- **1 F811 error**: Duplicate function definition
- **Total**: 19 errors

**Current State**: Functional but imports are in wrong location
**Fix Difficulty**: Medium (imports easy, function refactoring harder)

### memory/backends/redis_memory_backend.py
- **1 PLR0913 error**: Constructor with too many arguments
- **Total**: 1 error

**Current State**: Functional
**Fix Difficulty**: Easy (group parameters into config object)

### Test Files
- **3 PLC0415 errors**: Imports inside functions
- **Total**: 3 errors

**Current State**: Functional
**Fix Difficulty**: Easy (move imports to top)

---

## Remediation Priority

### High Priority (Fix First)
1. **F811 - Duplicate function** - Could cause runtime issues
2. **E501 - Line length** - Simple formatting fix

### Medium Priority
3. **PLC0415 - Import placement** - Simple structural fix
4. **E402 - Import order** - Cosmetic but numerous

### Low Priority (Requires Refactoring)
5. **PLR0913 - Function arguments** - May require design changes

---

## Estimated Fix Time

- **Quick fixes** (E501, F811, PLC0415): 5-10 minutes
- **Import ordering** (E402): 15-20 minutes  
- **Function refactoring** (PLR0913): 30-45 minutes
- **Total**: 50-75 minutes for 100% clean codebase

---

## Risk Assessment

### Low Risk Fixes
- Moving imports to top of file
- Breaking long lines
- Removing duplicate functions
- Moving imports out of functions

### Medium Risk Fixes
- Refactoring function parameters (requires understanding function usage)

### High Risk Fixes
- None identified

---

## Recommendations

1. **Immediate**: Fix the duplicate function (F811) and line length (E501)
2. **Short term**: Fix import placement issues (PLC0415)
3. **Medium term**: Fix import ordering (E402)
4. **Long term**: Consider refactoring functions with many parameters (PLR0913)

---

## Notes

- All current errors are **non-blocking** - the code functions normally
- The 48% improvement (54 → 28 errors) represents significant progress
- Most remaining issues are cosmetic or code quality improvements
- The codebase is in a stable, working state
