# screener-mcp-server

MCP server for Indian stock market data — search companies, analyze fundamentals, compare stocks, browse sectors and screens. Powered by [screener-unofficial-api](https://github.com/sahiljani/screener-unofficial-api).

---

## Tools (10)

| Tool | Description |
|------|-------------|
| `search_companies` | Search companies by name |
| `get_company` | Full company snapshot (overview, ratios, analysis) |
| `get_company_tab` | Single financial tab (ratios, P&L, balance-sheet, etc.) |
| `compare_companies` | Side-by-side comparison of 2+ companies |
| `list_sectors` | Browse 50+ market sectors |
| `get_sector_data` | Companies in a specific sector |
| `list_screens` | Browse/search public stock screens |
| `get_screen_details` | Run a screen and get matching companies |
| `get_market_overview` | Top sectors + trending screens |
| `health_check` | Verify API connectivity |

## Resources (3)

| URI | Content |
|-----|---------|
| `screener://company/{symbol}` | Company profile |
| `screener://sector/{slug}` | Sector listing |
| `screener://screen/{id}/{slug}` | Screen results |

## Prompts (3)

| Prompt | Workflow |
|--------|----------|
| `analyze-company` | Guided company deep-dive |
| `screen-stocks` | Find stocks matching criteria |
| `compare-stocks` | Structured comparison |

---

## Quick start (uses hosted API)

```bash
git clone https://github.com/sahiljani/screener-mcp-server.git
cd screener-mcp-server
pip install -e .
```

### Claude Desktop

Add to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "screener": {
      "command": "python3",
      "args": ["-m", "screener_mcp.server"],
      "cwd": "/path/to/screener-mcp-server",
      "env": {
        "SCREENER_API_BASE_URL": "https://screener.janisahil.com",
        "PYTHONPATH": "/path/to/screener-mcp-server/src"
      }
    }
  }
}
```

### Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "screener": {
      "command": "python3",
      "args": ["-m", "screener_mcp.server"],
      "cwd": "/path/to/screener-mcp-server",
      "env": {
        "SCREENER_API_BASE_URL": "https://screener.janisahil.com",
        "PYTHONPATH": "/path/to/screener-mcp-server/src"
      }
    }
  }
}
```

Restart Claude Code/Desktop after adding the config.

---

## Run with your own API

```bash
# 1. Run the screener API locally
git clone https://github.com/sahiljani/screener-unofficial-api.git
cd screener-unofficial-api
pip install -r requirements.txt
uvicorn app.main:app --port 8098

# 2. Point MCP server to localhost
export SCREENER_API_BASE_URL=http://127.0.0.1:8098
```

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SCREENER_API_BASE_URL` | `http://127.0.0.1:8098` | Screener API base URL |
| `SCREENER_API_KEY` | _(none)_ | Optional API key |
| `REQUEST_TIMEOUT_SECONDS` | `30` | HTTP request timeout |

---

## Tech stack

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (FastMCP)
- [httpx](https://www.python-httpx.org/) (async HTTP)
- [screener-unofficial-api](https://github.com/sahiljani/screener-unofficial-api) (data source)
