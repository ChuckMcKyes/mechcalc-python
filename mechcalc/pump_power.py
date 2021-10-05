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
import json


class PumpPower(wx.Panel):
    def __init__(self, notebook, wx_id, style):
        super().__init__(notebook, wx_id, style=style)

        self.font_14 = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.font_16 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)

        self.text_ctrl_flow_in = wx.TextCtrl(self, wx.ID_ANY, "20")
        self.text_ctrl_head_in = wx.TextCtrl(self, wx.ID_ANY, "100")
        self.text_ctrl_efficiency_in = wx.TextCtrl(self, wx.ID_ANY, "0.80")
        self.text_ctrl_power_out = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_ctrl_power_out_metric = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)

        # Bind event handlers
        self.text_ctrl_flow_in.Bind(wx.EVT_TEXT, self.on_power_calculate)
        self.text_ctrl_head_in.Bind(wx.EVT_TEXT, self.on_power_calculate)
        self.text_ctrl_efficiency_in.Bind(wx.EVT_TEXT, self.on_power_calculate)

        self.data_path = pkg_resources.resource_filename('mechcalc', 'data/')

        self.__set_properties()
        self.__do_layout()
        self.load_values()

        # Force calculation on __init__
        self.on_power_calculate(wx.EVT_TEXT)

    def __set_properties(self):
        # only the top text control in the column needs a minsize
        self.text_ctrl_flow_in.SetMinSize((160, 36))
        self.SetBackgroundColour(wx.Colour(40, 40, 40))
        self.SetForegroundColour(wx.Colour(255, 255, 255))
        self.SetFont(self.font_16)
        self.text_ctrl_flow_in.SetFont(self.font_14)
        self.text_ctrl_head_in.SetFont(self.font_14)
        self.text_ctrl_power_out.SetFont(self.font_14)
        self.text_ctrl_power_out_metric.SetFont(self.font_14)
        self.text_ctrl_efficiency_in.SetFont(self.font_14)

    def __do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(8, 3, 4, 4)
        # The first row is blank for spacing
        grid_sizer_1.Add((185, 10), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((120, 26), 0, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, "Pump Power")
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Flow")
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_flow_in, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "USgpm")
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "Head")
        grid_sizer_1.Add(label_4, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_head_in, 0, wx.EXPAND, 0)
        label_41 = wx.StaticText(self, wx.ID_ANY, "feet")
        grid_sizer_1.Add(label_41, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_42 = wx.StaticText(self, wx.ID_ANY, "Pump Efficiency")
        grid_sizer_1.Add(label_42, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_efficiency_in, 0, wx.EXPAND, 0)
        label_43 = wx.StaticText(self, wx.ID_ANY, "(0-1)")
        grid_sizer_1.Add(label_43, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Power Required")
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_power_out, 0, wx.EXPAND, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "hp")
        grid_sizer_1.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add(self.text_ctrl_power_out_metric, 0, wx.EXPAND, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, "kW")
        grid_sizer_1.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        # add a spacer row to pad the formula image
        grid_sizer_1.Add((0, 20), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        main_sizer.Add(grid_sizer_1)

        pad_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pad_sizer.Add(40, 0, 0)
        ppower_formula_image = wx.Image(self.data_path + 'pump_power.png', wx.BITMAP_TYPE_ANY)
        ppower_formula = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(ppower_formula_image))
        pad_sizer.Add(ppower_formula, 1, 0, 0)
        main_sizer.Add(pad_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def on_power_calculate(self, event):  # wxGlade: MyFrame.<event_handler>
        """
        Numbers are entered into flow and head fields. Non-numbers
        will not be accepted. Calculation is automatic upon entering
        valid numbers.
        """
        flow = 0    # to prevent accessing variables before assignment
        head = 0
        efficiency = 0

        str_flow = (self.text_ctrl_flow_in.GetValue())
        if str_flow:
            # Maker sure str_flow contains only decimal numbers and decimals '.'
            for character in str_flow:
                if not (character.isdigit() or character == '.'):
                    index = str_flow.find(character)
                    str_flow = str_flow[0:index] + str_flow[(index + 1):]
                    self.text_ctrl_flow_in.SetValue(str_flow)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_flow:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_flow.rfind('.'))
                str_flow = str_flow[0:index] + str_flow[(index + 1):]
                self.text_ctrl_flow_in.SetValue(str_flow)
            # If the entry is too long, delete last character
            if len(str_flow) > 8:
                str_flow = str_flow[0:-1]
                self.text_ctrl_flow_in.SetValue(str_flow)
            try:
                flow = float(str_flow)
            except ValueError:
                print("Invalid input")
                return

        str_head = (self.text_ctrl_head_in.GetValue())
        if str_head:
            # Maker sure str_head contains only decimal numbers and decimals '.'
            for character in str_head:
                if not (character.isdigit() or character == '.'):
                    index = str_head.find(character)
                    str_head = str_head[0:index] + str_head[(index + 1):]
                    self.text_ctrl_head_in.SetValue(str_head)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_head:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_head.rfind('.'))
                str_head = str_head[0:index] + str_head[(index + 1):]
                self.text_ctrl_head_in.SetValue(str_head)
            # If the entry is too long, delete last character
            if len(str_head) > 8:
                str_head = str_head[0:-1]
                self.text_ctrl_head_in.SetValue(str_head)
            try:
                head = float(str_head)
            except ValueError:
                print("Invalid input")
                return

        str_efficiency = (self.text_ctrl_efficiency_in.GetValue())
        if str_efficiency:
            # Maker sure str_efficiency contains only decimal numbers and decimals '.'
            for character in str_efficiency:
                if not (character.isdigit() or character == '.'):
                    index = str_efficiency.find(character)
                    str_efficiency = str_efficiency[0:index] + str_efficiency[(index + 1):]
                    self.text_ctrl_efficiency_in.SetValue(str_efficiency)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_efficiency:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_efficiency.rfind('.'))
                str_efficiency = str_efficiency[0:index] + str_efficiency[(index + 1):]
                self.text_ctrl_efficiency_in.SetValue(str_efficiency)
            # If the entry is too long, delete last character
            if len(str_efficiency) > 4:
                str_efficiency = str_efficiency[0:-1]
                self.text_ctrl_efficiency_in.SetValue(str_efficiency)
            try:
                efficiency = float(str_efficiency)
            except ValueError:
                print("Invalid input")
                return
            # efficiency has to be between 0 and 1.0
            if (efficiency < 0) or (efficiency > 1):
                str_efficiency = str_efficiency[0:-1]
                self.text_ctrl_efficiency_in.SetValue(str_efficiency)
                try:
                    efficiency = float(str_efficiency)
                except ValueError:
                    print("Invalid input")
                    return

        if flow and head and efficiency:
            power = flow * head / 3960 / efficiency
            power_metric = power * 0.746
            power = "{0:.2f}".format(power)
            self.text_ctrl_power_out.SetValue(power)
            power_metric = "{0:.2f}".format(power_metric)
            self.text_ctrl_power_out_metric.SetValue(power_metric)
        else:
            self.text_ctrl_power_out.SetValue("")
            self.text_ctrl_power_out_metric.SetValue("")

        self.save_values()

    def save_values(self):
        values = {"flow": self.text_ctrl_flow_in.GetValue(),
                  "head": self.text_ctrl_head_in.GetValue(),
                  "efficiency": self.text_ctrl_efficiency_in.GetValue()}

        my_dump = json.dumps(values)
        file = open(self.data_path + 'pump_power.json', 'w')
        file.write(my_dump)
        file.close()

    def load_values(self):
        try:
            file = open(self.data_path + 'pump_power.json', 'r')
            read_text = file.read()
            file.close()
            values = json.loads(read_text)
            self.text_ctrl_flow_in.SetValue(values["flow"])
            self.text_ctrl_head_in.SetValue(values["head"])
            self.text_ctrl_efficiency_in.SetValue(values["efficiency"])
        except FileNotFoundError:
            return

# end class PumpPower
