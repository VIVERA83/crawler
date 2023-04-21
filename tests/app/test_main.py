import asyncio

from app.main import main


async def test_main():
    assert isinstance(await asyncio.wait_for(main(), 1), list)
