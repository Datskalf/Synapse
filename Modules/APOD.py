import aiohttp, asyncio
import json

from . import GetAPIKeys
from . import DiscordTextFormat as dtf
from discord import Embed

API_KEY = GetAPIKeys.getKey('NASA', 'API_KEY')
URL = f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}'


async def getSiteContent():
	async with aiohttp.ClientSession() as session:
		async with session.get(URL) as response:
			if response.status == 200:
#				print(await response.text())
				return await response.text()


async def fetchAPOD():
	APOD = json.loads(await getSiteContent())

	emb = Embed()
	emb.color = 0xff9900
	emb.title = APOD['title']
	emb.set_image(url=APOD['hdurl'])
	desc = 'Copyright: {}\nDate: {}\n\n'.format(dtf.bold(APOD['copyright']), dtf.bold(APOD['date']))
	desc += dtf.italic(APOD['explanation'])
	emb.description = desc

	return emb


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(getSiteContent())