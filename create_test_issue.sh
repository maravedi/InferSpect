#!/bin/bash
#
# Script to create a test issue and trigger the Jules Planner workflow
# Requires: A GitHub Personal Access Token with 'repo' scope
#
# Usage:
#   export GITHUB_TOKEN="your_token_here"
#   ./create_test_issue.sh
#

set -e

REPO_OWNER="maravedi"
REPO_NAME="InferSpect"

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable is not set"
    echo ""
    echo "To create a token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Select 'repo' scope"
    echo "4. Generate and copy the token"
    echo "5. Run: export GITHUB_TOKEN='your_token_here'"
    echo ""
    exit 1
fi

echo "🧪 Creating test issue for Jules Planner workflow..."
echo ""

# Create the test issue
RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/issues" \
    -d @- <<'EOF'
{
  "title": "🧪 Test: Jules Planner Workflow Integration",
  "body": "This is an automated test issue to verify the updated Jules Planner workflow.\n\n**Test Objectives:**\n- Verify jules-planner package installs from GitHub\n- Confirm workflow triggers on @jules plan comment\n- Validate architecture plan generation\n- Ensure plan is posted as a comment\n\n**Expected Result:**\nThe workflow should complete successfully and post a formatted architecture plan to this issue.\n\n**What to check:**\n1. Go to Actions tab and verify workflow runs\n2. Check this issue for Jules plan comment\n3. Verify the plan contains structured implementation steps\n\n---\n*Created by automated testing script*"
}
EOF
)

# Extract issue number and URL
ISSUE_NUMBER=$(echo "$RESPONSE" | grep -o '"number":[0-9]*' | head -1 | grep -o '[0-9]*')
ISSUE_URL=$(echo "$RESPONSE" | grep -o '"html_url":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$ISSUE_NUMBER" ]; then
    echo "❌ Failed to create issue"
    echo "Response: $RESPONSE"
    exit 1
fi

echo "✅ Test issue created: #$ISSUE_NUMBER"
echo "🔗 URL: $ISSUE_URL"
echo ""

# Wait a moment
sleep 2

echo "💬 Posting '@jules plan' comment to trigger workflow..."
echo ""

# Post the trigger comment
COMMENT_RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/issues/$ISSUE_NUMBER/comments" \
    -d '{"body": "@jules plan\n\nPlease create a comprehensive architecture and implementation plan for integrating the jules-planner package into our CI/CD workflow."}')

COMMENT_URL=$(echo "$COMMENT_RESPONSE" | grep -o '"html_url":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$COMMENT_URL" ]; then
    echo "❌ Failed to post comment"
    echo "Response: $COMMENT_RESPONSE"
    exit 1
fi

echo "✅ Comment posted successfully"
echo ""
echo "=================================="
echo "🎉 Test Setup Complete!"
echo "=================================="
echo ""
echo "📋 Next steps:"
echo ""
echo "1. View the issue:"
echo "   $ISSUE_URL"
echo ""
echo "2. Check workflow execution:"
echo "   https://github.com/$REPO_OWNER/$REPO_NAME/actions"
echo ""
echo "3. Wait for workflow to complete (~1-2 minutes)"
echo ""
echo "4. Verify Jules plan comment appears on the issue"
echo ""
echo "5. Review workflow logs for any errors"
echo ""
echo "=================================="
echo ""
echo "🔍 To monitor workflow status, run:"
echo "   gh run list --workflow=jules_plan.yml --limit 1"
echo ""
echo "📊 To view workflow logs, run:"
echo "   gh run view --log"
echo ""
