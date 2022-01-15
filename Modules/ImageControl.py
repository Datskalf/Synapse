from PIL import Image

def gifToPng(GIFImage):
	frame = GIFImage.seek(0)
	frame.save('tempImage.png')
	return 