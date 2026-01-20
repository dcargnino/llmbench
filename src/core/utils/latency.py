"""Utilities for measuring network latency."""

import asyncio
from urllib.parse import urlparse

import aiohttp

from src.core.constants import DEFAULT_LATENCY_ATTEMPTS


async def measure_latency(base_url: str, attempts: int = DEFAULT_LATENCY_ATTEMPTS) -> float:
    """Measure average network latency to a base URL.

    Performs multiple HTTP GET requests to the base URL and calculates
    the average response time.

    Args:
        base_url: The base URL to test latency for.
        attempts: Number of requests to make for averaging (default: 5).

    Returns:
        Average latency in milliseconds.

    Raises:
        ValueError: If base_url is invalid or empty.
        RuntimeError: If HTTP requests fail.
    """
    if not base_url:
        raise ValueError("Empty base URL")

    parsed = urlparse(base_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Invalid base URL")

    test_url = f"{parsed.scheme}://{parsed.netloc}"

    latencies = []
    async with aiohttp.ClientSession() as session:
        for _ in range(attempts):
            start = asyncio.get_event_loop().time()
            try:
                async with session.get(test_url) as response:
                    await response.read()  # Consume the response
                latency = (asyncio.get_event_loop().time() - start) * 1000  # ms
                latencies.append(latency)
            except Exception as e:
                raise RuntimeError(f"HTTP GET error: {e}")

    return sum(latencies) / len(latencies)