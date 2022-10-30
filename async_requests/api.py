import asyncio
import aiohttp
from tqdm import tqdm

def get(urls, headers=None, params=None, retry:int =0):
	results = asyncio.run(_async_get(urls, headers, params, retry))
	return results

async def _async_get(urls, headers, params, retry):
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(_async_get_chunk(session, url, params, retry)))
        results = []
        for future in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            result = await future
            results.append(result)
    return results

async def _async_get_chunk(session, url, params, max_retry):
	retry = 0
	while retry <= max_retry:
		try:
			async with session.get(url, params=params) as resp:
				if resp.status != 200:
					retry += 1
					continue
				else:
					await resp.read()
					return resp
		except aiohttp.client_exceptions.ClientPayloadError as e:
			retry += 1
			continue
