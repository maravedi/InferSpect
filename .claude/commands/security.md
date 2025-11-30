---
description: Perform security analysis and checks
---

Perform a security analysis for InferSpect:

1. **Secrets Management**:
   - Scan for hardcoded secrets (API keys, passwords, tokens)
   - Verify all secrets use Azure Key Vault
   - Check .env files are in .gitignore
   - Ensure no secrets in logs or error messages

2. **Input Validation**:
   - All user inputs validated with Pydantic models
   - SQL injection prevention (using SQLAlchemy ORM)
   - XSS prevention in API responses
   - Command injection prevention
   - Path traversal prevention

3. **Authentication & Authorization**:
   - API key authentication properly implemented
   - JWT tokens have appropriate expiry
   - Tenant isolation enforced in all queries
   - Role-based access control (RBAC) working
   - No authentication bypass vulnerabilities

4. **Multi-Tenancy Security**:
   - Tenant_id used in all data queries
   - No cross-tenant data leakage
   - Tenant-specific rate limiting enforced
   - Proper tenant validation in middleware

5. **Data Protection**:
   - PII detection enabled (Deepchecks)
   - Encryption at rest (Azure Storage)
   - Encryption in transit (TLS 1.3)
   - Database connections encrypted
   - No sensitive data in logs

6. **Dependency Security**:
   ```bash
   # Check for vulnerable dependencies
   poetry show --outdated
   # Consider: poetry add --group dev safety
   # safety check
   ```

7. **Azure Security**:
   - Managed identities used where possible
   - Network security groups configured
   - Private endpoints for sensitive services
   - Key Vault access policies restrictive
   - No overly permissive IAM roles

8. **API Security**:
   - Rate limiting implemented
   - CORS properly configured
   - Security headers present
   - No verbose error messages in production
   - Input size limits enforced

Provide a security report with findings categorized by severity (Critical, High, Medium, Low).
