# GitHub Workflows Documentation

This directory contains GitHub Actions workflows that provide AI-powered development assistance for this repository. Each workflow offers different capabilities to help with code review, testing, and architecture planning.

## Available Workflows

- **[Claude PR Review](#claude-pr-review)** - Documentation-only PR updates using Claude AI
- **[Cursor Fix & Verify](#cursor-fix--verify)** - Implementation fixes, security review, and verification triggered via comments
- **[Jules Spec & Plan](#jules-spec--plan)** - Architecture planning and specification generation using Google's Jules AI

---

## Claude PR Review

**Workflow File:** `.github/workflows/claude_review.yml`

### Overview

This workflow uses Anthropic's Claude AI to automatically review pull requests for documentation accuracy. Claude now focuses solely on keeping written assets aligned with the latest code changes while deferring bug fixes and security work to Cursor.

### Features

- **Automatic PR Documentation Pass**: Runs when PRs are opened, updated, reopened, or marked ready
- **Docs-Only Commits**: Updates Markdown and `docs/` files without touching application code
- **Bug/Security Escalation**: Leaves review comments directing maintainers to run `@cursor verify` for implementation fixes
- **On-Demand Doc Refresh**: Comment `@claude` on any PR to request targeted documentation updates

### How to Use

#### Automatic Review

The workflow automatically runs when you:
- Open a new pull request
- Push new commits to an existing PR
- Reopen a PR
- Mark a draft PR as ready for review

#### Comment-Triggered Review

Comment `@claude` on any pull request with specific instructions, and Claude will:
- Address your documentation-specific request
- Update Markdown and `docs/` artifacts while leaving code changes to Cursor
- Highlight any blocking bugs or security issues so Cursor can follow up

**Example:**
```
@claude Please review the error handling in the authentication module
```

### Setup Instructions

1. **Get an Anthropic API Key**
   - Go to [console.anthropic.com](https://console.anthropic.com)
   - Sign up or log in to your account
   - Navigate to API Keys section
   - Create a new API key

2. **Configure Repository Secret**
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `ANTHROPIC_API_KEY`
   - Value: [paste your Anthropic API key]
   - Click "Add secret"

### What Claude Reviews

1. **Documentation Accuracy**: Ensures README.md, implementation plans, and other Markdown stay aligned
2. **Context Awareness**: Reads code changes to understand behavior without modifying code
3. **Issue Escalation**: Flags bugs/security gaps via comments so Cursor can take action
4. **Communication**: Summarizes doc updates and outstanding implementation follow-ups

### Technical Details

- Uses `anthropics/claude-code-action@v1`
- Requires permissions: `contents: write`, `pull-requests: write`, `id-token: write`
- Automatically commits and pushes documentation updates
- Configured with git user: "Claude Bot"

---

## Cursor Fix & Verify

**Workflow File:** `.github/workflows/cursor_verify.yml`

### Overview

Responds to `@cursor verify` comments by having Cursor apply implementation fixes, perform a security review, and run the automated test suite. Cursor now owns code changes while Claude focuses on documentation.

### Features

- **Implementation Ownership**: Cursor applies bug fixes and security hardening directly to the PR branch
- **Security Review**: Executes Bandit after AI modifications to catch common vulnerabilities
- **Test Verification**: Runs `poetry run pytest` to validate the updated code
- **Automated Commits & Reporting**: Pushes Cursor changes and posts an execution summary back to the PR

### How to Use

Comment `@cursor verify` on any pull request to run the full Cursor fix-and-verify pipeline.

**Example:**
```
@cursor verify
```

The workflow:
1. Checks out the PR branch with write permissions
2. Runs the Cursor AI action tuned for bug fixes and security remediation
3. Installs Poetry plus project dependencies
4. Executes pytest
5. Scans the repository with Bandit
6. Commits/pushes resulting code changes
7. Posts a status comment summarizing the outcome

### Setup Instructions

- Requires the shared `ANTHROPIC_API_KEY` secret (same as Claude)
- Uses the default `GITHUB_TOKEN` for checkout and pushes

### Requirements

- Project must have a `pyproject.toml` file
- Tests should be runnable via `poetry run pytest`
- Python 3.11 compatible

### Technical Details

- Triggered via issue comments containing `@cursor verify`
- Uses `anthropics/claude-code-action@v1` with a Cursor-specific prompt
- Installs Poetry from the official installer
- Reports status regardless of test outcome (`if: always()`)

---

## Jules Spec & Plan

**Workflow File:** `.github/workflows/jules_plan.yml`

### Overview

This workflow integrates with Google's Jules AI to provide architecture planning and specification generation directly in GitHub issues. Jules can help design systems, plan implementations, and create detailed technical specifications.

### Features

- **Architecture Planning**: Generate comprehensive system design plans
- **Specification Generation**: Create detailed technical specifications
- **Technology Recommendations**: Get suggestions for tech stack and tools
- **Implementation Strategy**: Receive step-by-step implementation guidance

### How to Use

#### Generate a Specification

Comment `@jules spec` on any GitHub issue to generate a technical specification.

Jules will analyze your issue and provide:
- Detailed technical specification
- API contracts and interfaces
- Data models and schemas
- Integration requirements

#### Generate an Architecture Plan

Comment `@jules plan` on any GitHub issue to generate an architecture plan.

Jules will provide:
1. Architecture overview
2. Technology stack recommendations
3. Implementation strategy
4. Design decisions and trade-offs
5. Security and performance considerations
6. Risk analysis
7. Actionable next steps

### Setup Instructions

#### Prerequisites

1. **Install the Jules GitHub App**
   - Go to [jules.google.com](https://jules.google.com)
   - Sign in with your Google account
   - Install the Jules GitHub app for this repository
   - Follow the installation prompts

2. **Generate a Jules API Key**
   - Go to [Jules Settings](https://jules.google.com/settings#api)
   - Click "Create API Key"
   - Copy the generated API key
   - **Important:** Keep this key secure - you can have at most 3 API keys at a time

3. **Configure Repository Secret**
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `JULES_API_KEY`
   - Value: [paste your Jules API key]
   - Click "Add secret"

#### Verification

To verify the setup:
1. Create a test issue or use an existing one
2. Comment `@jules spec` or `@jules plan` on the issue
3. Wait 1-2 minutes for Jules to generate the response
4. The result will be posted as a comment on the issue

### Technical Details

- **API**: Uses Jules API v1alpha (`https://jules.googleapis.com/v1alpha`)
- **Packages**:
  - `jules-specs` - for specification generation
  - `jules-planner` - for architecture planning
- **Permissions**: `contents: read`, `issues: write`, `pull-requests: write`
- **Python Version**: 3.11

### Session-Based Architecture

Jules uses a session-based approach:
- **Source**: GitHub repository connected to Jules
- **Session**: A continuous unit of work (like a chat session)
- **Activity**: Individual actions within a session (spec/plan generation, progress updates, etc.)

This allows Jules to generate comprehensive outputs and even create pull requests with implementation code.

---

## Troubleshooting

### Claude PR Review

#### Error: "Missing ANTHROPIC_API_KEY"
**Cause:** The API key is not configured in repository secrets.

**Fix:**
1. Get an API key from [console.anthropic.com](https://console.anthropic.com)
2. Add it as `ANTHROPIC_API_KEY` in repository secrets

#### No Response After @claude Comment
**Possible causes:**
- The workflow may still be running (check Actions tab)
- The comment might not contain `@claude`
- Permissions might be insufficient

**Fix:** Check the workflow run logs in the Actions tab for detailed error messages.

---

### Cursor Fix & Verify

#### Workflow Fails Before Tests
**Possible causes:**
- Missing `ANTHROPIC_API_KEY` secret (shared with Claude)
- `@cursor verify` comment issued on an issue (workflow requires a PR)
- Cursor action could not apply code changes cleanly

**Fix:** Confirm the secret is configured, ensure the comment is on a PR, and inspect workflow logs for merge conflicts.

#### Tests or Bandit Fail
**Cause:** Cursor changes introduced failing tests or security findings.

**Fix:** Review the workflow logs, address the reported failures locally, and re-run `@cursor verify`.

---

### Jules Spec & Plan

#### Error: "Repository Not Found"
**Cause:** The Jules GitHub app is not installed for this repository.

**Fix:**
1. Visit [jules.google.com](https://jules.google.com)
2. Install the Jules GitHub app
3. Grant access to this repository

#### Error: "401 Unauthorized"
**Cause:** The `JULES_API_KEY` is invalid, expired, or not configured.

**Fix:**
1. Go to [Jules Settings](https://jules.google.com/settings#api)
2. Create a new API key
3. Update the `JULES_API_KEY` secret in repository settings

#### No Response After Comment
**Possible causes:**
- The workflow may still be running (check Actions tab)
- The `JULES_API_KEY` secret might not be configured
- The Jules GitHub app might not be installed

**Fix:** Check the workflow run logs in the Actions tab for detailed error messages.

---

## Security Notes

### API Key Management
- **Never commit API keys to your repository**
- Store all API keys in GitHub repository secrets
- Rotate API keys regularly
- Google and Anthropic automatically disable publicly exposed API keys

### Workflow Permissions
All workflows run with minimal required permissions:
- **Claude PR Review**: Can write to contents and PRs to commit documentation updates
- **Cursor Fix & Verify**: Requires contents/pull-request write access to push implementation fixes
- **Jules Spec & Plan**: Can write to issues/PRs but only reads repository contents

---

## Resources

### Claude
- [Anthropic Console](https://console.anthropic.com)
- [Claude API Documentation](https://docs.anthropic.com)
- [Claude Code Action](https://github.com/anthropics/claude-code-action)

### Cursor
- [Cursor IDE](https://cursor.sh)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [pytest Documentation](https://docs.pytest.org)

### Jules
- [Jules Web App](https://jules.google.com)
- [Jules API Reference](https://developers.google.com/jules/api/reference/rest)
- [Jules Documentation](https://jules.google/docs)
- [jules-specs Package](https://pypi.org/project/jules-specs/)
- [jules-planner Package](https://pypi.org/project/jules-planner/)

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

## API Status

> **Note:** The Jules API is currently in alpha release. Specifications and behavior may change as Google works toward stabilization.

> **Note:** All workflows are subject to GitHub Actions usage limits and billing. See [GitHub Actions pricing](https://github.com/pricing) for details.
