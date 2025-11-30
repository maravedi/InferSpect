---
description: Perform a comprehensive code review of recent changes
---

Perform a comprehensive code review focusing on:

1. **InferSpect-Specific Concerns**:
   - Multi-tenancy: Verify tenant_id is used for data isolation
   - Security: Check for hardcoded secrets, validate input sanitization
   - Cost tracking: Ensure LLM usage is tracked per tenant
   - Observability: Verify Langfuse tracing is implemented

2. **Code Quality**:
   - Type hints: Verify all functions have proper type annotations
   - Error handling: Check for proper exception handling
   - Testing: Ensure test coverage for new code
   - Documentation: Verify docstrings for public APIs

3. **Architecture Alignment**:
   - Follows the structure in docs/ARCHITECTURE.md
   - Aligns with current implementation phase
   - Follows FastAPI best practices
   - Proper use of Pydantic models for validation

4. **Performance**:
   - Database queries are optimized (consider N+1 queries)
   - Caching is implemented where appropriate
   - Async/await is used correctly for I/O operations
   - No blocking operations in async functions

5. **Azure & Cloud Best Practices**:
   - Secrets use Azure Key Vault
   - Proper use of managed identities
   - Resource tagging for cost tracking
   - Follows Azure naming conventions

Provide specific, actionable feedback with file paths and line numbers.
