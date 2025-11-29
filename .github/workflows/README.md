# Jules Architecture Planning Workflow

This workflow integrates with the [official Jules API](https://developers.google.com/jules/api) to provide AI-powered architecture planning and design assistance directly in GitHub issues.

## What is Jules?

Jules is Google's AI coding agent that can help with:
- System design and architecture planning
- Code implementation and refactoring
- Bug fixes and code reviews
- Development task automation

## How to Use

Comment `@jules plan` on any GitHub issue to trigger Jules to generate a comprehensive architecture plan.

Jules will analyze your issue and provide:
1. Architecture overview
2. Technology stack recommendations
3. Implementation strategy
4. Design decisions and trade-offs
5. Security and performance considerations
6. Risk analysis
7. Actionable next steps

## Setup Instructions

### Prerequisites

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
   - Go to your repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `JULES_API_KEY`
   - Value: [paste your Jules API key]
   - Click "Add secret"

### Verification

To verify the setup:
1. Create a test issue or use an existing one
2. Comment `@jules plan` on the issue
3. Wait 1-2 minutes for Jules to generate the plan
4. The plan will be posted as a comment on the issue

## Troubleshooting

### Error: "Repository Not Found"

**Cause:** The Jules GitHub app is not installed for this repository.

**Fix:**
1. Visit [jules.google.com](https://jules.google.com)
2. Install the Jules GitHub app
3. Grant access to this repository

### Error: "401 Unauthorized"

**Cause:** The `JULES_API_KEY` is invalid, expired, or not configured.

**Fix:**
1. Go to [Jules Settings](https://jules.google.com/settings#api)
2. Create a new API key
3. Update the `JULES_API_KEY` secret in repository settings

### No Response After Comment

**Possible causes:**
- The workflow may still be running (check Actions tab)
- The `JULES_API_KEY` secret might not be configured
- The Jules GitHub app might not be installed

**Fix:** Check the workflow run logs in the Actions tab for detailed error messages.

## Technical Details

### API Documentation

This workflow uses the official Jules API (v1alpha):
- Base URL: `https://jules.googleapis.com/v1alpha`
- Authentication: `X-Goog-Api-Key` header
- Documentation: [developers.google.com/jules/api](https://developers.google.com/jules/api)

### Workflow Components

1. **Workflow File:** `.github/workflows/jules_plan.yml`
   - Triggered by issue comments containing `@jules plan`
   - Requires `issues: write` permission

2. **Python Script:** `.github/scripts/jules_planner.py`
   - Interacts with Jules API
   - Creates planning sessions
   - Formats and posts results

### How It Works

1. User comments `@jules plan` on an issue
2. Workflow detects the comment and starts
3. Script lists available sources (connected GitHub repos)
4. Creates a Jules session with the planning prompt
5. Polls session activities to retrieve the generated plan
6. Posts the plan as a comment on the issue

### Session-Based Architecture

Jules uses a session-based approach:
- **Source**: GitHub repository connected to Jules
- **Session**: A continuous unit of work (like a chat session)
- **Activity**: Individual actions within a session (plan generation, progress updates, etc.)

This allows Jules to generate comprehensive plans and even create pull requests with implementation code.

## Security Notes

- Keep your Jules API key secure
- Never commit API keys to your repository
- Google automatically disables publicly exposed API keys
- The workflow runs in GitHub Actions with restricted permissions

## API Status

> **Note:** The Jules API is currently in alpha release. Specifications and behavior may change as Google works toward stabilization.

## Resources

- [Jules Documentation](https://jules.google/docs)
- [Jules API Reference](https://developers.google.com/jules/api/reference/rest)
- [Jules Web App](https://jules.google.com)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
