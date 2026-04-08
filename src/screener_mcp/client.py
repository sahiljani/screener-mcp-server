"""Async HTTP client wrapping the Screener Unofficial API."""

from __future__ import annotations

import json
from typing import Any

import httpx

from screener_mcp.config import SCREENER_API_BASE_URL, SCREENER_API_KEY, REQUEST_TIMEOUT_SECONDS


class ScreenerAPIClient:
    """Thin async wrapper around the screener-unofficial-api endpoints."""

    def __init__(
        self,
        base_url: str = SCREENER_API_BASE_URL,
        api_key: str | None = SCREENER_API_KEY,
        timeout: int = REQUEST_TIMEOUT_SECONDS,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.headers: dict[str, str] = {}
        if api_key:
            self.headers["x-api-key"] = api_key

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
        ) as c:
            r = await c.get(path, params=clean_params)
            r.raise_for_status()
            return r.json()

    async def _get_text(self, path: str, params: dict[str, Any] | None = None) -> str:
        data = await self._get(path, params)
        return json.dumps(data, indent=2, ensure_ascii=False)

    # ── Company ─────────────────────────────────────────────────

    async def search_companies(self, query: str, limit: int = 10) -> dict[str, Any]:
        return await self._get("/v1/search/companies", {"q": query, "limit": limit})

    async def get_company(self, symbol: str, mode: str = "consolidated") -> dict[str, Any]:
        return await self._get(f"/v1/company/{symbol}", {"mode": mode})

    async def get_company_tab(self, symbol: str, tab: str, mode: str = "consolidated") -> dict[str, Any]:
        return await self._get(f"/v1/company/{symbol}/{tab}", {"mode": mode})

    async def compare_companies(self, symbols: list[str], mode: str = "consolidated") -> dict[str, Any]:
        return await self._get("/v1/compare", {"symbols": ",".join(symbols), "mode": mode})

    # ── Sectors ─────────────────────────────────────────────────

    async def list_sectors(self) -> dict[str, Any]:
        return await self._get("/v1/sectors")

    async def get_sector_data(self, sector: str, page: int = 1, limit: int = 50) -> dict[str, Any]:
        return await self._get(f"/v1/sectors/{sector}", {"page": page, "limit": limit})

    # ── Screens ─────────────────────────────────────────────────

    async def list_screens(self, page: int = 1, q: str | None = None, sort: str | None = None) -> dict[str, Any]:
        return await self._get("/v1/screens", {"page": page, "q": q, "sort": sort})

    async def get_screen_details(self, screen_id: int, slug: str, page: int = 1, limit: int = 50) -> dict[str, Any]:
        return await self._get(f"/v1/screens/{screen_id}/{slug}", {"page": page, "limit": limit})

    # ── Health ──────────────────────────────────────────────────

    async def health(self) -> dict[str, Any]:
        return await self._get("/health")

    async def ready(self) -> dict[str, Any]:
        return await self._get("/ready")
