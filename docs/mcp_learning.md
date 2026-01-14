# Model Context Protocol Learning

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
