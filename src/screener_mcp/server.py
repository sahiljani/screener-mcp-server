"""Screener MCP Server — exposes Indian stock market data as MCP tools."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from screener_mcp.client import ScreenerAPIClient

mcp = FastMCP(
    "screener-mcp",
    host="0.0.0.0",
    port=8098,
    transport_security={
        "enable_dns_rebinding_protection": True,
        "allowed_hosts": [
            "screener.janisahil.com",
            "screener.janisahil.com:*",
            "127.0.0.1:*",
            "localhost:*",
        ],
        "allowed_origins": [
            "https://screener.janisahil.com",
            "https://claude.ai",
            "http://127.0.0.1:*",
            "http://localhost:*",
        ],
    },
)
api = ScreenerAPIClient()

VALID_TABS = [
    "analysis", "peers", "quarters", "profit-loss",
    "balance-sheet", "cash-flow", "ratios", "shareholding", "documents",
]


def _fmt(data: Any) -> str:
    """Format data as pretty JSON string."""
    return json.dumps(data, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════
#  TOOLS
# ═══════════════════════════════════════════════════════════════════

@mcp.tool()
async def search_companies(query: str, limit: int = 10) -> str:
    """Search Indian stock market companies by name. Returns matching symbols and URLs.

    Args:
        query: Company name to search (e.g., "tata", "reliance", "infosys")
        limit: Max results to return (1-50, default 10)
    """
    data = await api.search_companies(query=query, limit=min(max(limit, 1), 50))
    return _fmt(data)


@mcp.tool()
async def get_company(symbol: str, mode: str = "consolidated") -> str:
    """Get full company snapshot — overview, key ratios, analysis (pros/cons), and all financial tabs for any NSE-listed Indian company.

    Args:
        symbol: Stock symbol (e.g., TCS, INFY, RELIANCE, HDFCBANK)
        mode: "consolidated" (default) or "standalone"
    """
    data = await api.get_company(symbol=symbol.strip().upper(), mode=mode)
    return _fmt(data)


@mcp.tool()
async def get_company_raw(symbol: str, mode: str = "consolidated") -> str:
    """Get raw HTML and section list for a company page — useful for extracting data not available via structured endpoints.

    Args:
        symbol: Stock symbol (e.g., TCS, INFY, RELIANCE, HDFCBANK)
        mode: "consolidated" (default) or "standalone"
    """
    data = await api.get_company_raw(symbol=symbol.strip().upper(), mode=mode)
    return _fmt(data)


@mcp.tool()
async def get_company_tab(symbol: str, tab: str, mode: str = "consolidated") -> str:
    """Get a specific financial data tab for a company.

    Args:
        symbol: Stock symbol (e.g., TCS, INFY)
        tab: One of: analysis, peers, quarters, profit-loss, balance-sheet, cash-flow, ratios, shareholding, documents
        mode: "consolidated" (default) or "standalone"
    """
    tab = tab.strip().lower()
    if tab not in VALID_TABS:
        return json.dumps({"error": f"Invalid tab '{tab}'. Valid tabs: {', '.join(VALID_TABS)}"})
    data = await api.get_company_tab(symbol=symbol.strip().upper(), tab=tab, mode=mode)
    return _fmt(data)


@mcp.tool()
async def compare_companies(symbols: str, mode: str = "consolidated") -> str:
    """Compare 2 or more companies side-by-side on key metrics (market cap, PE, ROE, dividend yield, etc.).

    Args:
        symbols: Comma-separated stock symbols (e.g., "TCS,INFY,WIPRO")
        mode: "consolidated" (default) or "standalone"
    """
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    if len(symbol_list) < 2:
        return json.dumps({"error": "Need at least 2 symbols to compare"})
    data = await api.compare_companies(symbols=symbol_list, mode=mode)
    return _fmt(data)


@mcp.tool()
async def list_sectors() -> str:
    """List all 50+ Indian stock market sectors (Pharma, IT, Banks, Auto, etc.) with their slugs."""
    data = await api.list_sectors()
    return _fmt(data)


@mcp.tool()
async def get_sector_data(sector: str, page: int = 1, limit: int = 50) -> str:
    """Get companies listed in a specific market sector with key financial metrics.

    Args:
        sector: Sector slug (e.g., "pharmaceuticals-biotechnology", "it-software", "banks-private-sector")
        page: Page number (default 1)
        limit: Results per page (1-50, default 50)
    """
    data = await api.get_sector_data(sector=sector.strip(), page=page, limit=min(max(limit, 1), 50))
    return _fmt(data)


@mcp.tool()
async def list_screens(page: int = 1, q: str | None = None, sort: str | None = None) -> str:
    """Browse or search public stock screens (user-created filters like "Magic Formula", "Growth Stocks", "High Dividend Yield").

    Args:
        page: Page number (default 1)
        q: Search screens by title/description (e.g., "dividend", "growth", "undervalued")
        sort: Sort by "title" (alphabetical) or "screen_id" (recency)
    """
    data = await api.list_screens(page=page, q=q, sort=sort)
    return _fmt(data)


@mcp.tool()
async def get_screen_details(screen_id: int, slug: str, page: int = 1, limit: int = 50) -> str:
    """Run a specific stock screen and get matching companies with their data.

    Args:
        screen_id: Screen ID (from list_screens results)
        slug: Screen URL slug (from list_screens results)
        page: Page number (default 1)
        limit: Results per page (1-50, default 50)
    """
    data = await api.get_screen_details(screen_id=screen_id, slug=slug, page=page, limit=min(max(limit, 1), 50))
    return _fmt(data)


@mcp.tool()
async def get_market_overview(top_n: int = 5) -> str:
    """Get a quick market overview combining top sectors and trending screens.

    Args:
        top_n: Number of top items to return per category (default 5)
    """
    sectors = await api.list_sectors()
    screens = await api.list_screens(page=1)

    sector_list = sectors.get("data", {}).get("sectors", [])[:top_n]
    screen_items = screens.get("data", {}).get("page", {}).get("items", [])[:top_n]

    overview = {
        "top_sectors": sector_list,
        "trending_screens": screen_items,
        "total_sectors": len(sectors.get("data", {}).get("sectors", [])),
        "total_screen_pages": screens.get("data", {}).get("page", {}).get("pagination", {}).get("total_pages"),
    }
    return _fmt(overview)


@mcp.tool()
async def health_check() -> str:
    """Check if the Screener API is reachable and healthy."""
    try:
        h = await api.health()
        r = await api.ready()
        return _fmt({"health": h, "ready": r})
    except Exception as e:
        return json.dumps({"error": f"API unreachable: {e}"})


# ═══════════════════════════════════════════════════════════════════
#  RESOURCES
# ═══════════════════════════════════════════════════════════════════

@mcp.resource("screener://company/{symbol}")
async def company_resource(symbol: str) -> str:
    """Company profile for {symbol} — overview, ratios, analysis."""
    data = await api.get_company(symbol=symbol.strip().upper())
    return _fmt(data)


@mcp.resource("screener://sector/{slug}")
async def sector_resource(slug: str) -> str:
    """Sector listing for {slug} — companies and key metrics."""
    data = await api.get_sector_data(sector=slug.strip())
    return _fmt(data)


@mcp.resource("screener://screen/{screen_id}/{slug}")
async def screen_resource(screen_id: int, slug: str) -> str:
    """Screen results for {slug} — matching companies and data."""
    data = await api.get_screen_details(screen_id=screen_id, slug=slug)
    return _fmt(data)


# ═══════════════════════════════════════════════════════════════════
#  PROMPTS
# ═══════════════════════════════════════════════════════════════════

@mcp.prompt()
async def analyze_company(symbol: str) -> str:
    """Deep-dive analysis of an Indian listed company.

    Args:
        symbol: Stock symbol to analyze (e.g., TCS, RELIANCE)
    """
    return f"""Please perform a comprehensive analysis of {symbol.upper()}:

