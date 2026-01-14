import os
import base64
import requests

# Get token from env variable
github_token = os.environ.get("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN environment variable is required")

# Settings
owner = "uernana"         # Replace with your GitHub username or org
repo = "MCP-Learning"              # Replace with the repo name
file_path = "docs/mcp_learning.md"  # Path inside the repo
commit_message = "Add MCP learning notes"

# Content about Model Context Protocol learning
file_content = """# Model Context Protocol Learning

The Model Context Protocol (MCP) is a communication specification that allows
AI-enabled applications (clients) to communicate consistently with external tools
and data sources (servers). Key points include:
- Standardised API surface for tools
- Supports transports like stdio, WebSockets, HTTP
- Enables modular integration of capabilities into editors (VS Code, Cursor, Windsurf)
- Server can wrap databases, APIs, or AI models

Learning MCP involves understanding:
1. How clients discover servers
2. Tool schemas and execution flows
3. Transport layers
4. Security and authentication for external resources

This document is part of hands-on practice connecting an MCP client to a server.
"""

# Encode content to base64
encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

# Construct API URL
url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

# Request payload
payload = {
    "message": commit_message,
    "content": encoded_content,
    # Optional: Specify branch if not default
    # "branch": "main"
}

# Headers with token
headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Send request
response = requests.put(url, json=payload, headers=headers)

# Check response
if response.status_code in (201, 200):
    print(f"✅ File created/updated successfully at {response.json()['content']['html_url']}")
else:
    print(f"❌ Failed with {response.status_code}: {response.text}")
