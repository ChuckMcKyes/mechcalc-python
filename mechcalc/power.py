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


class Power(wx.Panel):
    def __init__(self, notebook, wx_id, style):
        super().__init__(notebook, wx_id, style=style)

        self.font_14 = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.font_16 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)

        self.text_ctrl_torque_in = wx.TextCtrl(self, wx.ID_ANY, "20")
        self.text_ctrl_rpm_in = wx.TextCtrl(self, wx.ID_ANY, "1800")
        self.text_ctrl_power_out = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_ctrl_power_out_metric = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)

        self.data_path = pkg_resources.resource_filename('mechcalc', 'data/')

        # Bind event handlers
        self.text_ctrl_torque_in.Bind(wx.EVT_TEXT, self.on_power_calculate)
        self.text_ctrl_rpm_in.Bind(wx.EVT_TEXT, self.on_power_calculate)

        self.__set_properties()
        self.__do_layout()
        self.load_values()

        # Force calculation on __init__
        self.on_power_calculate(wx.EVT_TEXT)

    def __set_properties(self):
        # only the top text control in the column needs a minsize
        self.text_ctrl_torque_in.SetMinSize((160, 36))
        self.SetBackgroundColour(wx.Colour(40, 40, 40))
        self.SetForegroundColour(wx.Colour(255, 255, 255))
        self.SetFont(self.font_16)
        self.text_ctrl_torque_in.SetFont(self.font_14)
        self.text_ctrl_rpm_in.SetFont(self.font_14)
        self.text_ctrl_power_out.SetFont(self.font_14)
        self.text_ctrl_power_out_metric.SetFont(self.font_14)

    def __do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2 = wx.FlexGridSizer(7, 3, 4, 4)
        # The first row is blank for spacing
        grid_sizer_2.Add((90, 10), 0, 0, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        grid_sizer_2.Add((60, 26), 0, 0, 0)
        label_11 = wx.StaticText(self, wx.ID_ANY, "Power")
        grid_sizer_2.Add(label_11, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        label_12 = wx.StaticText(self, wx.ID_ANY, "Torque")
        grid_sizer_2.Add(label_12, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.text_ctrl_torque_in, 0, wx.EXPAND, 0)
        label_13 = wx.StaticText(self, wx.ID_ANY, u"ft\u2022lbf")
        grid_sizer_2.Add(label_13, 0, 0, 0)
        label_14 = wx.StaticText(self, wx.ID_ANY, "rpm")
        grid_sizer_2.Add(label_14, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.text_ctrl_rpm_in, 0, wx.EXPAND, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        label_15 = wx.StaticText(self, wx.ID_ANY, "Power")
        grid_sizer_2.Add(label_15, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.text_ctrl_power_out, 0, wx.EXPAND, 0)
        label_16 = wx.StaticText(self, wx.ID_ANY, "horsepower")
        grid_sizer_2.Add(label_16, 0, 0, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        grid_sizer_2.Add(self.text_ctrl_power_out_metric, 0, wx.EXPAND, 0)
        label_18 = wx.StaticText(self, wx.ID_ANY, "kW")
        grid_sizer_2.Add(label_18, 0, 0, 0)
        # add a spacer row to pad the formula image
        grid_sizer_2.Add((0, 20), 0, 0, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        grid_sizer_2.Add((0, 0), 0, 0, 0)
        main_sizer.Add(grid_sizer_2)

        pad_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pad_sizer.Add(40, 0, 0)
        power_formula_image = wx.Image(self.data_path + 'power.png', wx.BITMAP_TYPE_ANY)
        power_formula = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(power_formula_image))
        pad_sizer.Add(power_formula)
        main_sizer.Add(pad_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def on_power_calculate(self, event):   # event handler
        """
        Numbers are entered into power and rpm fields. Non-numbers
        will not be accepted. Calculation is automatic upon entering
        valid numbers.
        """
        torque = 0  # to prevent accessing variables before assignment
        rpm = 0

        str_torque = (self.text_ctrl_torque_in.GetValue())
        if str_torque:
            # Maker sure str_torque contains only decimal numbers and decimals '.'
            for character in str_torque:
                if not (character.isdigit() or character == '.'):
                    index = str_torque.find(character)
                    str_torque = str_torque[0:index] + str_torque[(index + 1):]
                    self.text_ctrl_torque_in.SetValue(str_torque)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_torque:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_torque.rfind('.'))
                str_torque = str_torque[0:index] + str_torque[(index + 1):]
                self.text_ctrl_torque_in.SetValue(str_torque)
            # If the entry is too long, delete last character
            if len(str_torque) > 8:
                str_torque = str_torque[0:-1]
                self.text_ctrl_torque_in.SetValue(str_torque)
            try:
                torque = float(str_torque)
            except ValueError:
                print("Invalid input")
                return

        str_rpm = (self.text_ctrl_rpm_in.GetValue())
        if str_rpm:
            # Maker sure str_rpm contains only decimal numbers and decimals '.'
            for character in str_rpm:
                if not (character.isdigit() or character == '.'):
                    index = str_rpm.find(character)
                    str_rpm = str_rpm[0:index] + str_rpm[(index + 1):]
                    self.text_ctrl_rpm_in.SetValue(str_rpm)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_rpm:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_rpm.rfind('.'))
                str_rpm = str_rpm[0:index] + str_rpm[(index + 1):]
                self.text_ctrl_rpm_in.SetValue(str_rpm)
            # If the entry is too long, delete last character
            if len(str_rpm) > 8:
                str_rpm = str_rpm[0:-1]
                self.text_ctrl_rpm_in.SetValue(str_rpm)
            try:
                rpm = float(str_rpm)
            except ValueError:
                print("Invalid input")
                return

        if torque and rpm:
            power = torque * rpm / 5252
            power_metric = power * 0.746
            power = "{0:.2f}".format(power)
            self.text_ctrl_power_out.SetValue(power)
            power_metric = "{0:.2f}".format(power_metric)
            self.text_ctrl_power_out_metric.SetValue(power_metric)
        else:
            self.text_ctrl_power_out.SetValue("")
            self.text_ctrl_power_out_metric.SetValue("")

        # Save field values to file
        self.save_values()

    def save_values(self):
        values = {"torque": self.text_ctrl_torque_in.GetValue(),
                  "rpm": self.text_ctrl_rpm_in.GetValue()}

        my_dump = json.dumps(values)
        file = open(self.data_path + 'power.json', 'w')
        file.write(my_dump)
        file.close()

    def load_values(self):
        try:
            file = open(self.data_path + 'power.json', 'r')
            read_text = file.read()
            file.close()
            values = json.loads(read_text)
            self.text_ctrl_torque_in.SetValue(values["torque"])
            self.text_ctrl_rpm_in.SetValue(values["rpm"])
        except FileNotFoundError:
            return

# end class Power
