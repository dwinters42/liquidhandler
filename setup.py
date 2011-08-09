#!/bin/env python

# Copyright (c) 2010,2011 Daniel Gruber <daniel@tydirium.org>
#
# Permission to use, copy, modify, and distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA
# OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

from distutils.core import setup

setup(name='py-liquidhandler',
      version="0.4",
      license="BSD",
      description='Control program and python interface to Waters 2700 (and compatible) liquid handling robots',
      long_description='''
This is a library and a GUI control program written in Python for
controlling a Waters 2700 Sample Manager (and compatible) liquid
handling robot. These are quite common in Mass spectrometry labs and
typically have 1-2 arms with attached syringes and one 6-port valve.

The library allows to easily 

  *  control the movements of up to 2 arms
  *  control the syringe pump and 6-port valve to dispense and draw
     liquids from a reservoir or e.g. a 96-well plate
  *  save and recall positions (like "wash", "A1" on a plate, etc.) for
     easier scripting

The GUI program provides a platform-independent graphical interface
for the library. However, the library can be used without the GUI
part.
''',
      author='Daniel Gruber',
      author_email="daniel@tydirium.org",
      package_dir={'liquidhandler': ''},
      package_data={'liquidhandler': ['README.txt']},
      url="http://www.tydirium.org/daniel/py-liquidhandler.html",
      packages=['liquidhandler'],
      scripts=['Liquidator'],
      keywords="robot liquid handler lab equipment",
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        ])
