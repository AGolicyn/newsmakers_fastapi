import asyncio
import pytest


@pytest.mark.asyncio
async def test_smoke():
    await asyncio.sleep(1)
