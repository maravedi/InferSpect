#!/usr/bin/env python3
"""
Jules Planning Integration Script

This script integrates with the official Jules API to provide
system design and architecture planning assistance.
"""

import os
import sys
import json
import time
import requests
from typing import Dict, Any, Optional, List


class JulesPlanner:
    """Client for Jules API planning requests."""

    def __init__(self, api_key: str, repo_owner: str, repo_name: str):
        """Initialize Jules planner with API key and repository info."""
        if not api_key:
            raise ValueError("JULES_API_KEY is required")

        self.api_key = api_key
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        # Official Jules API base URL
        self.base_url = "https://jules.googleapis.com/v1alpha"
        self.headers = {
            "X-Goog-Api-Key": api_key,
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make authenticated request to Jules API."""
        url = f"{self.base_url}/{endpoint}"
        kwargs.setdefault('headers', {}).update(self.headers)
        kwargs.setdefault('timeout', 60)

        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def list_sources(self) -> List[Dict[str, Any]]:
        """List available sources (GitHub repositories)."""
        response = self._make_request("GET", "sources")
        data = response.json()
        return data.get("sources", [])

    def find_source(self) -> Optional[str]:
        """Find the source name for the current repository."""
        sources = self.list_sources()

        for source in sources:
            github_repo = source.get("githubRepo", {})
            if (github_repo.get("owner") == self.repo_owner and
                github_repo.get("repo") == self.repo_name):
                return source.get("name")

        return None

    def create_session(self, prompt: str, source_name: str, title: str = "Architecture Planning") -> Dict[str, Any]:
        """Create a new Jules session."""
        payload = {
            "prompt": prompt,
            "sourceContext": {
                "source": source_name,
                "githubRepoContext": {
                    "startingBranch": "main"
                }
            },
            "title": title,
            "requirePlanApproval": False  # Auto-approve plans for API sessions
        }

        response = self._make_request("POST", "sessions", json=payload)
        return response.json()

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session details."""
        response = self._make_request("GET", f"sessions/{session_id}")
        return response.json()

    def list_activities(self, session_id: str, page_size: int = 50) -> List[Dict[str, Any]]:
        """List activities in a session."""
        response = self._make_request("GET", f"sessions/{session_id}/activities?pageSize={page_size}")
        data = response.json()
        return data.get("activities", [])

    def wait_for_plan(self, session_id: str, max_wait: int = 120) -> Optional[str]:
        """
        Wait for Jules to generate a plan and extract it.

        Args:
            session_id: The session ID to monitor
            max_wait: Maximum seconds to wait

        Returns:
            The generated plan as markdown, or None if not found
        """
        start_time = time.time()
        plan_text = None

        while (time.time() - start_time) < max_wait:
            activities = self.list_activities(session_id)

            # Look for plan generation activity
            for activity in activities:
                if "planGenerated" in activity:
                    plan = activity["planGenerated"].get("plan", {})
                    steps = plan.get("steps", [])

                    if steps:
                        # Format plan steps as markdown
                        plan_lines = ["## 📋 Implementation Plan\n"]
                        for step in steps:
                            step_num = step.get("index", 0) + 1
                            title = step.get("title", "")
                            plan_lines.append(f"{step_num}. **{title}**")

                        plan_text = "\n".join(plan_lines)

                # Also collect progress updates and other insights
                if "progressUpdated" in activity:
                    progress = activity["progressUpdated"]
                    # Could append progress updates to plan if needed

                # Check if session completed
                if "sessionCompleted" in activity:
                    break

            if plan_text:
                break

            time.sleep(5)  # Poll every 5 seconds

        return plan_text

    def generate_plan(self, context: Dict[str, Any]) -> str:
        """
        Generate architecture/design plan based on context.

        Args:
            context: Dictionary containing issue/PR details

        Returns:
            Generated plan as markdown string
        """
        try:
            # Find the source for this repository
            print("🔍 Looking for repository in Jules sources...")
            source_name = self.find_source()

            if not source_name:
                return f"""❌ **Repository Not Found**

The repository `{self.repo_owner}/{self.repo_name}` is not connected to Jules.

**To fix this:**
1. Go to [Jules web app](https://jules.google.com)
2. Install the Jules GitHub app for this repository
3. Once installed, try `@jules plan` again

For more information, see the [Jules documentation](https://jules.google/docs)."""

            print(f"✓ Found source: {source_name}")

            # Build the planning prompt
            prompt = self._build_planning_prompt(context)

            # Create a session
            print("📝 Creating Jules planning session...")
            session_title = f"Architecture Plan: {context.get('title', 'Issue')}"
            session = self.create_session(prompt, source_name, session_title)
            session_id = session.get("id")

            print(f"✓ Session created: {session_id}")

            # Wait for the plan to be generated
            print("⏳ Waiting for Jules to generate the plan...")
            plan = self.wait_for_plan(session_id, max_wait=120)

            if not plan:
                # Fallback: get all activities and format them
                print("⚠ No plan found, retrieving session activities...")
                activities = self.list_activities(session_id)

                if activities:
                    plan_parts = ["## 📊 Jules Session Summary\n"]
                    for activity in activities[:10]:  # Limit to first 10 activities
                        if "progressUpdated" in activity:
                            progress = activity["progressUpdated"]
                            title = progress.get("title", "")
                            description = progress.get("description", "")
                            if title:
                                plan_parts.append(f"- **{title}**")
                                if description:
                                    plan_parts.append(f"  {description}\n")

                    plan = "\n".join(plan_parts) if len(plan_parts) > 1 else None

            if not plan:
                return f"""⚠️ **Planning Session Created**

Jules session has been initiated but no plan was generated yet.

View the session progress at: https://jules.google.com

Session ID: `{session_id}`"""

            return plan

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return """❌ **Authentication Error**

The `JULES_API_KEY` is invalid or has expired.

**To fix this:**
1. Go to [Jules Settings](https://jules.google.com/settings#api)
2. Create a new API key
3. Update the `JULES_API_KEY` secret in repository settings

For more information, see the [Jules API documentation](https://developers.google.com/jules/api)."""
            else:
                return f"❌ Error calling Jules API: {e.response.status_code} {e.response.reason}"

        except requests.exceptions.RequestException as e:
            return f"❌ Error calling Jules API: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"

    def _build_planning_prompt(self, context: Dict[str, Any]) -> str:
        """Build the planning prompt from context."""
        issue_title = context.get("title", "")
        issue_body = context.get("body", "")
        comment_body = context.get("comment", "")
        issue_number = context.get("number", "")
        is_pr = context.get("is_pr", False)

        entity_type = "Pull Request" if is_pr else "Issue"

        prompt = f"""Create a detailed architecture and implementation plan for the following request.

**{entity_type} #{issue_number}: {issue_title}**

**Description:**
{issue_body}

**Planning Request:**
{comment_body}

Please provide a comprehensive architecture and design plan that includes:

1. **Architecture Overview**
   - High-level system design
   - Key components and their interactions
   - Data flow diagrams (in text/markdown format)

2. **Technology Stack Recommendations**
   - Recommended technologies and frameworks
   - Justification for each choice
   - Alternatives considered

3. **Implementation Strategy**
   - Phased implementation approach
   - Key milestones and deliverables
   - Dependencies and prerequisites

4. **Design Decisions**
   - Critical architectural decisions
   - Trade-offs and rationale
   - Scalability considerations

5. **Security & Performance**
   - Security considerations
   - Performance optimization strategies
   - Monitoring and observability approach

6. **Risk Analysis**
   - Potential risks and challenges
   - Mitigation strategies
   - Fallback options

7. **Next Steps**
   - Immediate action items
   - Long-term roadmap
   - Success criteria

Format your response in clear, well-structured Markdown. Use diagrams (ASCII/text-based), tables, and code examples where appropriate.

Focus on practical, actionable recommendations that can guide the development team.
"""

        return prompt


def get_issue_context() -> Dict[str, Any]:
    """Extract issue/PR context from GitHub environment variables."""
    # GitHub Actions provides context through environment variables
    event_path = os.getenv("GITHUB_EVENT_PATH")

    if not event_path or not os.path.exists(event_path):
        raise ValueError("GitHub event data not found")

    with open(event_path, 'r') as f:
        event_data = json.load(f)

    # Extract relevant information
    issue = event_data.get("issue", {})
    comment = event_data.get("comment", {})

    return {
        "number": issue.get("number", ""),
        "title": issue.get("title", ""),
        "body": issue.get("body", ""),
        "comment": comment.get("body", ""),
        "is_pr": "pull_request" in issue,
        "author": comment.get("user", {}).get("login", "unknown")
    }


def post_comment_to_github(comment_body: str) -> None:
    """Post the generated plan as a comment on the issue/PR."""
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    event_path = os.getenv("GITHUB_EVENT_PATH")

    if not all([github_token, repo, event_path]):
        print("Error: Missing required GitHub environment variables")
        sys.exit(1)

    with open(event_path, 'r') as f:
        event_data = json.load(f)

    issue_number = event_data.get("issue", {}).get("number")

    if not issue_number:
        print("Error: Could not determine issue number")
        sys.exit(1)

    # Post comment using GitHub API
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.post(
        url,
        headers=headers,
        json={"body": comment_body},
        timeout=30
    )

    if response.status_code == 201:
        print("✅ Successfully posted Jules plan to GitHub")
    else:
        print(f"❌ Failed to post comment: {response.status_code} - {response.text}")
        sys.exit(1)


def main():
    """Main execution function."""
    print("🚀 Jules Planning Integration Started")

    # Get API key
    api_key = os.getenv("JULES_API_KEY")
    if not api_key:
        error_msg = """❌ **Jules Planning Error**

The `JULES_API_KEY` secret is not configured.

To enable Jules planning:
1. Go to [Jules Settings](https://jules.google.com/settings#api)
2. Create a new API key
3. Go to repository Settings → Secrets and variables → Actions
4. Add a new secret named `JULES_API_KEY`
5. Set the value to your Jules API key

For more information, see the [Jules API documentation](https://developers.google.com/jules/api).
"""
        print(error_msg)
        post_comment_to_github(error_msg)
        sys.exit(1)

    # Get repository info
    repo = os.getenv("GITHUB_REPOSITORY")
    if not repo or "/" not in repo:
        error_msg = "❌ Error: Could not determine repository owner and name"
        print(error_msg)
        post_comment_to_github(error_msg)
        sys.exit(1)

    repo_owner, repo_name = repo.split("/", 1)

    try:
        # Get issue/PR context
        print("📋 Extracting issue context...")
        context = get_issue_context()
        print(f"   Issue #{context['number']}: {context['title']}")
        print(f"   Requested by: @{context['author']}")

        # Generate plan
        print("🤔 Generating architecture plan with Jules...")
        planner = JulesPlanner(api_key, repo_owner, repo_name)
        plan = planner.generate_plan(context)

        # Format the response
        formatted_response = f"""## 📐 Jules Architecture Plan

*Generated architecture and design plan for this request*

---

{plan}

---

<sub>🤖 Generated by Jules AI | Requested by @{context['author']}</sub>
"""

        # Post to GitHub
        print("📤 Posting plan to GitHub...")
        post_comment_to_github(formatted_response)

        print("✅ Jules planning completed successfully")

    except Exception as e:
        error_msg = f"""❌ **Jules Planning Error**

An error occurred while generating the plan:

```
{str(e)}
```

Please check the workflow logs for more details.
"""
        print(f"Error: {str(e)}")
        post_comment_to_github(error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
