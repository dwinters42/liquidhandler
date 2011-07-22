liquidator - control Waters 2700 and compatible Liquid Handling Robots
======================================================================

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

1 Installation 
~~~~~~~~~~~~~~~

Prerequisites: You will need the [Python interpreter] and the following
Python modules: 

- [py-serial]
- [py-yaml]

And additionally for the GUI part

- [wxPython]

After having these installed, run the binary installer (for Windows)
or run "sudo python setup.py install" from the commandline on Unix.


[Python interpreter]: http://www.python.org
[py-serial]: http://pyserial.sourceforge.net/
[py-yaml]: http://pyyaml.org/
[wxPython]: www.wxpython.org

2 Using the library 
~~~~~~~~~~~~~~~~~~~~

A typical usage pattern would be

  import liquidator
  
  r=liquidator.Robot()
  r.Move([100,100,50])
  r.AddPosition('wash')
  
  r.Move([1000,100,50])
  r.AddPosition('sample')
  
  r.Goto('sample')
  r.Draw(100,'sample')
  r.Goto('wash')
  r.Dispense(100)


3 Using the GUI 
~~~~~~~~~~~~~~~~

Just start the "Liquidator" script.

4 Description of the Robot serial protocol 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a reverse-engineered description of the serial protocol for
reference.

4.1 High-level command protocol 
================================

The protocol is the following:

- Send a command, e.g. "A18PA 100 100 100" (address 18 = arm1, PA: move to
  position (100,100,100))
- Read "command accepted" return message "@18" from robot
- Read optional information messages like "Q18"
- Contiue reading until "command finished" return message "Y18" or error
  status "A18" are sent
- clear state with "@18"

4.2 Serial communicaton 
========================

Commands are sent via serial port, 9600 8N1, no handshake.

All communication messages are encapsulated as

0xFF0x02<message>0x03<checksum>0x0D.

The checksum is built as the bitwise OR of the characters before the
checksum character like e.g. in Python:

s="\xFF\x02A18PA 29 29 29\x03"
chk=ord(s[1]);

for c in s[2:len(s)]:
    chk=chk ^ ord(c)

print "%s%c\r" % (s,chk)

4.3 Addresses 
==============

A command always starts with "A<addr>", where <addr> can be one of the
following:

- 18 for arm 1 (left)
- 11 for syringe 1 (left)
- 12 for syringe 2 (right)
- 28 for arm 2 (right)

4.4 Commands 
=============

fter the "A<addr>", the following commands can be appended

4.4.1 Arms 
-----------

- PI: initialize arm, needs to be done before first use
- SP0: set position recovery
- SA x y z s: set position range of arm
- PA x y z: arm goto position

4.4.2 Syringe pumps 
--------------------

- Sx Ay d R: set syringe speed x (1-20), position y (0-2000),
  direction of valve d (I for input, O for output) 

4.5 Return codes 
=================

The return code is of the following form:

X<address>

where X is one of:

- @: command accepted
- A: error, for example when position is out of range
- Q: command execution in progress
- Y: command finished.

(There may be more)

