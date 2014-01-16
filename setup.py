#!/usr/bin/env python3
from distutils.core import setup

setup(name="marvelload",
	version = "1.0",
	description = "Python downloader for Marvel Unlimited comic subscription",
	author = "Christoph \"Hammy\" Stahl",
	author_email = "christoph.stahl@uni-dortmund.de",
	url = "https://github.com/christofsteel/marvelload",
	packages=['Marvel'],
	package_dir={'' : 'src/'},
	scripts=['src/marvelload'])
