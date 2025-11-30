# Testing the Jules Planner Workflow

This document provides instructions for testing the updated Jules Planner workflow integration.

## What Changed

The workflow has been updated to use the official `jules-planner` package from https://github.com/maravedi/jules-actions instead of the custom Python script.

**Key Changes:**
- ✅ Replaced `.github/scripts/jules_planner.py` with `jules-planner` package
- ✅ Simplified workflow by using the official package CLI
- ✅ Added `contents: read` permission as required by documentation
- ✅ Installs package from PyPI (https://pypi.org/project/jules-planner/)

## Prerequisites

Before testing, ensure:

1. **JULES_API_KEY Secret**: Must be configured in repository settings
   - Go to: Settings → Secrets and variables → Actions
   - Verify `JULES_API_KEY` exists and is valid
   - If not, create one at https://jules.google.com/settings#api

2. **Repository Access**: The repository must be connected to Jules
   - Go to https://jules.google.com
   - Install the Jules GitHub app for this repository

## Manual Testing Steps

### Test 1: Automated Validation (Local)

Run the automated test script:

```bash
./test_jules_workflow.sh
```

This validates:
- ✓ Package installation works
- ✓ Command is available
- ✓ Workflow YAML syntax is correct
- ✓ Environment variables are documented

### Test 2: End-to-End Workflow Test (GitHub)

1. **Create a Test Issue**:
   - Go to: https://github.com/maravedi/InferSpect/issues/new
   - Title: "Test Jules Planner Integration"
   - Body: "Testing the updated workflow with jules-planner package"
   - Click "Submit new issue"

2. **Trigger the Workflow**:
   - Add a comment to the issue: `@jules plan`
   - The workflow should trigger automatically

3. **Verify Workflow Execution**:
   - Go to: https://github.com/maravedi/InferSpect/actions
   - Look for "Jules Plan" workflow run
   - Click on it to view logs

4. **Check Results**:
   - Workflow should complete successfully
   - Jules should post an architecture plan as a comment on the issue
   - Comment should contain structured implementation steps

### Expected Workflow Behavior

When triggered with `@jules plan`, the workflow will:

1. ✓ Checkout repository code
2. ✓ Set up Python 3.11
3. ✓ Install jules-planner from GitHub
4. ✓ Run jules-planner command with proper environment variables
5. ✓ Post generated architecture plan to the issue

### Workflow Logs to Review

Check these sections in the workflow logs:

- **Install jules-planner**: Should clone from GitHub and install successfully
- **Run Jules Planner**: Should show:
  - "🔍 Looking for repository in Jules sources..."
  - "✓ Found source: ..."
  - "📝 Creating Jules planning session..."
  - "✓ Session created: ..."
  - "⏳ Waiting for Jules to generate the plan..."
  - "✅ Successfully posted Jules plan to GitHub"

### Troubleshooting

#### Error: "JULES_API_KEY is not configured"
- **Solution**: Add the secret in repository settings
- Go to: Settings → Secrets and variables → Actions → New repository secret

#### Error: "Repository Not Found"
- **Solution**: Connect repository to Jules
- Go to: https://jules.google.com
- Install Jules GitHub app for this repository

#### Error: "pip install failed"
- **Solution**: Check PyPI connectivity
- Verify: https://pypi.org/project/jules-planner/ is accessible

#### No workflow triggered
- **Solution**: Check workflow file and permissions
- Ensure the comment contains exactly: `@jules plan`
- Check: https://github.com/maravedi/InferSpect/actions

## Workflow File Location

- **File**: `.github/workflows/jules_plan.yml`
- **Trigger**: Issue comments containing `@jules plan`
- **Package**: https://github.com/maravedi/jules-actions

## Verification Checklist

- [ ] Local test script passes (`./test_jules_workflow.sh`)
- [ ] JULES_API_KEY secret is configured
- [ ] Repository is connected to Jules
- [ ] Created test issue successfully
- [ ] Workflow triggered when commenting `@jules plan`
- [ ] Workflow completes without errors
- [ ] Architecture plan posted to issue
- [ ] Plan contains structured implementation steps

## Success Criteria

The workflow is considered working when:

1. ✅ Workflow runs without errors in GitHub Actions
2. ✅ jules-planner package installs successfully from GitHub
3. ✅ Jules API is called and returns a plan
4. ✅ Plan is posted as a comment on the issue
5. ✅ Comment contains formatted architecture/implementation details

## Next Steps After Testing

If all tests pass:
1. Close the test issue
2. The workflow is ready for production use
3. Team members can use `@jules plan` on any issue/PR

If tests fail:
1. Check workflow logs in Actions tab
2. Verify secrets are configured correctly
3. Ensure repository is connected to Jules
4. Review error messages and apply fixes from troubleshooting section
