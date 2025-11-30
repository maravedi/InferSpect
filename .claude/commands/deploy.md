---
description: Provide deployment guidance and pre-deployment checks
---

Provide deployment guidance for InferSpect:

1. **Pre-deployment checks**:
   - All tests passing?
   - Code quality checks pass?
   - Documentation updated?
   - Database migrations ready?
   - Environment variables documented?

2. **Deployment environment**:
   - Which environment? (dev/staging/prod)
   - Azure resources provisioned?
   - Kubernetes manifests updated?
   - Secrets in Azure Key Vault?

3. **Database migrations**:
   ```bash
   # Generate migration
   poetry run alembic revision --autogenerate -m "description"

   # Review migration
   # Check migrations/ directory

   # Apply migration
   poetry run alembic upgrade head
   ```

4. **Docker build**:
   ```bash
   # Build image
   docker build -t inferspect:latest -f docker/Dockerfile .

   # Tag for ACR
   docker tag inferspect:latest <acr-name>.azurecr.io/inferspect:<version>

   # Push to ACR
   docker push <acr-name>.azurecr.io/inferspect:<version>
   ```

5. **Kubernetes deployment**:
   - Update deployment manifests with new image tag
   - Apply ConfigMaps and Secrets first
   - Deploy using kubectl or Helm
   - Monitor pod rollout status

6. **Post-deployment verification**:
   - Health check endpoint responding?
   - Logs looking normal?
   - Metrics being collected?
   - Run smoke tests
   - Verify multi-tenant isolation

7. **Rollback plan**:
   - Document how to rollback if issues occur
   - Keep previous image tags available
   - Have database rollback scripts ready

Provide environment-specific deployment commands and verification steps.
