# Claude Code Configuration for InferSpect

This directory contains Claude Code-specific configuration, instructions, and custom commands for the InferSpect project.

## Directory Structure

```
.claude/
├── README.md              # This file
├── instructions.md        # Project-specific instructions for Claude Code
├── commands/              # Custom slash commands
│   ├── review.md         # Code review command
│   ├── test.md           # Testing command
│   ├── plan.md           # Implementation planning
│   ├── check.md          # Code quality checks
│   ├── deploy.md         # Deployment guidance
│   ├── docs.md           # Documentation updates
│   ├── security.md       # Security analysis
│   └── observability.md  # Observability checks
└── hooks/                # Event hooks (optional, currently empty)
```

## Custom Slash Commands

Use these commands by typing them in your conversation with Claude Code:

### `/review`
Performs a comprehensive code review focusing on:
- Multi-tenancy and security
- InferSpect-specific patterns (LiteLLM, Langfuse, etc.)
- Code quality and testing
- Architecture alignment
- Performance considerations

### `/test`
Runs tests and analyzes results:
- Identifies relevant tests for changes
- Executes pytest with coverage
- Analyzes failures and suggests fixes
- Checks test quality

### `/plan`
Creates detailed implementation plans:
- Breaks down features into tasks
- Considers multi-tenant architecture
- Plans testing strategy
- Addresses deployment concerns
- Defines success criteria

### `/check`
Runs all code quality checks:
- black (formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- Security scanning

### `/deploy`
Provides deployment guidance:
- Pre-deployment checklist
- Environment-specific instructions
- Database migrations
- Docker builds
- Kubernetes deployment
- Post-deployment verification

### `/docs`
Updates or generates documentation:
- API documentation (OpenAPI)
- Code docstrings
- Architecture documentation
- Configuration guides
- Deployment documentation

### `/security`
Performs security analysis:
- Secrets management review
- Input validation checks
- Authentication/authorization review
- Multi-tenancy security
- Dependency scanning
- Azure security best practices

### `/observability`
Reviews observability integration:
- Langfuse tracing coverage
- Deepchecks quality validation
- Promptfoo testing
- Logging and metrics
- Health checks and alerting

## Usage

To use a command, simply type it in your conversation:

```
/review
```

Or combine with specific requests:

```
/plan
I need to add rate limiting per tenant with Redis
```

## Instructions File

The `instructions.md` file contains:
- Project overview and architecture
- Development guidelines
- Code quality standards
- Multi-tenancy considerations
- Security best practices
- Testing strategies
- Common commands and troubleshooting

Claude Code automatically reads this file to understand project context.

## Alignment with Cursor Rules

The `.claude/` configuration complements the `.cursorrules` file:
- `.cursorrules`: For Cursor IDE users
- `.claude/`: For Claude Code users

Both align with the same project standards and development workflow.

## Development Workflow Integration

InferSpect uses an AI-powered development workflow:

| Provider | Command | Best For |
|----------|---------|----------|
| **Jules** | `@jules spec` | Requirements analysis |
| **Jules** | `@jules plan` | System design |
| **Claude** | `@claude` | Implementation, code review |
| **Cursor** | `@cursor verify` | Test validation |

Claude Code's role is **implementation and deep reasoning**.

## Contributing

When adding new commands:
1. Create a new `.md` file in `commands/`
2. Include a description in the frontmatter:
   ```yaml
   ---
   description: Brief description of the command
   ---
   ```
3. Write clear, actionable instructions
4. Update this README with the new command

## Resources

- **Architecture**: `docs/ARCHITECTURE.md`
- **Implementation Plan**: `docs/IMPLEMENTATION_PLAN.md`
- **Project README**: `README.md`
- **Cursor Rules**: `.cursorrules`
