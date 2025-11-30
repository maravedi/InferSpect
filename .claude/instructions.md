# Claude Code Instructions for InferSpect

## Project Overview

InferSpect is an LLM proxy and observability platform designed to centralize infrastructure for managing, monitoring, and validating LLM interactions. The project integrates LiteLLM for unified LLM API access, Langfuse for observability, Deepchecks for quality validation, and Promptfoo for prompt testing, all deployed on Azure Kubernetes Service (AKS).

## Architecture & Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Dependency Management**: Poetry
- **Proxy**: LiteLLM (unified interface for 100+ LLM providers)
- **Observability**: Langfuse (request tracing, analytics)
- **Quality Checks**: Deepchecks (LLM validation, bias detection)
- **Prompt Testing**: Promptfoo (evaluation, regression testing)
- **Database**: PostgreSQL (metadata, multi-tenant data with Row-Level Security)
- **Cache**: Redis (response caching, rate limiting)
- **Cloud Platform**: Azure (AKS, Azure OpenAI, Key Vault, Blob Storage)
- **Infrastructure as Code**: Terraform
- **Testing**: pytest, pytest-asyncio, pytest-cov

## Development Workflow

This project uses an AI-powered development workflow with specialized provider roles:

### Provider Task Mapping

| Provider | Command | Best For |
|----------|---------|----------|
| **Jules** | `@jules spec` | Requirements analysis, technical specifications |
| **Jules** | `@jules plan` | System design, architecture planning |
| **Claude** | `@claude` | Deep reasoning, code review, implementation |
| **Cursor** | `@cursor verify` | Test runs, final validation |

**As Claude Code, your primary role is implementation and deep reasoning.**

## Key Documentation

- **Architecture**: See `docs/ARCHITECTURE.md` for comprehensive system design
- **Implementation Plan**: See `docs/IMPLEMENTATION_PLAN.md` for phased development approach
- **Cursor Rules**: See `.cursorrules` for Cursor IDE-specific guidelines (also applicable here)

## Development Guidelines

### Code Quality Standards

1. **Type Hints**: Always use type hints (checked with mypy)
2. **Testing**: Maintain >80% test coverage with pytest
3. **Code Style**:
   - Use `black` for formatting
   - Use `flake8` for linting
   - Use `isort` for import sorting
4. **Documentation**:
   - Add docstrings to all public functions/classes
   - Keep inline comments for complex logic only
   - Update relevant docs when making architectural changes

### Project Structure

```
inferspect/
├── src/inferspect/           # Main application code
│   ├── api/                  # FastAPI routes and middleware
│   ├── core/                 # Configuration, security, dependencies
│   ├── proxy/                # LiteLLM integration and routing
│   ├── models/               # SQLAlchemy models and Pydantic schemas
│   ├── services/             # Business logic services
│   ├── observability/        # Langfuse, Deepchecks, Promptfoo clients
│   └── utils/                # Utility functions
├── tests/                    # Test suites (unit, integration, e2e)
├── migrations/               # Alembic database migrations
├── scripts/                  # Utility scripts
├── config/                   # Configuration files
├── docs/                     # Documentation
└── infra/                    # Terraform infrastructure code
```

### Implementation Phases

The project follows a 4-phase implementation approach (16 weeks):

- **Phase 1**: Foundation & Core Proxy (Weeks 1-4)
- **Phase 2**: Observability Integration (Weeks 5-8)
- **Phase 3**: Multi-Tenant Azure Deployment (Weeks 9-12)
- **Phase 4**: Advanced Features & Optimization (Weeks 13-16)

**When implementing features, align with the current phase in `docs/IMPLEMENTATION_PLAN.md`.**

### Multi-Tenancy Considerations

This is a **multi-tenant platform**. Always consider:

1. **Data Isolation**: Use `tenant_id` in all database queries (Row-Level Security)
2. **Resource Quotas**: Enforce tenant-specific limits
3. **Cost Tracking**: Track usage and costs per tenant
4. **Security**: Validate tenant access for all operations
5. **Configuration**: Support tenant-specific configurations

### Security Best Practices

- **Never hardcode secrets** - use Azure Key Vault
- **Validate all inputs** - use Pydantic models
- **Implement proper authentication** - API keys, JWT tokens
- **Use encryption** - TLS 1.3 in transit, Azure Storage Encryption at rest
- **Log security events** - authentication failures, unauthorized access
- **Sanitize PII** - use Deepchecks for PII detection and redaction

