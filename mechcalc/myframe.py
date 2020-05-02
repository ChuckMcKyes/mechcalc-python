"""
	mechcalc, mechanical engineering tools.
    Copyright (C) 2020, Chuck McKyes

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import wx
import wx.adv
from mechcalc import Torque
from mechcalc import Power
from mechcalc import PumpPower


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(*args, **kwds)
        self.SetSize((800, 400))
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.panel_1 = Torque(self.notebook_1_pane_1, wx.ID_ANY, style=wx.BORDER_NONE)
        self.panel_2 = Power(self.notebook_1_pane_1, wx.ID_ANY, style=wx.BORDER_NONE)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.panel_3 = PumpPower(self.notebook_1_pane_2, wx.ID_ANY, style=wx.BORDER_NONE)
        self.panel_4 = wx.Panel(self.notebook_1_pane_2, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Mechanical Engineering Calculator")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("/home/user/PycharmProjects/MechCalc/gnome-util.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.panel_1, 1, wx.EXPAND | wx.ALL, 4)
        sizer_2.Add(self.panel_2, 1, wx.EXPAND | wx.ALL, 4)
        self.notebook_1_pane_1.SetSizer(sizer_2)
        sizer_3.Add(self.panel_3, 1, wx.EXPAND | wx.ALL, 4)
        #sizer_3.Add(self.panel_4, 1, wx.EXPAND, 0)
        self.notebook_1_pane_2.SetSizer(sizer_3)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Torque")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Pump Power")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.SetMinSize((800, 400))
        self.Layout()
        # end wxGlade

# end of class MyFrame
