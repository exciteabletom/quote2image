#!/usr/bin/env python3
"""
Main entrypoint
"""
import sys
import argparse
import os
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


fs_sep = path_convert("/")

if fs_sep in sys.argv[0]:
	# Get the directory the script is in
	script_dir_lst = sys.argv[0].split(fs_sep)[:-1]
	script_dir = fs_sep.join(script_dir_lst)

	# Change to that directory
	os.chdir(script_dir)

parser = argparse.ArgumentParser(description="Generate inspirational quote images.")
parser.add_argument("--path", "-p", dest="file_path", default=str(Path("./quote.png")),
					help="The path the png should be saved to")
parser.add_argument("--quote", "-q", dest="quote", default="", help="The quote to be used on the image.")

args = parser.parse_args()

if not args.quote:
	args.quote = input("Please enter a quote: ")

args.quote = textwrap.wrap(args.quote, width=20)
if len(args.quote) >= 3:
	start_height = 150
elif len(args.quote) == 2:
	start_height = 200
else:
	start_height = 250

# Paste flair into image
background = Image.new("RGB", (640, 640), (255, 255, 255))

for _ in range(2):
	flair_list = os.listdir(path_convert("flairs/"))
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
for line in args.quote:
	w, h = draw.textsize(line, font=font)
	draw.text(((background.width - w) / 2, current_height), line, (255, 95, 00), font=font)
	current_height += h + padding

background.save(args.file_path, "png")
