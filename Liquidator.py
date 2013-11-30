#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010,2011 Daniel Winters <daniel@tydirium.org>
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

import wx
import liquidhandler

liquidhandler.debug=False
liquidhandler.demomode=False

# begin wxGlade: extracode
# end wxGlade

class ManualModeFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ManualModeFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.sizersyringecontrol_staticbox = wx.StaticBox(self.panel_1, -1, "Syringe")
        self.sizerarmcontrol_staticbox = wx.StaticBox(self.panel_1, -1, "Arm control")
        self.statusbar = self.CreateStatusBar(1, 0)
        self.labelPos = wx.StaticText(self.panel_1, -1, "Pos: [0000, 0000, 0000]")
        self.buttonYplus = wx.Button(self.panel_1, -1, "Y+")
        self.buttonUp = wx.Button(self.panel_1, -1, "Up")
        self.buttonXminus = wx.Button(self.panel_1, -1, "X-")
        self.buttonXplus = wx.Button(self.panel_1, -1, "X+")
        self.buttonYminus = wx.Button(self.panel_1, -1, "Y-")
        self.buttonDown = wx.Button(self.panel_1, -1, "Down")
        self.label_2 = wx.StaticText(self.panel_1, -1, "Selected Arm:")
        self.spinCtrlArmSelected = wx.SpinCtrl(self.panel_1, -1, "1", min=1, max=2)
        self.label_2_copy = wx.StaticText(self.panel_1, -1, "Stepsize for buttons:")
        self.comboBoxStepSize = wx.ComboBox(self.panel_1, -1, choices=["1", "10", "100"], style=wx.CB_DROPDOWN|wx.CB_SIMPLE|wx.CB_READONLY)
        self.listBoxPos = wx.ListBox(self.panel_1, -1, choices=[], style=wx.LB_SINGLE)
        self.buttonGotoPos = wx.Button(self.panel_1, -1, "Goto")
        self.buttonSavePos = wx.Button(self.panel_1, -1, "Add Location")
        self.buttonRemove = wx.Button(self.panel_1, -1, "Remove Location")
        self.buttonLoadLoc = wx.Button(self.panel_1, -1, "Load Locations")
        self.buttonSaveLoc = wx.Button(self.panel_1, -1, "Save Locations")
        self.label_3 = wx.StaticText(self.panel_1, -1, "Syringe content (units):")
        self.textCtrlSyringeContent = wx.TextCtrl(self.panel_1, -1, "0", style=wx.TE_READONLY)
        self.label_3_copy = wx.StaticText(self.panel_1, -1, "Syringe speed (0-20):")
        self.textCtrlSyringeSpeed = wx.TextCtrl(self.panel_1, -1, "10")
        self.label_3_copy_1 = wx.StaticText(self.panel_1, -1, "Amount to draw/dispense (units):")
        self.textCtrlSyringeAmount = wx.TextCtrl(self.panel_1, -1, "500")
        self.buttonDrawBottle = wx.Button(self.panel_1, -1, "Draw from bottle")
        self.buttonDrawSample = wx.Button(self.panel_1, -1, "Draw from sample")
        self.buttonDispense = wx.Button(self.panel_1, -1, "Dispense")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onButtonYplus, self.buttonYplus)
        self.Bind(wx.EVT_BUTTON, self.onButtonUp, self.buttonUp)
        self.Bind(wx.EVT_BUTTON, self.onButtonXminus, self.buttonXminus)
        self.Bind(wx.EVT_BUTTON, self.onButtonXplus, self.buttonXplus)
        self.Bind(wx.EVT_BUTTON, self.onButtonYminus, self.buttonYminus)
        self.Bind(wx.EVT_BUTTON, self.onButtonDown, self.buttonDown)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.onListBoxPosDoubleClick, self.listBoxPos)
        self.Bind(wx.EVT_BUTTON, self.onButtonGoto, self.buttonGotoPos)
        self.Bind(wx.EVT_BUTTON, self.onButtonSave, self.buttonSavePos)
        self.Bind(wx.EVT_BUTTON, self.onButtonRemove, self.buttonRemove)
        self.Bind(wx.EVT_BUTTON, self.onButtonLoadLoc, self.buttonLoadLoc)
        self.Bind(wx.EVT_BUTTON, self.onButtonSaveLoc, self.buttonSaveLoc)
        self.Bind(wx.EVT_BUTTON, self.onButtonDrawBottle, self.buttonDrawBottle)
        self.Bind(wx.EVT_BUTTON, self.onButtonDrawSample, self.buttonDrawSample)
        self.Bind(wx.EVT_BUTTON, self.onButtonDispense, self.buttonDispense)
        # end wxGlade

        self.syringecontent=0

        # read the serial port and locations file from the
        # registry/config file
        self.conf=wx.Config("Liquidhandler")

        if self.conf.HasEntry("ComPort"):
            port=self.conf.Read("ComPort")
        else:
            port=wx.GetTextFromUser("Please enter serial port to use:")

        if self.conf.HasEntry("LocationsFile"):
            self.dfile=self.conf.Read("LocationsFile")
        else:
            self.dfile=None

        self.Show()
        # disable windows while robot is being initialised
        wx.Yield()
        disabler=wx.WindowDisabler()
        wx.Yield()
        busy=wx.BusyInfo("Initialising robot, please wait ...")
        wx.Yield()
        try:
            self.r=liquidhandler.Robot(port, self.dfile)
        except:
            del disabler
            wx.LogError("Could not connect to robot! Is it switched on?")
            return

        self._updatePosList()
        self.statusbar.SetStatusText("Ready")
        self.conf.Write("ComPort", port)

    def __set_properties(self):
        # begin wxGlade: ManualModeFrame.__set_properties
        self.SetTitle("Liquidator Robot Control")
        self.statusbar.SetStatusWidths([-1])
        # statusbar fields
        statusbar_fields = ["Connecting to robot ..."]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        self.labelPos.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.comboBoxStepSize.SetSelection(2)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ManualModeFrame.__do_layout
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer2 = wx.BoxSizer(wx.VERTICAL)
        sizersyringecontrol = wx.StaticBoxSizer(self.sizersyringecontrol_staticbox, wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_4 = wx.GridSizer(3, 2, 0, 0)
        sizerarmcontrol = wx.StaticBoxSizer(self.sizerarmcontrol_staticbox, wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.GridSizer(2, 2, 5, 5)
        grid_sizer_1 = wx.GridSizer(3, 4, 5, 5)
        sizerarmcontrol.Add(self.labelPos, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add(self.buttonYplus, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add(self.buttonUp, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(self.buttonXminus, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add(self.buttonXplus, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add(self.buttonYminus, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add((20, 20), 0, 0, 0)
        grid_sizer_1.Add(self.buttonDown, 1, wx.ALL|wx.EXPAND, 5)
        sizerarmcontrol.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_2.Add(self.spinCtrlArmSelected, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_2.Add(self.label_2_copy, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_2.Add(self.comboBoxStepSize, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizerarmcontrol.Add(grid_sizer_2, 0, wx.ALL|wx.EXPAND, 5)
        sizerarmcontrol.Add(self.listBoxPos, 1, wx.ALL|wx.EXPAND, 5)
        sizer_6.Add(self.buttonGotoPos, 1, wx.ALL|wx.EXPAND, 5)
        sizer_6.Add(self.buttonSavePos, 1, wx.ALL|wx.EXPAND, 5)
        sizer_6.Add(self.buttonRemove, 1, wx.ALL|wx.EXPAND, 5)
        sizerarmcontrol.Add(sizer_6, 0, wx.EXPAND, 5)
        sizer_5.Add(self.buttonLoadLoc, 1, wx.ALL|wx.EXPAND, 5)
        sizer_5.Add((20, 20), 1, wx.ALL|wx.EXPAND, 5)
        sizer_5.Add(self.buttonSaveLoc, 1, wx.ALL|wx.EXPAND, 5)
        sizerarmcontrol.Add(sizer_5, 0, wx.ALL|wx.EXPAND, 5)
        mainsizer2.Add(sizerarmcontrol, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_4.Add(self.label_3, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_4.Add(self.textCtrlSyringeContent, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_4.Add(self.label_3_copy, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_4.Add(self.textCtrlSyringeSpeed, 0, wx.ALL|wx.EXPAND, 5)
        grid_sizer_4.Add(self.label_3_copy_1, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_4.Add(self.textCtrlSyringeAmount, 0, wx.ALL|wx.EXPAND, 5)
        sizersyringecontrol.Add(grid_sizer_4, 0, wx.EXPAND, 0)
        sizer_8.Add(self.buttonDrawBottle, 1, wx.ALL|wx.EXPAND, 5)
        sizer_8.Add(self.buttonDrawSample, 1, wx.ALL|wx.EXPAND, 5)
        sizer_8.Add(self.buttonDispense, 1, wx.ALL|wx.EXPAND, 5)
        sizersyringecontrol.Add(sizer_8, 0, wx.ALL|wx.EXPAND, 5)
        mainsizer2.Add(sizersyringecontrol, 0, wx.ALL|wx.EXPAND, 5)
        self.panel_1.SetSizer(mainsizer2)
        mainsizer.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Layout()
        # end wxGlade

    def onButtonYplus(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self._movearm(1,"pos")

    def onButtonXminus(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self._movearm(0,"neg")

    def onButtonXplus(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self._movearm(0,"pos")

    def onButtonYminus(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self._movearm(1,"neg")

    def _movearm(self,axis,direction="pos"):
        arm=int(self.spinCtrlArmSelected.GetValue())
        pos=self.r.ShowPosition(arm)[:] # [:] to actually copy the
                                        # values, not the reference!
        stepsize=int(self.comboBoxStepSize.GetValue())

        if direction == "pos":
            pos[axis]=pos[axis]+stepsize
        elif direction == "neg" and pos[axis] >= stepsize:
            pos[axis]=pos[axis]-stepsize

        try:
            self.r.MoveAxis(axis,pos[axis],arm)
        except Exception, err:
            wx.LogError("Error: %s" % err)
        else:
            self.labelPos.SetLabel("Pos: [%04i, %04i, %04i]" % \
                                       (pos[0],pos[1],pos[2]))

    def onButtonUp(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self._movearm(2,"neg")

    def onButtonDown(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self._movearm(2,"pos")

    def onListBoxPosDoubleClick(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self.onButtonGoto(event)

    def onButtonGoto(self, event): # wxGlade: ManualModeFrame.<event_handler>
        pos=self.r.locations.keys()[self.listBoxPos.GetSelections()[0]]
        arm=int(self.spinCtrlArmSelected.GetValue())

        self.r.Goto(pos,arm)
        coord=self.r.ShowPosition(arm)
        self.labelPos.SetLabel("Pos: [%04i, %04i, %04i]" % \
                                   (coord[0],coord[1],coord[2]))

    def onButtonSave(self, event): # wxGlade: ManualModeFrame.<event_handler>
        arm=int(self.spinCtrlArmSelected.GetValue())
        label=wx.GetTextFromUser("Name of location:", "New location").\
            encode('ascii') # to have a ascii-only yaml file

        self.r.AddPosition(label,self.r.ShowPosition(arm)[:])
        self._updatePosList()

    def onButtonRemove(self, event): # wxGlade: ManualModeFrame.<event_handler>
        pos=self.r.locations.keys()[self.listBoxPos.GetSelections()[0]]
        self.r.locations.pop(pos)
        self._updatePosList()

    def _updatePosList(self):
        list=[]
        for item in self.r.locations.keys():
            list.append("%s %s" % (item,str(self.r.locations[item])))
        self.listBoxPos.Set(list)

    def onButtonLoadLoc(self, event): # wxGlade: ManualModeFrame.<event_handler>
        dlg=wx.FileDialog(self, style = wx.FD_OPEN|wx.FD_FILE_MUST_EXIST\
                              |wx.FD_CHANGE_DIR, wildcard="*.yml")
        if dlg.ShowModal() == wx.ID_OK:
            self.dfile=dlg.GetPath()
            del(dlg)
            self.r.LoadLocations(self.dfile)
            self.conf.Write("LocationsFile", self.dfile)
            self._updatePosList()

    def onButtonSaveLoc(self, event): # wxGlade: ManualModeFrame.<event_handler>
        dlg=wx.FileDialog(self, style = wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT\
                              |wx.FD_CHANGE_DIR, defaultFile = \
                              self.dfile, wildcard="*.yml")
        if dlg.ShowModal() == wx.ID_OK:
            self.dfile=dlg.GetPath()
            del(dlg)
            self.r.SaveLocations(self.dfile)
            self.conf.Write("LocationsFile", self.dfile)
            self._updatePosList()

    def onButtonDrawBottle(self, event): # wxGlade: ManualModeFrame.<event_handler>
        units=int(self.textCtrlSyringeAmount.GetValue())
        speed=int(self.textCtrlSyringeSpeed.GetValue())

        try:
            self.r.Draw(units,'bottle',speed)
        except Exception, err:
            wx.LogError("Error: %s" % err)
        else:
            self.syringecontent=self.syringecontent+units
            self._updateSyringeContent()

    def onButtonDrawSample(self, event): # wxGlade: ManualModeFrame.<event_handler>
        units=int(self.textCtrlSyringeAmount.GetValue())
        speed=int(self.textCtrlSyringeSpeed.GetValue())
        try:
            self.r.Draw(units,'sample',speed)
        except Exception, err:
            wx.LogError("Error: %s" % err)
        else:
            self.syringecontent=self.syringecontent+units
            self._updateSyringeContent()

    def onButtonDispense(self, event): # wxGlade: ManualModeFrame.<event_handler>
        units=int(self.textCtrlSyringeAmount.GetValue())
        speed=int(self.textCtrlSyringeSpeed.GetValue())
        try:
            self.r.Dispense(units,speed)
        except Exception, err:
            wx.LogError("Error: %s" % err)
        else:
            self.syringecontent=self.syringecontent-units
            self._updateSyringeContent()

    def _updateSyringeContent(self):
        self.textCtrlSyringeContent.SetValue(str(self.syringecontent))

# end of class ManualModeFrame

class RobotController(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = ManualModeFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class RobotController

if __name__ == "__main__":
    app = RobotController(0)
    app.MainLoop()
