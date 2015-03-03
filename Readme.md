About
=====

This is a library and a GUI control program for controlling liquid
handling robots compatible with the Waters 2700 Sample Manager. These
are quite common in Mass spectrometry labs and typically have 1-2 arms
with attached syringes and one 6-port valve.

The library can be used without the GUI and allows to 

-   control the movements of up to 2 arms
-   control the syringe pump and 6-port valve to dispense and draw
    liquids from a reservoir or e.g. a 96-well plate
-   save and recall positions (like "wash", "A1" on a plate, etc.) for
    easier scripting

The author is Daniel Winters <daniel@tydirium.org>. Please contact me
in case of questions or problems.

Downloads
=========

The source code and binary installers for Windows can be downloaded
from [PyPi](https://pypi.python.org/pypi/py-liquidhandler). This
[fossil](http://fossil-scm.org) source code repository can be cloned
as well.

Installation
============

Prerequisites: You will need the [Python
interpreter](https://www.python.org) and the following Python modules:

-   [py-serial](http://pyserial.sourceforge.net/)
-   [py-yaml](http://pyyaml.org/)
-   [wxPython](http://www.wxpython.org) - only necessary for the GUI part

Usage
=====

For using the graphical interface, start the "Liquidator.py" script
and explore. A simple python script using the library is in the
[examples](./examples/simple.py).
