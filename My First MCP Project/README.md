# MCP GitHub Demo

This repository demonstrates how to use Python to call the GitHub REST API
to create/update files, inspired by Model Context Protocol (MCP) concepts.

## What is MCP?

Model Context Protocol (MCP) is a standardized way for AI-enabled tools & editors
to talk to servers providing capabilities — like wrapping APIs, databases, or models.

## How to Run This Demo

1. Install requirements:
```
pip install requests
```

2. Setup your Github token
```
export GITHUB_TOKEN=ghp_yourTokenHere
```

3. Edit your .py file with your username/repo name.

4. Run: For example
```
python create_mcp_file.py
```

If successful, a new file (docs/mcp_learning.md) will appear in your repo.
