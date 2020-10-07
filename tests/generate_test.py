#!/usr/bin/env python3
"""
Run generate and show the output.

Not really a test but I'm calling it a test anyway.
"""
from quote2image import generate

generate.main("Testing quote2image!", debug=True, shadow=True)  # , noise_tint="#FF6F00")

