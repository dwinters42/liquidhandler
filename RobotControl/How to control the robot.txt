* High-level command protocol

The protocol is the following:

- Send a command, e.g. "A18PA 100 100 100" (address 18 = arm1, PA: move to
  position (100,100,100))
- Read "command accepted" return message "@18" from robot
- Read optional information messages like "Q18"
- Contiue reading until "command finished" return message "Y18" or error
  status "A18" are sent
- clear state with "@18"

* Serial communicaton

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

* Addresses

A command always starts with "A<addr>", where <addr> can be one of the
following:

- 18 for arm 1 (left)
- 11 for syringe 1 (left)
- 12 for syringe 2 (right)
- 28 for arm 2 (right)

* Commands

After the "A<addr>", the following commands can be appended

** Arms

- PI: initialize arm, needs to be done before first use
- SP0: set position recovery
- SA x y z s: set position range of arm
- PA x y z: arm goto position

** Syringe pumps

- Sx Ay d R: set syringe speed x (1-20), position y (0-2000),
  direction of valve d (I for input, O for output) 

* Return codes

The return code is of the following form:

X<address>

where X is one of:

- @: command accepted
- A: error, for example when position is out of range
- Q: command execution in progress
- Y: command finished.

(There may be more)




