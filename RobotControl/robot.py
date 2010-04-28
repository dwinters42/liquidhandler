#/usr/bin/python

debug=False

import serial
import time

### class Robot ###

class Robot():
    def __init__(self,port="/dev/ttyUSB0"):
        # constants for arms
        self.armaddr=[18,28]
        self.armlimits=[[2500, 1000, 1200, 10],[1600, 1000, 1200, 10]]

        # constants for pumps
        self.pumpaddr=[11]
        self.syringecontents=[0]

        # locations to Goto to
        self.locations={}

        # init serial port
        self.s=serial.Serial(port,rtscts=0,xonxoff=0,timeout=0)

        # init arms
        for i in range(len(self.armaddr)):
            self._sendcommand(self.armaddr[i],"PI")
            self._sendcommand(self.armaddr[i],"SP0")
            s="SA %i %i %i %i" % (self.armlimits[i][0],self.armlimits[i][2],\
                                  self.armlimits[i][2],self.armlimits[i][3])
            self._sendcommand(self.armaddr[i],s)

        # init pumps
        for i in range(len(self.pumpaddr)):
            self._sendcommand(self.pumpaddr[i],"Z1 0 R")

    ## Arm commands ##

    def AddPosition(self,name,coordinates):
        self.locations[name]=coordinates

    def Goto(self,armnum,location):
        pos=self.locations[location]
        self.Move(armnum,pos)

    def Move(self,armnum,pos=[0,0,0]):
        s="PA %i %i %i" % (pos[0],pos[1],pos[2])
        return self._sendcommand(self.armaddr[armnum-1],s)
    
    ## Pump commands ##

    def Dispense(self,pump,units):
        '''Dispense units (0-2000) of liquid from syringe'''
        if units > self.syringecontents[pump-1]:
            raise ValueError, "Not enough liquid in syringe!"

        self.Pump(pump,3,self.syringecontents[pump-1],'out')
        self.Pump(pump,3,self.syringecontents[pump-1]-units,'out')
        self.syringecontents[pump-1]=self.syringecontents[pump-1]-units

    def Draw(self,pump,units,source='bottle'):
        if source == 'bottle':
            direction='in'
        elif source == 'sample':
            direction='out'
        else:
            raise ValueError,"Source for Dispense must be either bottle or sample!"
    
        if self.syringecontents[pump-1]+units>2000:
            raise ValueError,"Syringe can only contain up to 2000 units!"

        self.Pump(pump,3,self.syringecontents[pump-1],direction)
        self.Pump(pump,3,self.syringecontents[pump-1]+units,direction)
        self.syringecontents[pump-1]=self.syringecontents[pump-1]+units

    def Pump(self,pump,speed,position,direction):
        if direction == "in":
            dircode='I'
        elif direction == 'out':
            dircode='O'
        else:
            raise ValueError,"Pump direction must be 'in' or 'out'!"

        s="S%i A%i %c R" % (speed,position,dircode)
        return self._sendcommand(self.pumpaddr[pump-1],s)

    ## internal stuff, not for external use ##

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
