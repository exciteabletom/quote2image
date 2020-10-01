"""
The backend logic that creates the image.
"""
import os
import sys
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw
from pathlib import Path


def path_convert(path):
	"""
	Convert a string to the correct file path depending on the system.

	:param path: A file Path
	:return: OS agnostic file path
	"""
	return str(Path(path))


def default_file_path():
	"""
	Return the OS equivalent of ~/Pictures/quote.png

	:rtype: str
	"""

	return str(Path(f"{Path.home()}/Pictures/generated_image.png"))


def main(quote, file_path=default_file_path(), **kwargs):
	"""
	Saves a png with 'quote' printed on it to 'file_path'.


	:param quote: The message to be printed on the image
	:param file_path: Where to save the png file (defaults to ~/Pictures/)

	:keyword shadow: Whether to add shadow to the text or not.
	:keyword noise: The amount of graphics to be overlaid on the image

	:rtype: bool
	:return: True on success,  False otherwise
	"""

	# Parse kwarg options
	shadow = kwargs.get("shadow")

	# Noise is passed as a Decimal instance so we convert it to int
	noise = kwargs.get("noise")

	if noise is None:
		noise = 2
	else:
		noise = int(noise)

	os.chdir(str(Path(__file__).parent))

	quote = textwrap.wrap(quote, width=20)

	if len(quote) >= 3:
		start_height = 150
	elif len(quote) == 2:
		start_height = 200
	else:
		start_height = 250

	# Paste flair into image
	background = Image.new("RGB", (640, 640), (255, 255, 255))

	flair_list = os.listdir(path_convert("flairs/"))

	for _ in range(noise):
		flair_name = flair_list[random.randint(0, len(flair_list) - 1)]
		flair_list.remove(flair_name)

		flair_path = path_convert(f"flairs/{flair_name}")
		flair = Image.open(flair_path)

		background.paste(flair, (0, 0), flair)

	# Add text to image
	font = ImageFont.truetype("fonts/playlist_script.otf", size=64)
	draw = ImageDraw.Draw(background)

	current_height = start_height
	padding = 20
	for line in quote:
		w, h = draw.textsize(line, font=font)

		# Text shadow is a grey text layer slightly offset to the normal text
		if shadow:
			draw.text((((background.width - w) / 2) - 2, current_height - 2), line, (75, 75, 75), font=font, align="center")

		draw.text(((background.width - w) / 2, current_height), line, (255, 95, 00), font=font, align="center")
		current_height += h + padding

	background.save(file_path, "png")

	return True
