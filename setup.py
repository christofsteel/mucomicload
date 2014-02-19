#!/usr/bin/env python3
from distutils.core import setup

setup(name="mucomicload",
	version = "2.0",
	description = "Python downloader for Marvel Unlimited comic subscription",
	author = "Christoph \"Hammy\" Stahl",
	author_email = "christoph.stahl@uni-dortmund.de",
	url = "https://github.com/christofsteel/mucomicload",
	packages=['MUComic'],
	requires=['pyside', 'appdirs'],
	package_dir={'' : 'src/'},
	package_data={'': ['res/*.*']},
	include_package_data=True,
	scripts=['src/mucomicload'])
