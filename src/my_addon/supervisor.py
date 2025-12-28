"""Home Assistant Supervisor API client."""

import logging
import os
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class SupervisorAPI:
    """Client for communicating with Home Assistant Supervisor."""

    def __init__(self, session: aiohttp.ClientSession | None = None):
        """Initialize Supervisor API client.

        Args:
            session: Optional aiohttp session (will create one if not provided)
        """
        self.token = os.getenv("SUPERVISOR_TOKEN")
        self.base_url = "http://supervisor"
        self._session = session
        self._own_session = session is None

    async def __aenter__(self) -> "SupervisorAPI":
        """Async context manager entry."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        if self._own_session and self._session:
            await self._session.close()

    def _get_headers(self) -> dict[str, str]:
        """Get headers for Supervisor API requests."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def _request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> dict[str, Any]:
        """Make a request to the Supervisor API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments for aiohttp request

        Returns:
            JSON response as dict

        Raises:
            aiohttp.ClientError: If request fails
        """
        if not self._session:
            raise RuntimeError("Session not initialized")

        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()

        logger.debug("Supervisor API request: %s %s", method, endpoint)

        async with self._session.request(
            method, url, headers=headers, **kwargs
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_info(self) -> dict[str, Any]:
        """Get Supervisor information.

        Returns:
            Supervisor info as dict
        """
        return await self._request("GET", "info")

    async def get_addon_info(self) -> dict[str, Any]:
        """Get information about this add-on.

        Returns:
            Add-on info as dict
        """
        return await self._request("GET", "addons/self/info")

    async def get_homeassistant_api_info(self) -> dict[str, Any]:
        """Get Home Assistant API information.

        Returns:
            Home Assistant API info including URL and token
        """
        return await self._request("GET", "homeassistant/api")

    async def ping_homeassistant(self) -> bool:
        """Check if Home Assistant is accessible.

        Returns:
            True if Home Assistant is accessible, False otherwise
        """
        try:
            await self._request("GET", "homeassistant/api")
            return True
        except Exception as e:
            logger.warning("Failed to ping Home Assistant: %s", e)
            return False
