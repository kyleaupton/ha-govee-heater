"""Sample API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class GoveeHeaterApiClientError(Exception):
    """Exception to indicate a general API error."""


class GoveeHeaterApiClientCommunicationError(
    GoveeHeaterApiClientError
):
    """Exception to indicate a communication error."""


class GoveeHeaterApiClientAuthenticationError(
    GoveeHeaterApiClientError
):
    """Exception to indicate an authentication error."""


class GoveeHeaterApiClient:
    """Sample API Client."""

    def __init__(
        self,
        api_key: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._api_key = api_key
        self._session = session

    async def async_get_devices(self) -> any:
        """Get devices."""
        return await self._api_wrapper(
            method="get",
            url="https://developer-api.govee.com/v1/appliance/devices"
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            _headers = {
                "Govee-API-Key": self._api_key
            }

            if headers != None:
                _headers = {
                    **_headers,
                    **headers,
                }

            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=_headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise GoveeHeaterApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise GoveeHeaterApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise GoveeHeaterApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise GoveeHeaterApiClientError(
                "Something really wrong happened!"
            ) from exception
