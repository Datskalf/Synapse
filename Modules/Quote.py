import requests
from PIL import Image
from bs4 import BeautifulSoup as bs
from io import BytesIO
from os.path import join
from pathlib import Path

NEW_QUOTE_URL = 'https://inspirobot.me/api?generate=true'
MEDIA_FOLDER = join(Path(__file__).parent.parent, 'Media')

def getSource():
	return 'I get my quotes from https://inspirobot.me/api'

def getQuoteURL():
	response = requests.get(NEW_QUOTE_URL)
	return response.content.decode('utf-8')

    