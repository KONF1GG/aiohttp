import asyncio
import aiohttp


async def main():
    session = aiohttp.ClientSession()
    response = await session.post(
        'http://127.0.0.1:8080/hello/world/42?a=1&b=2',
        json={'key': 'value'},
        headers={'Content-Type': 'application/json'},
    )
    print(await response.json())
    await session.close()

asyncio.run(main())
