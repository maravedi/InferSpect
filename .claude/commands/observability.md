---
description: Check and enhance observability integration
---

Review and enhance observability for InferSpect:

1. **Langfuse Tracing**:
   - Are all LLM calls traced?
   - Is metadata included (tenant_id, user_id, session_id)?
   - Are costs tracked per request?
   - Are errors logged with full context?
   - Is latency measured at each step?

2. **Deepchecks Quality Validation**:
   - Quality checks implemented for LLM responses?
   - Toxicity detection enabled?
   - PII detection configured?
   - Response relevance measured?
   - Custom quality metrics defined?

3. **Promptfoo Testing**:
   - Prompt test suites created?
   - Regression tests for critical prompts?
   - A/B testing configured?
   - Prompt versions tracked?
   - Evaluation metrics defined?

4. **Logging**:
   - Structured logging implemented (JSON format)?
   - Appropriate log levels used?
   - No sensitive data in logs?
   - Correlation IDs for request tracing?
   - Tenant context in all logs?

5. **Metrics**:
   - Prometheus metrics exposed?
   - Key metrics tracked:
     - Request rate, error rate, latency
     - LLM costs per tenant
     - Cache hit rate
     - Quality scores
     - Quota usage
   - Custom metrics for business logic?

6. **Health Checks**:
   - /health endpoint implemented?
   - /ready endpoint for Kubernetes?
   - Dependency health checks (DB, Redis, LLM providers)?
   - Proper HTTP status codes?

7. **Alerting**:
   - Critical alerts defined?
   - Alert thresholds appropriate?
   - Alert fatigue avoided?
   - Runbooks for common alerts?

8. **Dashboards**:
   - Real-time monitoring dashboard?
   - Per-tenant usage dashboard?
   - Cost tracking dashboard?
   - Quality metrics visualization?

Provide recommendations to improve observability and monitoring.