### Testing Strategy

Follow the testing pyramid:
- **60% Unit Tests**: Test individual functions and services
- **30% Integration Tests**: Test API endpoints and database interactions
- **10% E2E Tests**: Test complete user workflows

**Commands**:
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov

# Run specific test file
poetry run pytest tests/unit/test_proxy.py

# Run tests matching a pattern
poetry run pytest -k "test_tenant"
```

### Common Commands

```bash
# Development
poetry install                    # Install dependencies
poetry run uvicorn src.inferspect.api.main:app --reload  # Run dev server
poetry run pytest                 # Run tests

# Code Quality
poetry run black .                # Format code
poetry run flake8 .               # Lint code
poetry run isort .                # Sort imports
poetry run mypy src/              # Type checking

# Database
poetry run alembic revision --autogenerate -m "description"  # Create migration
poetry run alembic upgrade head   # Apply migrations
poetry run alembic downgrade -1   # Rollback last migration

# Docker
docker-compose -f docker/docker-compose.dev.yml up  # Start dev environment
```

### GitHub Workflows

The project has automated workflows:

- **Claude Review** (`.github/workflows/claude_review.yml`): Auto-reviews PRs
- **Cursor Verify** (`.github/workflows/cursor_verify.yml`): Runs tests on PRs
- **Jules Planner/Spec**: Triggered via comments on issues/PRs

### When Implementing Features

1. **Check the Implementation Plan**: Reference `docs/IMPLEMENTATION_PLAN.md` to understand the current phase and priorities
2. **Follow the Architecture**: Reference `docs/ARCHITECTURE.md` for design decisions
3. **Write Tests First**: Consider TDD for complex features
4. **Update Documentation**: Keep docs in sync with code changes
5. **Consider Multi-Tenancy**: Always think about tenant isolation and quotas
6. **Add Observability**: Integrate with Langfuse for tracing
7. **Validate Quality**: Add Deepchecks validation where appropriate
8. **Test Prompts**: Use Promptfoo for prompt-related features

### LiteLLM Integration Notes

- Configuration is in `config/litellm_config.yaml`
- Supports OpenAI, Azure OpenAI, Anthropic, and 100+ other providers
- Built-in fallback logic: if primary model fails, automatically route to fallback
- Cost tracking is automatic - costs are logged per request
- Token counting is automatic - both input and output tokens

### Langfuse Integration Notes

- Track all LLM requests for observability
- Include metadata: `tenant_id`, `user_id`, `session_id`, custom tags
- Use for debugging latency issues, cost analysis, and usage patterns
- Create custom dashboards for different stakeholders

### Azure-Specific Considerations

- **Resource Naming**: Follow Azure naming conventions (lowercase, hyphens)
- **Managed Identities**: Use for service-to-service authentication
- **Key Vault**: Store all secrets (API keys, connection strings)
- **Regions**: Consider data residency requirements
- **Cost Management**: Tag all resources with `tenant_id`, `environment`, `project`

## Performance Targets

- **API Latency**: p95 < 500ms (excluding LLM processing time)
- **Throughput**: > 10,000 requests/second
- **Availability**: 99.9% uptime (SLA)
- **Cache Hit Rate**: > 40%
- **Error Rate**: < 0.1%

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're using `poetry run` or activate the virtual environment
2. **Database Connection**: Check PostgreSQL is running and credentials are correct
3. **Redis Connection**: Ensure Redis is running (check Docker Compose)
4. **Type Errors**: Run `mypy src/` to catch type issues early
5. **Test Failures**: Run tests in isolation to identify flaky tests

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Langfuse Documentation](https://langfuse.com/docs)
- [Deepchecks LLM](https://docs.deepchecks.com/stable/nlp/tutorials/index.html)
- [Promptfoo Documentation](https://www.promptfoo.dev/docs/intro)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure AKS Best Practices](https://learn.microsoft.com/en-us/azure/aks/)

## Questions?

If you're unsure about anything:
1. Check `docs/ARCHITECTURE.md` for design decisions
2. Check `docs/IMPLEMENTATION_PLAN.md` for feature priorities
3. Check existing code for patterns and conventions
4. Review the phase-specific tasks in the implementation plan
