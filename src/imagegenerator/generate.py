"""
The backend logic that creates the image.

'main' is the entrypoint.
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

	return str(Path(f"{Path.home()}/Pictures/quote.png"))


def main(quote, file_path=default_file_path()):
	"""
	Saves a png with 'quote' printed on it to 'file_path'

	:param quote: The message to be printed on the image
	:param file_path: Where to save the png file (defaults to ~/Pictures/)
	:rtype: bool
	:return: True on success,  False otherwise
	"""

	fs_sep = path_convert("/")

	if fs_sep in sys.argv[0]:
		# Get the directory the script is in
		script_dir_lst = sys.argv[0].split(fs_sep)[:-1]
		script_dir = fs_sep.join(script_dir_lst)

		# Change to that directory
		os.chdir(script_dir)

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

	for _ in range(2):
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
		draw.text(((background.width - w) / 2, current_height), line, (255, 95, 00), font=font)
		current_height += h + padding

	background.save(file_path, "png")
