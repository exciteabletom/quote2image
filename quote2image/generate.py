"""
The backend logic that creates the image.
"""
import os
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageEnhance, ImageFilter
from pathlib import Path


def path_convert(path):
	"""
	Convert a string to the correct file path depending on the system.

	:param path: A file Path
	:return: OS agnostic file path
	"""
	return str(Path(path))


# A list of random colours that can be picked from

def random_color():
	"""
	Gets a random color

	:return: A random color RGB tuple
	"""
	colors_rand = [
		(153, 255, 153),
		(100, 200, 0),
		(255, 153, 0),
		(255, 153, 204),
		(0, 255, 255),
		(0, 255, 153),
		(204, 102, 255),
		(255, 80, 80)
	]

	return colors_rand[random.randint(0, len(colors_rand) - 1)]



def hex_to_rgb(hex_str):
	"""
	Converts a hex_str colour string to an RGB tuple.

	E.g. "#FFFFFF" --> (255, 255, 255)

	:param hex_str: A hexadecimal colour string. Can start with '#' or not

	:raises ValueError: if
	:return: A tuple represented RGB values
	"""
	# List of valid hex_str values
	hex_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

	# Convert hex_str string to upper case
	hex_str = hex_str.upper()

	# Remove hashtags from string if they exist
	hex_str = hex_str.replace("#", "")

	if len(hex_str) != 6:
		raise ValueError("Hex string is the incorrect length")

	for char in hex_str:
		# Check validity of hex_str string
		if char not in hex_values:
			raise ValueError("Invalid characters in hex string.")

	# #FFFFFF becomes ['FF', 'FF', 'FF']
	hex_pairs = [hex_str[0:2], hex_str[2:4], hex_str[4:6]]
	rgb_pairs = []

	for pair in hex_pairs:
		# Hex to int
		rgb_pairs.append(int(pair, 16))

	# Return as an immutable tuple
	return tuple(rgb_pairs)


def tint_image(img: Image, color):
	"""
	Tint an image a certain colour and then blur it slightly.

	:param img: A PIL.Image instance
	:param color: Either a hex string or an RGB tuple.
	:return: A tinted and slightly blurred image.
	"""

	# Get the alpha channel of the image
	alpha = img.split()[-1]

	# Convert Image to greyscale
	gray_scale = ImageOps.grayscale(img)

	# Fix reduced contrast on Image
	gray_scale = ImageOps.autocontrast(gray_scale)

	# Tint the greyscale image
	tinted = ImageOps.colorize(gray_scale, (0, 0, 0, 0), color)

	# raise brightness of image
	tinted = ImageEnhance.Brightness(tinted).enhance(1.5)

	# Return alpha channel
	tinted.putalpha(alpha)



	return tinted


def main(quote, **kwargs):
	"""
	Creates a PIL Image with 'quote' printed on it.

	:param quote: The message to be printed on the image

	:keyword shadow: Whether to add shadow to the text or not.
	:keyword noise: The amount of graphics to be overlaid on the image

	:keyword text_color: The colour of the text as a hex string.
	:keyword shadow_color: The colour of the text shadow as a hex string.
	:keyword background_color: The colour of the background as a hex string.
	:keyword noise_tint: The colour to tint background noise elements

	:keyword debug: Boolean to show the image after creating it or not.

	:rtype: PIL.Image
	:return: A PIL image object
	"""

	# Parse kwarg options
	shadow = kwargs.get("shadow")

	# Noise is passed as a Decimal instance so we convert it to int
	noise = kwargs.get("noise")

	if noise is None:
		noise = 2
	else:
		noise = int(noise)

	# Get custom colors
	colors_default = {
		"background": (255, 255, 255),
		"text": random_color(),
		"shadow": (75, 75, 75),
		"noise": None
	}

	colors = {
		"text": kwargs.get("text_color"),
		"shadow": kwargs.get("shadow_color"),
		"background": kwargs.get("background_color"),
		"noise": kwargs.get("noise_tint")
	}

	for key, value in colors.items():
		if not value:
			colors[key] = colors_default[key]

	# Debug mode
	debug = kwargs.get("debug")

	# Go to the directory containing this module
	file_prefix = str(Path(__file__).parent)

	quote = textwrap.wrap(quote, width=20)

	if len(quote) >= 3:
		start_height = 150
	elif len(quote) == 2:
		start_height = 200
	else:
		start_height = 250

	main_img = Image.new("RGB", (640, 640), colors["background"])

	# Paste flair into image
	flair_list = os.listdir(path_convert(f"{file_prefix}/flairs/"))

	for _ in range(noise):
		flair_name = flair_list[random.randint(0, len(flair_list) - 1)]
		flair_list.remove(flair_name)

		flair_path = path_convert(f"{file_prefix}/flairs/{flair_name}")
		flair = Image.open(flair_path)

		if colors["noise"]:
			flair = tint_image(flair, colors["noise"])
		else:
			# Random colors
			if random.random() > 0.5:
				rand_color = random_color()
				flair = tint_image(flair, rand_color)

		main_img.paste(flair, (0, 0), flair)

	# Add text to image
	font = ImageFont.truetype(path_convert(f"{file_prefix}/fonts/playlist_script.otf"), size=64)
	draw = ImageDraw.Draw(main_img)

	current_height = start_height
	padding = 20
	for line in quote:
		w, h = draw.textsize(line, font=font)

		# Text shadow is a grey text layer slightly offset to the normal text
		if shadow:
			draw.text((((main_img.width - w) / 2) - 2, current_height - 2), line, colors["shadow"], font=font,
					  align="center")

		draw.text(((main_img.width - w) / 2, current_height), line, colors["text"], font=font, align="center")
		current_height += h + padding

	if debug:
		main_img.show()

	return main_img
