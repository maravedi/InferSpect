---
description: Run tests and analyze results
---

Run the appropriate tests for the current changes:

1. **Identify what to test**:
   - Determine which files have changed
   - Identify relevant test files
   - Check if new tests are needed

2. **Run tests**:
   ```bash
   poetry run pytest --cov
   ```

3. **Analyze results**:
   - Report test failures with details
   - Check code coverage (target: >80%)
   - Identify missing test coverage
   - Suggest additional test cases if needed

4. **Test quality checks**:
   - Verify tests follow AAA pattern (Arrange, Act, Assert)
   - Check for proper mocking of external services (LLM APIs)
   - Ensure multi-tenant scenarios are tested
   - Verify async tests use pytest-asyncio correctly

5. **If tests fail**:
   - Analyze the failure reason
   - Suggest fixes
   - Check if it's a real bug or test issue

Provide a summary of test results and recommendations.
