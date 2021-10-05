#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Mechanical Engineering Calculators, Chuck McKyes

    Copyright (C) 2021 Chuck McKyes

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
import pkg_resources
import platform

from mechcalc import Torque
from mechcalc import Power
from mechcalc import PumpPower
from mechcalc import PumpHead
from mechcalc import ThreePhasePower
from mechcalc import VapourPressure


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(*args, **kwds)
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)

        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.panel_1 = Torque(self.notebook_1_pane_1, wx.ID_ANY, style=wx.BORDER_RAISED)
        self.panel_2 = Power(self.notebook_1_pane_1, wx.ID_ANY, style=wx.BORDER_RAISED)

        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.panel_3 = PumpPower(self.notebook_1_pane_2, wx.ID_ANY, style=wx.BORDER_RAISED)
        self.panel_4 = PumpHead(self.notebook_1_pane_2, wx.ID_ANY, style=wx.BORDER_RAISED)

        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.panel_5 = ThreePhasePower(self.notebook_1_pane_3, wx.ID_ANY, style=wx.BORDER_RAISED)

        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.panel_6 = VapourPressure(self.notebook_1_pane_4, wx.ID_ANY, style=wx.BORDER_RAISED)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("Mechanical Engineering Calculator")
        data_path = pkg_resources.resource_filename('mechcalc', 'data/')
        # data_path = "data/"
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap(data_path + "my_icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.notebook_1_pane_1.SetForegroundColour(wx.Colour(255, 255, 255))
        self.notebook_1_pane_2.SetForegroundColour(wx.Colour(255, 255, 255))
        self.notebook_1_pane_3.SetForegroundColour(wx.Colour(255, 255, 255))
        self.notebook_1_pane_4.SetForegroundColour(wx.Colour(255, 255, 255))

        # Set a darker background for Linux
        if platform.system() == "Linux":
            self.notebook_1_pane_1.SetBackgroundColour(wx.Colour(40, 40, 40))
            self.notebook_1_pane_2.SetBackgroundColour(wx.Colour(40, 40, 40))
            self.notebook_1_pane_3.SetBackgroundColour(wx.Colour(40, 40, 40))
            self.notebook_1_pane_4.SetBackgroundColour(wx.Colour(40, 40, 40))
        else:
            self.notebook_1_pane_1.SetBackgroundColour(wx.Colour(100, 100, 100))
            self.notebook_1_pane_2.SetBackgroundColour(wx.Colour(100, 100, 100))
            self.notebook_1_pane_3.SetBackgroundColour(wx.Colour(100, 100, 100))
            self.notebook_1_pane_4.SetBackgroundColour(wx.Colour(100, 100, 100))

    def __do_layout(self):
        # main window sizer
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        # notebook_1_pane_1 sizer
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        # notebook_1_pane_2 sizer
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        # notebook_1_pane_3 sizer
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        # notebook_1_pane_4 sizer
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_2.Add(self.panel_1, 1, wx.EXPAND | wx.ALL, 4)
        sizer_2.Add(self.panel_2, 1, wx.EXPAND | wx.ALL, 4)
        self.notebook_1_pane_1.SetSizer(sizer_2)

        sizer_3.Add(self.panel_3, 1, wx.EXPAND | wx.ALL, 4)
        sizer_3.Add(self.panel_4, 1, wx.EXPAND | wx.ALL, 4)
        self.notebook_1_pane_2.SetSizer(sizer_3)

        sizer_4.Add(self.panel_5, 1, wx.EXPAND | wx.ALL, 4)
        self.notebook_1_pane_3.SetSizer(sizer_4)

        sizer_5.Add(self.panel_6, 1, wx.EXPAND | wx.ALL, 4)
        self.notebook_1_pane_4.SetSizer(sizer_5)

        self.notebook_1.AddPage(self.notebook_1_pane_1, "Torque")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Pump Power")
        self.notebook_1.AddPage(self.notebook_1_pane_3, "Electrical")
        self.notebook_1.AddPage(self.notebook_1_pane_4, "Vapour Pressure")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.notebook_1.SetSelection(0)
        self.SetMinSize((1000, 500))
        self.Layout()

# end of class MyFrame
