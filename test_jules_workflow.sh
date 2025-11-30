#!/bin/bash
#
# Test script to verify jules-planner workflow integration
# This script simulates the GitHub Actions environment for testing
#

set -e

echo "🧪 Testing Jules Planner Workflow"
echo "=================================="
echo ""

# Test 1: Check if jules-planner is installed
echo "✓ Test 1: Checking jules-planner installation..."
if command -v jules-planner &> /dev/null; then
    echo "  ✓ jules-planner command found at: $(which jules-planner)"
else
    echo "  ✗ jules-planner command not found"
    exit 1
fi

# Test 2: Verify package version
echo ""
echo "✓ Test 2: Checking package version..."
pip show jules-planner | grep -E "Name|Version|Location"

# Test 3: Create mock GitHub event for testing
echo ""
echo "✓ Test 3: Creating mock GitHub event..."
mkdir -p /tmp/github-event
cat > /tmp/github-event/event.json <<'EOFTEST'
{
  "action": "created",
  "issue": {
    "number": 999,
    "title": "Test Issue for Jules Planning",
    "body": "This is a test issue to verify the Jules planning workflow integration.",
    "pull_request": null
  },
  "comment": {
    "body": "@jules plan\n\nPlease create an architecture plan for this feature.",
    "user": {
      "login": "test-user"
    }
  },
  "repository": {
    "name": "InferSpect",
    "owner": {
      "login": "maravedi"
    }
  }
}
EOFTEST
echo "  ✓ Mock event created at /tmp/github-event/event.json"

# Test 4: Verify workflow YAML syntax
echo ""
echo "✓ Test 4: Validating workflow YAML syntax..."
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/jules_plan.yml')); print('  ✓ YAML syntax is valid')"

# Test 5: Check required environment variables (simulation)
echo ""
echo "✓ Test 5: Checking environment variable requirements..."
echo "  Required environment variables for jules-planner:"
echo "    - JULES_API_KEY (must be set in GitHub Secrets)"
echo "    - GITHUB_TOKEN (automatically provided by GitHub Actions)"
echo "    - GITHUB_REPOSITORY (automatically provided by GitHub Actions)"
echo "    - GITHUB_EVENT_PATH (automatically provided by GitHub Actions)"

echo ""
echo "=================================="
echo "✅ All tests passed!"
echo ""
echo "📋 Next Steps:"
echo "1. Ensure JULES_API_KEY is set in repository secrets"
echo "2. Create or comment on an issue with '@jules plan'"
echo "3. Check the Actions tab for workflow execution"
echo "4. Verify the plan is posted as a comment on the issue"
echo ""
echo "🔗 Workflow file: .github/workflows/jules_plan.yml"
echo "🔗 Package repo: https://github.com/maravedi/jules-actions"
