liquidhandler - control Waters 2700 and compatible Liquid Handling Robots
==================================================================================

Author:  <daniel@tydirium.org>

This is a library and a GUI control program written in Python for
controlling a Waters 2700 Sample Manager (and compatible) liquid
handling robot. These are quite common in Mass spectrometry labs and
typically have 1-2 arms with attached syringes and one 6-port valve.

The library allows to easily 

- control the movements of up to 2 arms
- control the syringe pump and 6-port valve to dispense and draw
  liquids from a reservoir or e.g. a 96-well plate
- save and recall positions (like "wash", "A1" on a plate, etc.) for
  easier scripting

The GUI program provides a platform-independent graphical interface
for the library. However, the library can be used without the GUI part.

The author is Daniel Gruber <daniel@tydirium.org>, please contact me
in case of questions or problems.

Table of Contents
=================
1 News 
2 Downloads 
3 Installation 
4 Using the library 
5 Using the GUI 


1 News 
~~~~~~~

- *15/8/2011*: Version 0.5, more bugfixes and it looks nice on Windows
  now!
- *09/08/2011*: Version 0.4, lot's of bugfixes, I use it on a daily
  basis at the moment.

2 Downloads 
~~~~~~~~~~~~

The source code and binary installers for Windows can be downloaded
[here].


[here]: http://pypi.python.org/pypi/py-liquidhandler

3 Installation 
~~~~~~~~~~~~~~~

Prerequisites: You will need the [Python interpreter] and the following
Python modules: 

- [py-serial]
- [py-yaml]

And additionally for the GUI part

- [wxPython]

After having these installed, run the binary installer (for Windows)
or run "python setup.py install" from the commandline on Unix.


[Python interpreter]: http://www.python.org
[py-serial]: http://pyserial.sourceforge.net/
[py-yaml]: http://pyyaml.org/
[wxPython]: www.wxpython.org

4 Using the library 
~~~~~~~~~~~~~~~~~~~~

A typical usage pattern would be

  import liquidhandler
  
  r=liquidhandler.Robot()
  r.Move([100,100,50])
  r.AddPosition('wash')
  
  r.Move([1000,100,50])
  r.AddPosition('sample')
  
  r.Goto('sample')
  r.Draw(100,'sample')
  r.Goto('wash')
  r.Dispense(100)


5 Using the GUI 
~~~~~~~~~~~~~~~~

Just start the "Liquidator" script.
