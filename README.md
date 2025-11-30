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
| **Claude** | `@claude` | Documentation audits & updates |
| **Cursor** | `@cursor verify` | GPT-5.1 Codex review + automated verification |

### How It Works

- **Jules (Specifications & Planning)**:
  - Comment `@jules spec` on an issue or PR to generate technical specifications and requirements analysis
  - Comment `@jules plan` on an issue or PR to request system design and architecture planning
  - Uses Google Gemini 1.5 Pro for comprehensive analysis
  - Generates detailed specifications, implementation strategies, technology recommendations, and risk assessments
  - **Requires `JULES_API_KEY` secret** - See [setup guide](#jules-api-key-setup)
  - Powered by [jules-specs](https://pypi.org/project/jules-specs/) and [jules-planner](https://pypi.org/project/jules-planner/) packages

- **Claude (Documentation Refresh)**:
  - **Auto-Review:** Non-draft Pull Requests are automatically reviewed by Claude upon opening, synchronization, or when marked ready for review
  - **On-Demand:** Comment `@claude` in your Pull Request to request specific documentation updates
  - Claude keeps Markdown and planning docs current while flagging any issues for Cursor to address
  - **Note:** Draft PRs are excluded from automatic reviews to avoid premature feedback

- **Cursor (Verify)**: Comment `@cursor verify` on a PR to:
  - Invoke the Cursor Cloud GPT-5.1 Codex agent for a whole-repo security/quality review
  - Receive a Markdown report posted back to the PR with prioritized findings
  - Run the automated verification pipeline (`poetry run pytest` plus Bandit) to validate fixes

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

## Cursor Cloud API Key Setup

To enable the Cursor AI agent step inside `@cursor verify`, configure `CURSOR_CLOUD_API_KEY`:

1. **Create an API Key**
   - Visit [https://cursor.com](https://cursor.com) and open the Cloud dashboard
   - Generate a new API key with access to the Cursor Cloud Agent endpoints
2. **Add Repository Secret**
   - Go to Settings → Secrets and variables → Actions
   - Add `CURSOR_CLOUD_API_KEY` with the newly created key
   - (Optional) add `CURSOR_CLOUD_BASE_URL` if you are targeting a private Cursor Cloud deployment
3. **Trigger the Workflow**
   - Comment `@cursor verify` on any pull request
   - The workflow launches GPT-5.1 Codex via Cursor Cloud, posts the agent's Markdown report, then runs pytest + Bandit

If the secret is missing, the workflow skips the agent invocation but still performs the local test suite. Setting the secret is strongly recommended so you receive the automated review before the tests run.
