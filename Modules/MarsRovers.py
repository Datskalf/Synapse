from datetime import datetime, timedelta
from discord import Embed, File
from pathlib import Path
from io import BytesIO
from PIL import Image
from . import GetAPIKeys

import aiohttp
from requests import get
from os.path import join
from json import loads


URL = 'https://api.nasa.gov/mars-photos/api/v1/rovers/{}/latest_photos?earth_date={}&api_key={}'


async def getImage(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			return Image.open(BytesIO(await response.text()))

async def saveImage(url, roverName):
	img = await getImage(url)
	imgPath = join(Path(__file__).parent, 'Media', 'MarsRovers', f'{roverName}.png')
	img.save(imgPath)
	return imgPath

async def getSource():
    return 'I get my rover data from https://api.nasa.gov'


async def getLatestImage(ctx, roverName):
	date = datetime.utcnow()
	dayMax = 7

	for _ in range(dayMax):
		dateAsString = date.strftime('%Y-%m-%d')
		async with aiohttp.ClientSession() as session:
			async with session.get(URL.format(roverName, dateAsString, GetAPIKeys.getKey('NASA', 'API_KEY'))) as response:
				data = loads(await response.text())['latest_photos']

		if len(data) > 0:
			embed = Embed()
			embed.title = f'Latest image from the {roverName} rover'
			embed.description = f'Image was received {data[-1]["earth_date"]} on its sol {data[-1]["sol"]}'
			embed.description += f'\nImage was taken by the rovers {data[-1]["camera"]["name"]} camera'
			file = File(saveImage(data[-1]['img_src'], roverName), 'image.png')
			embed.set_image(url="attachment://image.png")
			await ctx.send(file=file, embed=embed)
			return

		date -= timedelta(days=1)

	await ctx.send(f'No images found in the last {dayMax} days')