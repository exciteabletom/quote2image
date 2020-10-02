#!/usr/bin/env python3
from setuptools import setup
import sys

with open("./README.md", encoding="utf-8") as readme:
	long_description = readme.read()

setup(
	name="quote2image",
	version="0.3",

	description="Generate an image based on a quote.",
	long_description=long_description,
	long_description_content_type="text/markdown",

	url="https://github.com/exciteabletom/quote2image",
	author="Tommy Dougiamas",
	author_email="tom@digitalnook.net",

	classifiers=[
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3"
	],

	entry_points={
		"console_scripts": ["quote2image = quote2image.__main__:main"],
	},

	keywords="image-generation image-processing quote",

	packages=["quote2image"],

	python_requires=">=3.6",

	install_requires=["Pillow>=6.0"],

	extras_require={
		"gui": ["toga==0.3.0.dev23"]
	},

	package_data={
		"quote2image": ["flairs/*", "fonts/*"]
	}
)
