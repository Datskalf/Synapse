import discord
from discord.ext import commands
from Modules import GetAPIKeys


from Modules import JWST, Aurora, MarsRovers, Quote, APOD



# Bot settings
TOKEN = GetAPIKeys.getKey('DISCORD', 'BOT_TOKEN')
bot = commands.Bot(command_prefix='!')




@bot.event
async def on_ready():
	print(f'{bot.user.name} har logged on!')


@bot.command(name='ping', help="Responds to show whether I'm live or not")
async def ping(ctx):
	await ctx.send("Pong!")


@bot.command(name='source', help="Returns my sources")
async def source(ctx, *args):
	if not args or not args[0] in ['jwst', 'aurora', 'rover', 'quote']:
		await ctx.send('Syntax: [ jwst | aurora | rover | quote ]')

	arg = args[0].lower()
	if arg == 'jwst':
		await ctx.send(JWST.getSource())
	elif arg == 'aurora':
		await ctx.send(Aurora.getSource())
	elif arg == 'rover':
		await ctx.send(await MarsRovers.getSource())
	elif arg == 'quote':
		await ctx.send(Quote.getSource())


@bot.command(name='jwst', help="Fetches live data from the James Webb satellite")
async def info(ctx):
	await ctx.send(embed=await JWST.createDiscordEmbedJWSTData())


@bot.command(name='aurora', help='Returns live 24h data of activity in the magnetosphere')
async def aurora(ctx):
	await ctx.send(file=Aurora.getAurora24h())


@bot.command(name='quote', help='Sends an A.I. generated quote')
async def quote(ctx):
    emb = discord.Embed()
    emb.set_image(url=Quote.getQuoteURL())
    await ctx.send(embed=emb)


@bot.command(name='rover', help='Fetches the latest image from the named mars rover')
async def rover(ctx, *args):
	if not args:
		await ctx.send('Syntax: [ Curiosity | Opportunity | Perseverance | Spirit ]')
		return

	if not args[0].lower() in ['curiosity', 'spirit', 'perseverance', 'opportunity']:
		await ctx.send("I'm sorry, I don't recognize that rover. Please check your spelling and try again")
		return

	await MarsRovers.getLatestImage(ctx, args[0])


@bot.command(name='poll', help='Creates a basic poll')
async def poll(ctx, *args):
	text = ''
	if int(args[0]) in range(10):
		numEmojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
		
		for arg in args[1:]:
			text += arg + ' '

		msg = await ctx.send(text)
		for i in range(int(args[0])):
			await msg.add_reaction(numEmojis[i])
		return
	
	for arg in args[0:]:
		text += arg + ' '

		msg = await ctx.send(text)
		await msg.add_reaction('✅')
		await msg.add_reaction('❌')


@bot.command(name='apod', help='Sends NASAs Astronomy picture of the day')
async def apod(ctx):
	await ctx.send(embed=await APOD.fetchAPOD())


bot.run(TOKEN)