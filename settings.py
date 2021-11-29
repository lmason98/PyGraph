"""
File: settings.py
Author: Luke Mason

Description: Main application development settings file
"""

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WIDTH = 800
HEIGHT = 900

PAD = 15

APP_NAME = 'PyGraph'  # Str of app name for window title
DEBUG = 1  # Puts the app in debug mode (extra logging to console).
LOG = 1  # Puts the app in log mode, (shows success/error messages in console).

COLOR = {
	'black': (0, 0, 0),
	'white': (255, 255, 255),
	'selected': (168, 255, 168)
}

FONT = 'Dubai'
FONT_SIZE = 25

# VIEWS = [
# 	'home',  # Main home app
# 	# 'graph',  # Graph interaction
# 	# 'save',  # Graph save/load
# 	# 'settings'  # App user settings
# ]