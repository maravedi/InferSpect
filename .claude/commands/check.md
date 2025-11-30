---
description: Run code quality checks (formatting, linting, type checking)
---

Run all code quality checks for InferSpect:

1. **Code formatting (black)**:
   ```bash
   poetry run black . --check
   ```
   If not formatted, run: `poetry run black .`

2. **Import sorting (isort)**:
   ```bash
   poetry run isort . --check-only
   ```
   If not sorted, run: `poetry run isort .`

3. **Linting (flake8)**:
   ```bash
   poetry run flake8 .
   ```
   Check for code style violations and complexity issues

4. **Type checking (mypy)**:
   ```bash
   poetry run mypy src/
   ```
   Verify type hints are correct

5. **Security checks**:
   - Scan for hardcoded secrets
   - Check for common security vulnerabilities
   - Verify proper input validation

6. **Report results**:
   - Summarize all issues found
   - Prioritize critical issues
   - Provide specific fixes for each issue
   - Auto-fix formatting issues if requested

If all checks pass, confirm that code quality standards are met.
