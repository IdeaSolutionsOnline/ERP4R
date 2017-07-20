#!/usr/bin/env python
try:
	from PIL import Image, ImageOps
except ImportError:
	import Image
	import ImageOps
import os

def normalize(image, file_name):
	if image.mode not in ("L", "RGB"):
		image = image.convert("RGB")
	width, height = image.size
	if height > width:
		image = image.rotate(270)
	if width > 100 or height > 60:
		image.thumbnail((100,0), Image.ANTIALIAS)
	image.save(file_name, 'JPEG', quality=75)

for image_dir in ['comida', 'bebidas', 'outros']:
	for root, dirs, files in os.walk(os.path.join('/var/www/core/static/files/Public/pos',image_dir)):
		for f in os.listdir(root):
			if f in files:
				file_name = os.path.join(root,f)
				print (file_name)
				image = Image.open(file_name)
				normalize (image, file_name)





