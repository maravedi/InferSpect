#!/usr/bin/env python3
"""
Jules Planning Integration Script

This script integrates with Jules (Google Gemini) API to provide
system design and architecture planning assistance.
"""

import os
import sys
import json
import requests
from typing import Dict, Any, Optional


class JulesPlanner:
    """Client for Jules (Gemini) API planning requests."""

    def __init__(self, api_key: str):
        """Initialize Jules planner with API key."""
        if not api_key:
            raise ValueError("JULES_API_KEY is required")

        self.api_key = api_key
        # Jules uses Google Gemini API
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

    def generate_plan(self, context: Dict[str, Any]) -> str:
        """
        Generate architecture/design plan based on context.

        Args:
            context: Dictionary containing issue/PR details

        Returns:
            Generated plan as markdown string
        """
        prompt = self._build_planning_prompt(context)

        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "topK": 40,
                        "topP": 0.95,
                        "maxOutputTokens": 8192,
                    }
                },
                timeout=60
            )

            response.raise_for_status()
            result = response.json()

            # Extract the generated text from Gemini response
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if len(parts) > 0 and "text" in parts[0]:
                        return parts[0]["text"]

            return "❌ Error: Unable to parse Jules response"

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

        prompt = f"""You are Jules, an expert system architect and software designer.

You have been asked to create a detailed architecture and implementation plan for the following request.

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

Please format your response in clear, well-structured Markdown. Use diagrams (ASCII/text-based), tables, and code examples where appropriate.

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
1. Go to repository Settings → Secrets and variables → Actions
2. Add a new secret named `JULES_API_KEY`
3. Set the value to your Google Gemini API key

Get your API key at: https://makersuite.google.com/app/apikey
"""
        print(error_msg)
        post_comment_to_github(error_msg)
        sys.exit(1)

    try:
        # Get issue/PR context
        print("📋 Extracting issue context...")
        context = get_issue_context()
        print(f"   Issue #{context['number']}: {context['title']}")
        print(f"   Requested by: @{context['author']}")

        # Generate plan
        print("🤔 Generating architecture plan with Jules...")
        planner = JulesPlanner(api_key)
        plan = planner.generate_plan(context)

        # Format the response
        formatted_response = f"""## 📐 Jules Architecture Plan

*Generated architecture and design plan for this request*

---

{plan}

---

<sub>🤖 Generated by Jules (Gemini 1.5 Pro) | Requested by @{context['author']}</sub>
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