1. First, use the `get_company` tool to fetch the full company snapshot for {symbol.upper()}.
2. Then use `get_company_tab` with tab="peers" to see how it compares to peers.
3. Use `get_company_tab` with tab="ratios" for historical ratio trends.

Based on the data, provide:
- **Company Overview**: What does this company do? Key metrics.
- **Strengths**: Based on the analysis pros and financial ratios.
- **Weaknesses**: Based on the analysis cons and any red flags.
- **Peer Comparison**: How does it stack up against competitors?
- **Valuation**: Is it expensive or cheap based on PE, PB, and peer comparison?
- **Summary**: One-paragraph investment thesis.
"""


@mcp.prompt()
async def screen_stocks(criteria: str) -> str:
    """Help find stocks matching specific criteria.

    Args:
        criteria: Natural language description of what you're looking for (e.g., "high dividend pharma stocks")
    """
    return f"""The user is looking for: {criteria}

Follow these steps:
1. Use `list_screens` with a relevant search query (q parameter) to find matching public screens.
2. If a relevant screen is found, use `get_screen_details` to fetch the actual matching companies.
3. If no screen matches, try `list_sectors` to find a relevant sector, then `get_sector_data` to browse companies in that sector.
4. Present the results as a clean table with key metrics.
5. Highlight the top 3-5 picks that best match the criteria and explain why.
"""


@mcp.prompt()
async def compare_stocks(symbols: str) -> str:
    """Structured comparison of multiple stocks.

    Args:
        symbols: Comma-separated symbols to compare (e.g., "TCS,INFY,WIPRO")
    """
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    symbols_str = ", ".join(symbol_list)
    return f"""Please compare these companies: {symbols_str}

1. Use `compare_companies` with symbols="{','.join(symbol_list)}" to get the side-by-side comparison.
2. For each company, use `get_company_tab` with tab="ratios" to get historical trends.
3. Present a comparison table covering: Market Cap, PE, ROE, Dividend Yield, Sales Growth, Profit Growth.
4. For each metric, mark the best performer.
5. Give a final verdict: which stock looks strongest overall and why.
"""


# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Screener MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport type: stdio (default, for Claude Code) or sse (for Claude.ai)",
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind SSE server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port for SSE server (default: 8000)"
    )
    args = parser.parse_args()

    if args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
