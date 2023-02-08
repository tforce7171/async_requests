import asyncio
import aiohttp
from tqdm import tqdm

def get(urls, headers=None, params=None, retry:int =0, timeout=None, async_limit:int = 100):
	split_urls = [urls[idx:idx + async_limit] for idx in range(0,len(urls), async_limit)]
	results = []
	pbar = tqdm(total=len(urls))
	for each_urls in split_urls:
		each_results = asyncio.run(_async_get(pbar, each_urls, headers, params, retry, timeout))
		results.extend(each_results)
	return results

async def _async_get(pbar, urls, headers, params, retry, timeout):
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(_async_get_chunk(session, url, params, retry, timeout)))
        results = []
        for future in asyncio.as_completed(tasks):
            result = await future
            results.append(result)
            pbar.update(1)
    return results

async def _async_get_chunk(session, url, params, max_retry, timeout_seconds):
	retry = 0
	while retry <= max_retry:
		try:
			async with session.get(url, params=params, timeout=timeout_seconds) as resp:
				if resp.status != 200:
					retry += 1
					continue
				else:
					await resp.read()
					return resp
		except aiohttp.client_exceptions.ClientPayloadError as e:
			retry += 1
			continue
		except aiohttp.client_exceptions.ServerDisconnectedError as e:
			retry += 1
			continue
		except aiohttp.client_exceptions.ClientConnectorError as e:
			retry += 1
			continue
		except asyncio.exceptions.TimeoutError as e:
			retry += 1
			continue
	return None
