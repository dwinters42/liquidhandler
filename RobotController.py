#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon May  3 20:48:02 2010

# Copyright (c) 2010 Daniel Gruber <daniel@tydirium.org>
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
import robot

robot.debug=True
robot.demomode=False

# begin wxGlade: extracode
# end wxGlade

class ManualModeFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ManualModeFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.sizerarmcontrol_staticbox = wx.StaticBox(self, -1, "Arm control")
        self.statusbar = self.CreateStatusBar(1, 0)
        self.labelPos = wx.StaticText(self, -1, "Pos: [0000, 0000, 0000]")
        self.buttonYplus = wx.Button(self, -1, "Y+")
        self.buttonUp = wx.Button(self, -1, "Up")
        self.buttonXminus = wx.Button(self, -1, "X-")
        self.buttonXplus = wx.Button(self, -1, "X+")
        self.buttonYminus = wx.Button(self, -1, "Y-")
        self.buttonDown = wx.Button(self, -1, "Down")
        self.label_2 = wx.StaticText(self, -1, "Selected Arm:")
        self.spinCtrlArmSelected = wx.SpinCtrl(self, -1, "1", min=1, max=2)
        self.label_2_copy = wx.StaticText(self, -1, "Stepsize for buttons:")
        self.comboBoxStepSize = wx.ComboBox(self, -1, choices=["1", "10", "100"], style=wx.CB_DROPDOWN|wx.CB_SIMPLE|wx.CB_READONLY)
        self.listBoxPos = wx.ListBox(self, -1, choices=[], style=wx.LB_SINGLE)
        self.buttonGotoPos = wx.Button(self, -1, "Goto")
        self.buttonSavePos = wx.Button(self, -1, "Save")
        self.buttonRemove = wx.Button(self, -1, "Remove")
        self.buttonLoadLoc = wx.Button(self, -1, "Load Locations")
        self.buttonSaveLoc = wx.Button(self, -1, "Save Locations")

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
        # end wxGlade

        # disable windows while robot is being initialised
        wx.Yield()
        disabler=wx.WindowDisabler()
        wx.Yield()
        busy=wx.BusyInfo("Initialising robot, please wait ...")
        wx.Yield()
        self.r=robot.Robot("/dev/ttyUSB0")
        self.statusbar.SetStatusText("Ready")

    def __set_properties(self):
        # begin wxGlade: ManualModeFrame.__set_properties
        self.SetTitle("Manual Control")
        self.statusbar.SetStatusWidths([-1])
        # statusbar fields
        statusbar_fields = ["manualframe_statusbar"]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        self.labelPos.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.comboBoxStepSize.SetSelection(2)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ManualModeFrame.__do_layout
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
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
        sizer_4.Add(sizerarmcontrol, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer_4)
        sizer_4.Fit(self)
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

        self.r.Move(pos,arm)
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

        self.r.AddPosition(label,self.r.ShowPosition(arm))
        self._updatePosList()

    def onButtonRemove(self, event): # wxGlade: ManualModeFrame.<event_handler>
        pos=self.r.locations.keys()[self.listBoxPos.GetSelections()[0]]
        self.r.locations.pop(pos)
        self._updatePosList()

    def _updatePosList(self):
        self.listBoxPos.Set(self.r.locations.keys())

    def onButtonLoadLoc(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self.r.LoadLocations()
        self._updatePosList()

    def onButtonSaveLoc(self, event): # wxGlade: ManualModeFrame.<event_handler>
        self.r.SaveLocations()
        self._updatePosList()

# end of class ManualModeFrame


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_OPEN, "", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_SAVE, "", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_SAVEAS, "", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.NewId(), "Check\tCTRL+C", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.NewId(), "Run\tCTRL+R", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_EXIT, "", "", wx.ITEM_NORMAL)
        self.frame_1_menubar.Append(wxglade_tmp_menu, "File")
        self.SetMenuBar(self.frame_1_menubar)
        # Menu Bar end
        self.frame_1_statusbar = self.CreateStatusBar(1, 0)
        
        # Tool Bar
        self.frame_1_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.frame_1_toolbar)
        self.frame_1_toolbar.AddLabelTool(wx.ID_OPEN, "", wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        # Tool Bar end
        self.label_1 = wx.StaticText(self, -1, "Positions:")
        self.listboxPositions = wx.ListBox(self, -1, choices=[], style=wx.LB_SINGLE|wx.LB_SORT)
        self.buttonEditPositions = wx.Button(self, -1, "Edit Positions")
        self.textctrlRunlist = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_LINEWRAP)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.openRunlist, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.saveRunlist, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.saveasRunlist, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.checkRunlist, id=-1)
        self.Bind(wx.EVT_MENU, self.quitApp, id=wx.ID_EXIT)
        self.Bind(wx.EVT_TOOL, self.openRunlist, id=wx.ID_OPEN)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.insertPosition, self.listboxPositions)
        self.Bind(wx.EVT_BUTTON, self.edtPositions, self.buttonEditPositions)
        # end wxGlade
        
        self.filename="runlist.py"

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("RobotController")
        self.frame_1_statusbar.SetStatusWidths([-1])
        # statusbar fields
        frame_1_statusbar_fields = ["frame_1_statusbar"]
        for i in range(len(frame_1_statusbar_fields)):
            self.frame_1_statusbar.SetStatusText(frame_1_statusbar_fields[i], i)
        self.frame_1_toolbar.Realize()
        self.textctrlRunlist.SetMinSize((400,400))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.label_1, 0, wx.ALL|wx.EXPAND, 5)
        sizer_3.Add(self.listboxPositions, 1, wx.ALL|wx.EXPAND, 5)
        sizer_3.Add(self.buttonEditPositions, 0, wx.ALL, 5)
        sizer_3.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.ALL|wx.EXPAND, 5)
        sizer_2.Add(self.textctrlRunlist, 2, wx.ALL|wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def edtPositions(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `edtPositions' not implemented!"
        event.Skip()

    def openRunlist(self, event): # wxGlade: MainFrame.<event_handler>

        print "Event handler `openRunlist' not implemented!"
        event.Skip()

    def saveRunlist(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `saveRunlist' not implemented"
        event.Skip()

    def saveasRunlist(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `saveasRunlist' not implemented"
        event.Skip()

    def checkRunlist(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `checkRunlist' not implemented"
        event.Skip()

    def insertPosition(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `insertPosition' not implemented"
        event.Skip()

    def quitApp(self, event): # wxGlade: MainFrame.<event_handler>
        if self.textctrlRunlist.IsModified():
            if wx.MessageBox("Save Runlist?", "Confirm", wx.YES_NO) == wx.YES:
                self.textctrlRunlist.SaveFile(self.filename)

        self.Destroy()

# end of class MainFrame


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
