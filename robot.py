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

debug=False # if True, log the communication with the robot to the
            # command line
demomode=False # if True, don't talk to the robot at all, suitable for
               # testing

import serial
import time
import yaml

### class Robot ###

class Robot():
    def __init__(self,port='/dev/ttyUSB0',setupfile=None):
        # constants for arms
        self.armaddr=[18,28]
        self.armlimits=[[2500, 1000, 1200, 10],[1600, 1000, 1200, 10]]

        # constants for pumps
        self.pumpaddr=[11]
        self.syringecontents=[0]

        # locations to Goto to
        self.locations={}

        # init serial port
        if not demomode:
            self.s=serial.Serial(port,rtscts=0,xonxoff=0,timeout=0)

        # init arms
        for i in range(len(self.armaddr)):
            self._sendcommand(self.armaddr[i],"PI")
            self._sendcommand(self.armaddr[i],"SP0")
            s="SA %i %i %i %i" % (self.armlimits[i][0],self.armlimits[i][2],\
                                  self.armlimits[i][2],self.armlimits[i][3])
            self._sendcommand(self.armaddr[i],s)
        
        self.curpos=[[0,0,0],[0,0,0]]

        # init pumps
        for i in range(len(self.pumpaddr)):
            self._sendcommand(self.pumpaddr[i],"Z1 0 R")

        # finally, load saved locations
        if setupfile != None:
            self.LoadLocations(setupfile)

    ## Save/Load locations ##

    def SaveLocations(self, filename='robot-locations.yml'):
        f=file(filename,'w')
        yaml.dump(self.locations,f)

    def LoadLocations(self, filename='robot-locations.yml'):
        f=file(filename,'r')
        self.locations=yaml.load(f)

    ## Arm commands ##

    def AddPosition(self,name,coordinates):
        '''Memorize position with coordinates [x,y,z] as 'name' '''
        self.locations[name]=coordinates

    def Goto(self,location,armnum=1):
        '''Move arm 'armnum' to memorized position 'location' '''
        if not self.locations.has_key(location):
            raise ValueError,"No such location!"

        pos=self.locations[location]
        self.Move(pos,armnum)

    def Move(self,pos=[0,0,0],armnum=1):
        '''Move arm 'armnum' to coordinates 'pos' ([x,y,z])'''
        s="PA %i %i %i" % (int(pos[0]),int(pos[1]),int(pos[2]))
        self._sendcommand(self.armaddr[armnum-1],s)
        self.curpos[armnum-1]=pos

    def MoveAxis(self,axis=0,pos=10,armnum=1):
        '''Move axis of arm 'armnum' to coordinate pos'''
        axes=("X","Y","Z")
        s="%sA %i" % (axes[axis],pos)
        self._sendcommand(self.armaddr[armnum-1],s)
        self.curpos[armnum-1][axis]=pos

    def ShowPosition(self,armnum=1):
        return self.curpos[armnum-1]
    
    ## Pump commands ##

    def Dispense(self,units,speed=3,pump=1):
        '''Dispense units (0-2000) of liquid from syringe'''
        if int(units) > self.syringecontents[pump-1]:
            raise ValueError, "Not enough liquid in syringe!"

        self.Pump(pump,3,self.syringecontents[pump-1],'out')
        self.Pump(pump,3,self.syringecontents[pump-1]-int(units),'out')
        self.syringecontents[pump-1]=self.syringecontents[pump-1]-int(units)

    def Draw(self,units,source='bottle',speed=3,pump=1):
        '''Draw units (0-2000) from either bottle or sample'''
        if source == 'bottle':
            direction='in'
        elif source == 'sample':
            direction='out'
        else:
            raise ValueError,"Source must be either 'bottle' or 'sample'!"
    
        if self.syringecontents[pump-1]+units>2000:
            raise ValueError,"Syringe can only contain up to 2000 units!"

        self.Pump(pump,3,self.syringecontents[pump-1],direction)
        self.Pump(pump,3,self.syringecontents[pump-1]+int(units),direction)
        self.syringecontents[pump-1]=self.syringecontents[pump-1]+int(units)

    def Pump(self,pump,speed,position,direction):
        if int(speed) < 0 or int(speed)>20:
            raise ValueError,"Pump speed must be between 0 and 20!"

        if int(position) < 0 or int(position)>2000:
            raise ValueError,"Pump position must be between 0 and 2000!"

        if direction == "in":
            dircode='I'
        elif direction == 'out':
            dircode='O'
        else:
            raise ValueError,"Pump direction must be 'in' or 'out'!"

        s="S%i A%i %c R" % (int(speed),int(position),dircode)
        return self._sendcommand(self.pumpaddr[pump-1],s)

    ## internal stuff, not for external use ##

    def _makecommandstring(self,command):
        s="\xFF\x02%s\x03" % (command)
        chk=ord(s[1]);

        for c in s[2:len(s)]:
            chk=chk ^ ord(c)

        return "%s%c\r" % (s,chk)

    def _sendcommand(self, address, command):
        if demomode:
            return

        # send command
        cmd="A%i%s" % (address,command)
        if debug:
            print "-> %s" % cmd
        c=self._makecommandstring(cmd)
        self.s.write(c)
        time.sleep(0.3)
    
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
                        if word.count('Y')>0:
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
