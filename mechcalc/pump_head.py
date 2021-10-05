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


class PumpHead(wx.Panel):
    def __init__(self, notebook, wx_id, style):
        super().__init__(notebook, wx_id, style=style)

        self.font_14 = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)
        self.font_16 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL)

        self.text_ctrl_diameter_in = wx.TextCtrl(self, wx.ID_ANY, "8")
        self.text_ctrl_rpm_in = wx.TextCtrl(self, wx.ID_ANY, "1800")
        self.text_ctrl_head_out = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_ctrl_head_out_metric = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)

        self.data_path = pkg_resources.resource_filename('mechcalc', 'data/')

        # Bind event handlers
        self.text_ctrl_diameter_in.Bind(wx.EVT_TEXT, self.on_head_calculate)
        self.text_ctrl_rpm_in.Bind(wx.EVT_TEXT, self.on_head_calculate)

        self.__set_properties()
        self.__do_layout()
        self.load_values()

        # Force calculation on __init__
        self.on_head_calculate(wx.EVT_TEXT)

    def __set_properties(self):
        # only the top text control in the column needs a minsize
        self.text_ctrl_diameter_in.SetMinSize((160, 36))
        self.SetBackgroundColour(wx.Colour(40, 40, 40))
        self.SetForegroundColour(wx.Colour(255, 255, 255))
        self.SetFont(self.font_16)
        self.text_ctrl_diameter_in.SetFont(self.font_14)
        self.text_ctrl_rpm_in.SetFont(self.font_14)
        self.text_ctrl_head_out.SetFont(self.font_14)
        self.text_ctrl_head_out_metric.SetFont(self.font_14)

    def __do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(8, 3, 4, 4)
        # The first row is blank for spacing
        grid_sizer_1.Add((150, 10), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((120, 26), 0, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, "Pump Head")
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Impeller dia.")
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_diameter_in, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "inches")
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "rpm")
        grid_sizer_1.Add(label_4, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_rpm_in, 0, wx.EXPAND, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Head")
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_head_out, 0, wx.EXPAND, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "feet")
        grid_sizer_1.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add(self.text_ctrl_head_out_metric, 0, wx.EXPAND, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, "m")
        grid_sizer_1.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        # add a spacer row to pad the formula image
        grid_sizer_1.Add((0, 20), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        main_sizer.Add(grid_sizer_1)

        pad_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pad_sizer.Add(40, 0, 0)
        head_formula_image = wx.Image(self.data_path + 'pump_head.png', wx.BITMAP_TYPE_ANY)
        head_formula = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(head_formula_image))
        pad_sizer.Add(head_formula)
        main_sizer.Add(pad_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def on_head_calculate(self, event):  # wxGlade: MyFrame.<event_handler>
        """
        Numbers are entered into diameter and rpm fields. Non-numbers
        will not be accepted. Calculation is automatic upon entering
        valid numbers.
        """
        diameter = 0    # to prevent accessing variables before assignment
        rpm = 0

        str_diameter = (self.text_ctrl_diameter_in.GetValue())
        if str_diameter:
            # Maker sure str_diameter contains only decimal numbers and decimals '.'
            for character in str_diameter:
                if not (character.isdigit() or character == '.'):
                    index = str_diameter.find(character)
                    str_diameter = str_diameter[0:index] + str_diameter[(index + 1):]
                    self.text_ctrl_diameter_in.SetValue(str_diameter)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_diameter:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_diameter.rfind('.'))
                str_diameter = str_diameter[0:index] + str_diameter[(index + 1):]
                self.text_ctrl_diameter_in.SetValue(str_diameter)
            # If the entry is too long, delete last character
            if len(str_diameter) > 8:
                str_diameter = str_diameter[0:-1]
                self.text_ctrl_diameter_in.SetValue(str_diameter)
            try:
                diameter = float(str_diameter)
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

        if diameter and rpm:
            head = diameter ** 2 * (rpm/1800)**2
            head_metric = head * 0.3048
            head = "{0:.2f}".format(head)
            self.text_ctrl_head_out.SetValue(head)
            head_metric = "{0:.2f}".format(head_metric)
            self.text_ctrl_head_out_metric.SetValue(head_metric)
        else:
            self.text_ctrl_head_out.SetValue("")
            self.text_ctrl_head_out_metric.SetValue("")

        self.save_values()

    def save_values(self):
        values = {"diameter": self.text_ctrl_diameter_in.GetValue(),
                  "rpm": self.text_ctrl_rpm_in.GetValue()}

        my_dump = json.dumps(values)
        file = open(self.data_path + 'pump_head.json', 'w')
        file.write(my_dump)
        file.close()

    def load_values(self):
        try:
            file = open(self.data_path + 'pump_head.json', 'r')
            read_text = file.read()
            file.close()
            values = json.loads(read_text)
            self.text_ctrl_diameter_in.SetValue(values["diameter"])
            self.text_ctrl_rpm_in.SetValue(values["rpm"])
        except FileNotFoundError:
            return

# end class PumpHead
