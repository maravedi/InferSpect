---
description: Plan the implementation of a feature or fix
---

Create a detailed implementation plan for the requested feature or fix:

1. **Understand the requirement**:
   - Clarify what needs to be implemented
   - Reference relevant documentation (ARCHITECTURE.md, IMPLEMENTATION_PLAN.md)
   - Identify the current implementation phase
   - Check for related existing code

2. **Design considerations**:
   - How does this fit into the multi-tenant architecture?
   - What are the security implications?
   - How will this be observed/monitored? (Langfuse)
   - What quality checks are needed? (Deepchecks)
   - How will this impact cost tracking?

3. **Implementation steps**:
   - Break down into specific, actionable tasks
   - Identify files that need to be created or modified
   - List required dependencies or configuration changes
   - Consider database migrations if needed
   - Plan for API changes (OpenAPI/schema updates)

4. **Testing strategy**:
   - What unit tests are needed?
   - What integration tests are needed?
   - What edge cases should be tested?
   - How to mock LLM providers?

5. **Deployment considerations**:
   - Any infrastructure changes needed?
   - Environment variables or secrets?
   - Database migrations?
   - Backward compatibility concerns?

6. **Success criteria**:
   - How will we know this is complete?
   - What metrics will we track?
   - What performance targets apply?

Present the plan as a structured, ordered list of tasks.
