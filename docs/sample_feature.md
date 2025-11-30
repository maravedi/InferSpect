# Sample Feature Documentation

This document describes the sample feature implemented in `sample_code.py`.

> **WARNING:** This code contains intentional security vulnerabilities for testing the automated review workflows. **DO NOT use this code in production.**

## Purpose

This sample code serves as a test fixture to verify that:
- The Claude documentation review workflow correctly identifies and documents security issues
- The Cursor verification workflow detects and can fix security vulnerabilities
- Security scanning tools (e.g., Bandit) properly flag dangerous code patterns

## Functions

### `process_user_input(user_input)`

**Location:** `sample_code.py:1`

Processes user input by executing it as a shell command.

**Parameters:**
- `user_input` (str): Raw user input to be processed

**Returns:**
- `bool`: Always returns `True`

**Security Issues:**
- **Command Injection (CWE-78):** This function concatenates unsanitized user input directly into a shell command using `os.system()`. An attacker could inject arbitrary shell commands by providing input like `; rm -rf /` or `&& cat /etc/passwd`.
- **No Input Validation:** The function accepts any string without sanitization or validation.
- **Unsafe Command Execution:** Uses `os.system()` instead of safer alternatives like `subprocess.run()` with proper argument escaping.

**Example Attack Vector:**
```python
# Malicious input could execute arbitrary commands
process_user_input("test; cat /etc/passwd")
# Executes: echo test; cat /etc/passwd
```

**Recommended Fix (for reference - do not implement):**
- Use `subprocess.run()` with a list of arguments instead of string concatenation
- Validate and sanitize all user inputs
- Avoid shell execution entirely if possible
- Implement allowlisting of permitted commands/characters

### `add_numbers(a, b)`

**Location:** `sample_code.py:11`

Adds two numbers together.

**Parameters:**
- `a` (numeric): First number to add
- `b` (numeric): Second number to add

**Returns:**
- The sum of `a` and `b`

**Security:** This function has no security issues and serves as a baseline for safe code patterns.

## Testing Instructions

To test the workflow integration:

1. **Create a Pull Request** containing this code
2. **Verify Claude Review:** Claude should automatically identify and document the security vulnerability in `process_user_input`
3. **Trigger Cursor Verification:** Comment `@cursor verify` on the PR to trigger security fixes
4. **Verify Bandit Detection:** The workflow should run `bandit` and report the command injection vulnerability

## Expected Security Scan Results

When Bandit or similar tools scan this code, they should flag:
- **Issue:** Use of `os.system()` (B605/B607)
- **Severity:** High
- **Confidence:** High
- **Location:** `sample_code.py:8`

## Project Dependencies

The test project includes:
- **Python:** ^3.11
- **Dev Dependencies:** pytest ^8.0.0
- **Managed by:** Poetry (see `pyproject.toml`)

## Related Files

- **Source Code:** `sample_code.py`
- **Project Config:** `pyproject.toml`
- **Lock File:** `poetry.lock`
- **Workflow Docs:** `docs/TESTING_JULES_WORKFLOW.md`
