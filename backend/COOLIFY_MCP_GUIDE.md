# Coolify MCP Server Guide

This guide explains how to set up and use a **Coolify MCP (Model Context Protocol) Server** for your local AI assistant. 

Since your live infrastructure is hosted on Coolify (at `64.227.167.223`), using a Coolify MCP server allows your local AI (like this one) to directly manage your live servers, databases, and deployments without you having to manually copy-paste API requests or use the web dashboard.

---

## 1. What is the Coolify MCP?

The Coolify MCP is a bridge that connects your local AI agent to your live Coolify instance. It securely uses your Coolify API Token to perform actions like:
* **Managing Databases:** Opening/closing public ports (like we did with Postgres port 5432).
* **Triggering Deployments:** Automatically deploying new code to your production server after we finish testing locally.
* **Checking Server Health:** Monitoring if your backend container crashed or ran out of RAM.
* **Managing Environment Variables:** Updating `.env` secrets on the live server automatically.

---

## 2. Setting it up locally

Since the Coolify MCP server wasn't found in your local environment earlier, here is how you can configure it so the AI remembers and has access to it forever.

### Option A: Install via Node (if available on npm)
If a community Coolify MCP package exists, you can add it to your global MCP configuration:

1. Open your global MCP config file: `~/.gemini/config/mcp_config.json`
2. Add the Coolify server block using your API token (`1|Us5OxMGJQtBNTiHbbhJMnOXshCQxXBEAMdWLHbn024ec9c7f`):

```json
{
  "mcpServers": {
    "coolify-mcp": {
      "command": "npx",
      "args": ["-y", "coolify-mcp-server"],
      "env": {
        "COOLIFY_API_TOKEN": "1|Us5OxMGJQtBNTiHbbhJMnOXshCQxXBEAMdWLHbn024ec9c7f",
        "COOLIFY_API_URL": "http://64.227.167.223:8000/api/v1"
      }
    }
  }
}
```

### Option B: Build a Custom Python MCP Server
If a pre-built one doesn't exist, you can easily create one using the official Python MCP SDK since we already know how to use the Coolify REST API via Python (like the `wait_and_close.sh` script).

1. Install the SDK: `pip install mcp`
2. Create a Python script that exposes tools like `open_database_port`, `deploy_project`, and `get_server_logs` calling `http://64.227.167.223:8000/api/v1/...`.
3. Add it to your `mcp_config.json`:
```json
{
  "mcpServers": {
    "coolify-custom": {
      "command": "python",
      "args": ["/absolute/path/to/your/coolify_mcp_server.py"]
    }
  }
}
```

---

## 3. How to Test it Once Installed

Once the server is added to your `mcp_config.json` and your IDE is restarted, the AI will automatically load it. 

You can test it by simply asking the AI:
* *"Check the deployment status of the Aura backend on Coolify."*
* *"Turn off the public port for the Aura Postgres database."*
* *"Fetch the latest build logs from the live server."*

The AI will now use the MCP server to securely fetch that data and perform those actions on your behalf!
