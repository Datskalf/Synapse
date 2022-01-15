from configparser import ConfigParser
from os.path import join
from pathlib import Path

API_KEY_PATH = join(Path(__file__).parent.parent, 'SETTINGS.ini')
config = ConfigParser()
config.read(API_KEY_PATH)

def getKey(category, keyName):
	return config[category][keyName]