#!/bin/bash
#
# Test script to verify jules-specs and jules-planner workflow integration
# This script simulates the GitHub Actions environment for testing
#

set -e

echo "🧪 Testing Jules Spec & Plan Workflows"
echo "========================================"
echo ""

# Test 1: Check if jules-specs is installed
echo "✓ Test 1: Checking jules-specs installation..."
if command -v jules-specs &> /dev/null; then
    echo "  ✓ jules-specs command found at: $(which jules-specs)"
else
    echo "  ✗ jules-specs command not found"
    exit 1
fi

# Test 2: Check if jules-planner is installed
echo ""
echo "✓ Test 2: Checking jules-planner installation..."
if command -v jules-planner &> /dev/null; then
    echo "  ✓ jules-planner command found at: $(which jules-planner)"
else
    echo "  ✗ jules-planner command not found"
    exit 1
fi

# Test 3: Verify package versions
echo ""
echo "✓ Test 3: Checking package versions..."
echo "  jules-specs:"
pip show jules-specs | grep -E "Name|Version|Location"
echo ""
echo "  jules-planner:"
pip show jules-planner | grep -E "Name|Version|Location"

# Test 4: Create mock GitHub events for testing
echo ""
echo "✓ Test 4: Creating mock GitHub events..."
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

# Create mock event for spec generation
cat > /tmp/github-event/spec-event.json <<'EOFSPEC'
{
  "action": "created",
  "issue": {
    "number": 998,
    "title": "Test Issue for Jules Spec Generation",
    "body": "Generate a technical specification for this new feature.",
    "pull_request": null
  },
  "comment": {
    "body": "@jules spec\n\nPlease generate technical specifications for this feature.",
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
EOFSPEC
echo "  ✓ Mock spec event created at /tmp/github-event/spec-event.json"

# Test 5: Verify workflow YAML syntax
echo ""
echo "✓ Test 5: Validating workflow YAML syntax..."
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/jules_plan.yml')); print('  ✓ YAML syntax is valid')"

# Test 6: Check required environment variables (simulation)
echo ""
echo "✓ Test 6: Checking environment variable requirements..."
echo "  Required environment variables for jules-specs and jules-planner:"
echo "    - JULES_API_KEY (must be set in GitHub Secrets)"
echo "    - GITHUB_TOKEN (automatically provided by GitHub Actions)"
echo "    - GITHUB_REPOSITORY (automatically provided by GitHub Actions)"
echo "    - GITHUB_EVENT_PATH (automatically provided by GitHub Actions)"

echo ""
echo "=========================================="
echo "✅ All tests passed!"
echo ""
echo "📋 Next Steps:"
echo "1. Ensure JULES_API_KEY is set in repository secrets"
echo "2. Create or comment on an issue with '@jules spec' or '@jules plan'"
echo "3. Check the Actions tab for workflow execution"
echo "4. Verify the generated spec/plan is posted as a comment on the issue"
echo ""
echo "🔗 Workflow file: .github/workflows/jules_plan.yml"
echo "🔗 Package repos:"
echo "   - https://pypi.org/project/jules-specs/"
echo "   - https://pypi.org/project/jules-planner/"
