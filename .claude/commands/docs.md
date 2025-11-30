---
description: Update or generate documentation for code changes
---

Update or generate documentation for InferSpect:

1. **Identify what documentation is needed**:
   - API changes? (OpenAPI/Swagger docs)
   - New features? (docs/ directory)
   - Architecture changes? (ARCHITECTURE.md)
   - Configuration changes? (.env.example, README.md)
   - Deployment changes? (deployment docs)

2. **API Documentation**:
   - Ensure FastAPI docstrings are complete
   - Verify OpenAPI schema is accurate
   - Add usage examples for new endpoints
   - Document authentication requirements
   - Include tenant-specific considerations

3. **Code Documentation**:
   - Add/update docstrings for public functions and classes
   - Use Google-style docstrings:
     ```python
     def function_name(param1: str, param2: int) -> bool:
         """Brief description.

         Longer description if needed.

         Args:
             param1: Description of param1
             param2: Description of param2

         Returns:
             Description of return value

         Raises:
             ValueError: When invalid input is provided
         """
     ```

4. **Architecture Documentation**:
   - Update ARCHITECTURE.md for significant changes
   - Document design decisions and trade-offs
   - Add/update diagrams if needed
   - Update component descriptions

5. **README Updates**:
   - Update setup instructions if changed
   - Add new features to feature list
   - Update commands if new ones added
   - Keep provider workflow documentation current

6. **Configuration Documentation**:
   - Update .env.example with new variables
   - Document configuration options
   - Include Azure-specific settings
   - Document tenant configuration options

7. **Deployment Documentation**:
   - Update deployment guides
   - Document infrastructure changes
   - Update Terraform/Kubernetes docs
   - Include troubleshooting steps

Generate or update the appropriate documentation based on recent changes.
