#!/bin/env python

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
