def bold(string):
	return '**' + string + '**'

def italic(string):
	return '*' + string + '*'

def code(string):
	return '```\n' + string + '\n```'

def createProgressBar(percentageComplete=0):
	width = 25
	progressLetterText = '▇'
	progressLetterEmpty = '—'

	progress = round((percentageComplete/100)*width)

	progressText = ""
	for _ in range(progress):
		progressText += progressLetterText
	for _ in range(width-progress):
		progressText += progressLetterEmpty

	progressBar = '[' + progressText + ']'

	return bold(progressBar)


