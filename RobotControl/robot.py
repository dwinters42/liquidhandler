#/usr/bin/python

debug=False

import serial
import time

### class Robot ###

class Robot():
    def __init__(self,port="/dev/ttyUSB0"):
        self.armaddr=[18,28]
        self.armlimits=[[2500, 1000, 1200, 10],[1600, 1000, 1200, 10]]
        self.syringeaddr=[11]
        self.locations={}

        self.s=serial.Serial(port,rtscts=0,xonxoff=0,timeout=0)

        # init arms
        for i in range(len(self.armaddr)):
            self._sendcommand(self.armaddr[i],"PI")
            self._sendcommand(self.armaddr[i],"SP0")
            s="SA %i %i %i %i" % (self.armlimits[i][0],self.armlimits[i][2],\
                                  self.armlimits[i][2],self.armlimits[i][3])
            self._sendcommand(self.armaddr[i],s)

        # init syringes
        for i in range(len(self.syringeaddr)):
            self._sendcommand(self.syringeaddr[i],"Z1 0 R")

    def AddPosition(self,name,coordinates):
        self.locations[name]=coordinates

    def Goto(self,armnum,location):
        pos=self.locations[location]
        self.Move(armnum,pos)

    def Move(self,armnum,pos=[0,0,0]):
        s="PA %i %i %i" % (pos[0],pos[1],pos[2])
        return self._sendcommand(self.armaddr[armnum-1],s)
    
    def Syringe(self,syringe,speed,position,direction):
        if direction == "in":
            dircode='I'
        elif direction == 'out':
            dircode='O'
        else:
            raise ValueError,"Syringe direction must be 'in' or 'out'!"

        s="S%i A%i %c R" % (speed,position,dircode)
        return self._sendcommand(self.syringeaddr[syringe-1],s)

    def _makecommandstring(self,command):
        s="\xFF\x02%s\x03" % (command)
        chk=ord(s[1]);

        for c in s[2:len(s)]:
            chk=chk ^ ord(c)

        return "%s%c\r" % (s,chk)

    def _sendcommand(self, address, command):
        # send command
        cmd="A%i%s" % (address,command)
        if debug:
            print "-> %s" % cmd
        c=self._makecommandstring(cmd)
        self.s.write(c)
        time.sleep(0.1)
    
        # wait for command to complete
        go=True
        while go is True:
            answer=self.s.readline(eol='\r')
            if answer != "":
                # we got something
                words=answer.split('\x02')
                for word in words[1:]:
                    if len(word) < 3:
                        if debug:
                            print "word too short"
                        res = -2
                    else:
                        # throw away checksum and separator
                        word=word[0:-2]
                        if debug:
                            print "<- %s" % word
                        if word.count('Q')>0:
                            # command finished
                            go = False
                            if debug:
                                print("<- finished")
                            res = 0
                        elif word.count('A')>0:
                            go = False
                            if debug:
                                print("<- error!")
                            res = -1
            time.sleep(0.1)

        # clear flag
        cmd="@%s" % address
        if debug:
            print "-> %s" % cmd
        c=self._makecommandstring(cmd)
        self.s.write(c)
        if res != 0:
            raise IOError,"Robot returns error!"

### end of class Robot ###
