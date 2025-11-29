# InferSpect

![InferSpect Logo](logo.jpg)

InferSpect is an LLM proxy and observability platform designed to centralize infrastructure for managing, monitoring, and validating LLM interactions.

> **Note:** This project is currently under development.

## Development Workflow

This repository uses an AI-powered development workflow with three specialized providers:

### Provider Task Mapping

| Provider | Trigger Command | Best For |
|----------|----------------|----------|
| **Jules** | `@jules plan` | System design, architecture planning |
| **Claude** | `@claude` | Deep reasoning, code review, implementation |
| **Cursor** | `@cursor verify` | Test runs, final validation |

### How It Works

- **Jules (Planning)**: Comment `@jules plan` on an issue or PR to request system design and architecture planning.
  - *Note: Currently in placeholder mode - acknowledgment only*

- **Claude (Review & Implementation)**:
  - **Auto-Review:** All Pull Requests are automatically reviewed by Claude upon opening or synchronization
  - **On-Demand:** Comment `@claude` in your Pull Request to request specific reviews or ask questions
  - Claude can analyze code, suggest improvements, and commit documentation updates

- **Cursor (Verification)**: Comment `@cursor verify` on a PR to:
  - Run the full test suite with pytest
  - Validate code changes
  - Report test results back to the PR
