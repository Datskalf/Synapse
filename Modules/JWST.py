import requests, json, discord
from bs4 import BeautifulSoup as bs
from . import DiscordTextFormat as dtf


JWSTDataURL = 'https://api.jwst-hub.com/track'



def tempDelta(temps):
	maxC = max(temps)
	minC = min(temps)
	return maxC - minC

def getJWSTData():
	response = requests.get(JWSTDataURL)
	soup = bs(response.content, 'lxml')
	jsonData = json.loads(soup.find('p').text)
	return jsonData


def getSource():
	return f'I get my JWST data from {JWSTDataURL}'

async def createDiscordEmbedJWSTData():
	data = getJWSTData()
	emb = discord.Embed()
	emb.color = 0xD1C520
	
	emb.title = "James Webb telescope launch: T+" + data['launchElapsedTime']
	emb.set_image(url=data['deploymentImgURL'])
	desc = "\n"
	
	percent = data['percentageCompleted']
	desc += "JWST has currently travelled " + dtf.bold(str(data['distanceEarthKm'])) + " km, with " + dtf.bold(str(data['distanceL2Km'])) + " km remaining. (" + str(round(percent, 2)) + "%)" + "\n"
	desc += dtf.createProgressBar(percent) + "\n\n"
	desc += "Current velocity: " + dtf.bold(str(data['speedKmS'])) + " km/s" + "\n\n"
	temps = [data['tempC']['tempWarmSide1C'], data['tempC']['tempWarmSide2C'], data['tempC']['tempCoolSide1C'], data['tempC']['tempCoolSide2C']]
	desc += "Warm side 1: " + dtf.bold(str(temps[0])) + u" \N{DEGREE SIGN}C" + "\n"
	desc += "Warm side 2: " + dtf.bold(str(temps[1])) + u" \N{DEGREE SIGN}C" + "\n"
	desc += "Cool side 1: " + dtf.bold(str(temps[2])) + u" \N{DEGREE SIGN}C" + "\n"
	desc += "Cool side 2: " + dtf.bold(str(temps[3])) + u" \N{DEGREE SIGN}C" + "\n"
	desc += "Largest \u0394 in temperature: " + dtf.bold(str(round(tempDelta(temps), 2))) + u" \N{DEGREE SIGN}C" + "\n\n"
	
	desc += "Current deployment step:" + "\n" + dtf.bold(data['currentDeploymentStep'])
	
	emb.description = desc

	return emb
