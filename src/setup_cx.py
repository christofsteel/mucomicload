from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
	Executable('mucomicload', base=base)
]

setup(name='MUComicLoad',
	author = "Christoph \"Hammy\" Stahl",
	author_email = "christoph.stahl@uni-dortmund.de",
	url = "https://github.com/christofsteel/mucomicload",
	packages=['mucomic'],
	requires=['pyside', 'appdirs'],
	scripts=['mucomicload'],
	version = '2.0',
	description = 'Python downloader for Marvel Unlimited comic subscription',
	executables = executables)
