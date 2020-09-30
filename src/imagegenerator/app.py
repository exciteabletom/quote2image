"""
GUI frontend for generate.py
"""
import os

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

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

		submit_button = toga.Button(
			"Submit!",
			on_press=self.submit,
			style=Pack(padding=5)
		)
		main_box.add(message_box)
		main_box.add(submit_button)

		self.main_window = toga.MainWindow(title=self.formal_name)
		self.main_window.content = main_box
		self.main_window.show()

	def submit(self, widget):
		"""
		Compute the values and save an image.
		"""
		os.listdir()
		generate.main(self.message_input.value)


def main():
	return ImageGenerator()
