from distutils.core import setup

# Dependencies are automatically detected, but it might need
# fine tuning.

import sys

setup(name='MUComicLoad',
	author = "Christoph \"Hammy\" Stahl",
	author_email = "christoph.stahl@uni-dortmund.de",
	url = "https://github.com/christofsteel/mucomicload",
	packages=['mucomic', 'mucomic.core', 'mucomic.Qt', 'mucomic.Qt.windows'],
	requires=['pyside', 'appdirs'],
	scripts=['mucomicload'],
	version = '2.0',
	description = 'Python downloader for Marvel Unlimited comic subscription')
