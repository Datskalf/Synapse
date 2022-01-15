from discord import File
from os.path import join
from pathlib import Path
from PIL import Image
from io import BytesIO
from urllib.request import urlopen

URL = 'https://flux.phys.uit.no/Last24/Last24_and1a.gif'
fileLoc = join(Path(__file__).parent, 'Media', 'Aurora', '24hData.png')


def getSource():
	return 'I get my aurora data from https://geo.phys.uit.no'

def updateImg():
	print(fileLoc)
	img = Image.open(BytesIO(urlopen(URL).read()))
	img.seek(0)
	img.save(fileLoc)
	print(f'Saved image to {fileLoc}')


def getAurora24h():
	updateImg()

	return File(fileLoc)

if __name__ == '__main__':
    updateImg()
    img = Image.open(fileLoc)
    img.show()