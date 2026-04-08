# Screener MCP — Claude Code Skills Guide

## Available Tools

### search_companies
Find Indian stock market companies by name.
```
search_companies(query="tata", limit=10)
```

### get_company
Full company snapshot — overview, key ratios, pros/cons analysis.
```
get_company(symbol="TCS")
get_company(symbol="RELIANCE", mode="standalone")
```

### get_company_tab
Single financial data tab for a company.
```
get_company_tab(symbol="TCS", tab="ratios")
get_company_tab(symbol="INFY", tab="profit-loss")
get_company_tab(symbol="HDFCBANK", tab="balance-sheet")
```
**Valid tabs:** analysis, peers, quarters, profit-loss, balance-sheet, cash-flow, ratios, shareholding, documents

### compare_companies
Side-by-side comparison of 2+ companies on key metrics.
```
compare_companies(symbols="TCS,INFY,WIPRO")
```

### list_sectors
Browse all 50+ Indian market sectors.
```
list_sectors()
```

### get_sector_data
Companies in a specific sector with financial metrics.
```
get_sector_data(sector="pharmaceuticals-biotechnology")
get_sector_data(sector="it-software", page=1, limit=25)
```

### list_screens
Browse or search popular public stock screens.
```
list_screens()
list_screens(q="dividend", sort="title")
list_screens(q="growth", page=2)
```

### get_screen_details
Run a specific screen and get matching companies.
```
get_screen_details(screen_id=343087, slug="fii-buying")
get_screen_details(screen_id=59, slug="magic-formula", limit=25)
```

### get_market_overview
Quick market summary — top sectors + trending screens.
```
get_market_overview(top_n=5)
```

### health_check
Verify the Screener API is reachable.
```
health_check()
```

---

## Available Resources

Load these as context in your conversation:

| URI | Description |
|-----|-------------|
| `screener://company/TCS` | TCS company profile |
| `screener://company/RELIANCE` | Reliance company profile |
| `screener://sector/it-software` | IT sector companies |
| `screener://screen/343087/fii-buying` | FII Buying screen results |

---

## Available Prompts

### analyze-company
Guided deep-dive analysis of any Indian listed company.
```
analyze-company(symbol="TCS")
```
**Workflow:** Fetches company snapshot + peers + ratios, then provides overview, strengths, weaknesses, peer comparison, valuation, and investment thesis.

### screen-stocks
Find stocks matching natural language criteria.
```
screen-stocks(criteria="high dividend yield pharma stocks")
screen-stocks(criteria="undervalued IT companies with low PE")
```
**Workflow:** Searches screens, fetches results, falls back to sector browsing, presents top picks.

### compare-stocks
Structured comparison of multiple stocks.
```
compare-stocks(symbols="TCS,INFY,WIPRO")
```
**Workflow:** Fetches comparison + individual ratios, builds comparison table, picks strongest performer.

---

## Example Conversations

**"What are TCS's key financial ratios?"**
→ Uses `get_company_tab(symbol="TCS", tab="ratios")`

**"Compare HDFC Bank and ICICI Bank"**
→ Uses `compare_companies(symbols="HDFCBANK,ICICIBANK")`

**"Find stocks with high dividend yield"**
→ Uses `list_screens(q="dividend")` → `get_screen_details(...)`

**"Show me all pharma companies"**
→ Uses `get_sector_data(sector="pharmaceuticals-biotechnology")`

**"Give me a full analysis of Reliance"**
→ Uses `analyze-company` prompt → calls get_company + peers + ratios

**"What screens are trending?"**
→ Uses `list_screens(page=1)` or `get_market_overview()`

---

## Sector Slugs (common)

| Sector | Slug |
|--------|------|
| IT / Software | `it-software` |
| Pharma | `pharmaceuticals-biotechnology` |
| Private Banks | `banks-private-sector` |
| Public Banks | `banks-public-sector` |
| Auto | `automobiles-passenger-cars` |
| Cement | `cement` |
| FMCG | `fmcg` |
| Oil & Gas | `oil-exploration` |
| Real Estate | `construction-real-estate` |
| Telecom | `telecom-services` |

Use `list_sectors()` for the full list with all slugs.

---

## Tips

- Always use **uppercase symbols**: `TCS`, not `tcs`
- Use `mode="standalone"` for subsidiary-level data (default is `consolidated`)
- For full-text search across all screens, combine `q` with `include_all_pages` via the API directly
- Screen `screen_id` and `slug` come from `list_screens()` results
- Sector slugs come from `list_sectors()` results
