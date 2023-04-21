import asyncio

from app.main import main


async def test_main():
    """Тест на корректный запуск"""
    assert isinstance(await asyncio.wait_for(main(), 1), list)
