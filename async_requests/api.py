import asyncio
import aiohttp
from tqdm import tqdm

def get(urls, headers=None, params=None, retry:int =0):
	results = asyncio.run(_async_get(urls, headers, params, retry))
	return results

async def _async_get(urls, headers, params, retry):
	bar = tqdm(total=len(urls))
	results = []
	while True:
		try:
			async with aiohttp.ClientSession(headers=headers) as session:
				tasks = []
				for url in urls:
					tasks.append(asyncio.ensure_future(_async_get_chunk(session, url, params, retry)))
				for future in asyncio.as_completed(tasks):
					result = await future
					bar.update(1)
					results.append(result)
		except aiohttp.client_exceptions.ServerDisconnectedError as e:
			for result in results:
				if str(result._url) in urls:
					urls.remove(str(result._url))
			continue
		break
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
		except Exception as e:
			retry += 1
			continue
