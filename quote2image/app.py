"""
GUI frontend for generate.py.
"""
import os
import random

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, BOTTOM, TOP, LEFT, RIGHT

from . import generate


class ImageGenerator(toga.App):
	"""
	Main class for the GUI
	"""

	def startup(self):
		"""
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
		main_box = toga.Box(style=Pack(direction=COLUMN))

		message_label = toga.Label(
			"Message to be placed on image: ",
			style=Pack(padding=(0, 5))
		)
		self.message_input = toga.TextInput(style=Pack(flex=1))

		message_box = toga.Box(style=Pack(direction=ROW, padding=5))
		message_box.add(message_label)
		message_box.add(self.message_input)

		# Whether text shadow should be added or not
		shadow_box = toga.Box(style=Pack(direction=ROW, padding=5))

		shadow_label = toga.Label(
			"Add shadow to text ",
			style=Pack(padding=(5))
		)
		self.shadow_check = toga.Switch(
			"",
			style=Pack(padding=5)
		)

		shadow_box.add(shadow_label)
		shadow_box.add(self.shadow_check)
		main_box.add(shadow_box)

		noise_box = toga.Box(
			style=Pack(direction=ROW, padding=5)
		)

		main_box.add(noise_box)

		# The amount of graphics to be overlaid on the image
		noise_modifier_label = toga.Label(
			"Amount of background images ",
			style=Pack(padding=(20, 5))
		)

		self.noise_modifier = toga.NumberInput(
			min_value=0,
			max_value=4,
			default=2,
			style=Pack(padding=(20, 5))
		)

		noise_box.add(noise_modifier_label)
		noise_box.add(self.noise_modifier)

		self.main_window = toga.MainWindow(title=self.formal_name)

		submit_button = toga.Button(
			"Submit!",
			on_press=self.submit,
			style=Pack(padding=5)
		)
		main_box.add(message_box)
		main_box.add(submit_button)

		self.main_window.content = main_box
		self.main_window.show()

	def submit(self, widget):
		"""
		Create the Image.
		"""
		os.listdir()
		img = generate.main(self.message_input.value,
					      shadow=self.shadow_check.is_on,
					      noise=self.noise_modifier.value)

		self.save_image(img)

	def save_image(self, img):
		"""
		Show the user the image and save it to a location.

		:param img: A PIL.Image instance
		:return: Where the image was saved, empty string otherwise
		"""
		disallowed_chars = (" ", "'", "\"")
		file_name = f"{self.message_input.value[0:8]}-{str(random.random())[2:7]}"

		for char in file_name:
			if char in disallowed_chars:
				file_name = file_name.replace(char, "")

		img.show()

		file_path = ""
		if self.main_window.question_dialog("Save this image?", "Would you like to save this image?"):
			try:
				file_path = self.main_window.save_file_dialog(
					"Save image where?",
					file_name,
					["png", ".png"]
				)
			except ValueError:
				return ""

			img.save(file_path)

		return file_path


def main():
	"""
	Main entrypoint for the GUI.

	:rtype: toga.App
	:return: toga.App instance
	"""
	return ImageGenerator('quote2image', 'net.digitalnook.quote2image')

