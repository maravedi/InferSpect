# InferSpect

![InferSpect Logo](assets/logo.jpg)

InferSpect is an LLM proxy and observability platform designed to centralize infrastructure for managing, monitoring, and validating LLM interactions.

> **Note:** This project is currently under development.

## Development Workflow

This repository uses an AI-powered development workflow with three specialized providers:

### Provider Task Mapping

| Provider | Trigger Command | Best For |
|----------|----------------|----------|
| **Jules** | `@jules spec` | Requirements analysis, technical specifications |
| **Jules** | `@jules plan` | System design, architecture planning |
| **Claude** | `@claude` | Deep reasoning, code review, implementation |
| **Cursor** | `@cursor verify` | Test runs, final validation |

### How It Works

- **Jules (Specifications & Planning)**:
  - Comment `@jules spec` on an issue or PR to generate technical specifications and requirements analysis
  - Comment `@jules plan` on an issue or PR to request system design and architecture planning
  - Uses Google Gemini 1.5 Pro for comprehensive analysis
  - Generates detailed specifications, implementation strategies, technology recommendations, and risk assessments
  - **Requires `JULES_API_KEY` secret** - See [setup guide](#jules-api-key-setup)
  - Powered by [jules-specs](https://pypi.org/project/jules-specs/) and [jules-planner](https://pypi.org/project/jules-planner/) packages

- **Claude (Review & Implementation)**:
  - **Auto-Review:** All Pull Requests are automatically reviewed by Claude upon opening or synchronization
  - **On-Demand:** Comment `@claude` in your Pull Request to request specific reviews or ask questions
  - Claude can analyze code, suggest improvements, and commit documentation updates

- **Cursor (Verification)**: Comment `@cursor verify` on a PR to:
  - Run the full test suite with pytest
  - Validate code changes
  - Report test results back to the PR

## Jules API Key Setup

To enable Jules architecture planning, you need to configure the `JULES_API_KEY` secret:

1. **Get a Gemini API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated API key

2. **Add Secret to GitHub:**
   - Go to your repository Settings
   - Navigate to "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Name: `JULES_API_KEY`
   - Value: Paste your Gemini API key
   - Click "Add secret"

3. **Test the Integration:**
   - Create a test issue or PR
   - Comment `@jules spec` to generate technical specifications
   - Comment `@jules plan` to generate a comprehensive architecture plan

**Note:** The Gemini API has usage limits. Check the [pricing page](https://ai.google.dev/pricing) for details.
