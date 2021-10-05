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


class ThreePhasePower(wx.Panel):
    def __init__(self, notebook, wx_id, style):
        super().__init__(notebook, wx_id, style=style)

        self.font_14 = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.font_16 = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        self.text_ctrl_current_in = wx.TextCtrl(self, wx.ID_ANY, "20")
        self.text_ctrl_voltage_in = wx.TextCtrl(self, wx.ID_ANY, "575")
        self.text_ctrl_efficiency_in = wx.TextCtrl(self, wx.ID_ANY, "0.95")
        self.text_ctrl_power_factor_in = wx.TextCtrl(self, wx.ID_ANY, "0.90")
        self.text_ctrl_power_out = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_ctrl_power_out_hp = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)

        self.data_path = pkg_resources.resource_filename('mechcalc', 'data/')

        # Bind event handlers
        self.text_ctrl_current_in.Bind(wx.EVT_TEXT, self.on_power_calculate)
        self.text_ctrl_voltage_in.Bind(wx.EVT_TEXT, self.on_power_calculate)
        self.text_ctrl_efficiency_in.Bind(wx.EVT_TEXT, self.on_power_calculate)
        self.text_ctrl_power_factor_in.Bind(wx.EVT_TEXT, self.on_power_calculate)

        self.__set_properties()
        self.__do_layout()
        self.load_values()

        # Force calculation on __init__
        self.on_power_calculate(wx.EVT_TEXT)

    def __set_properties(self):
        # only the top text control in the column needs a minsize
        self.text_ctrl_current_in.SetMinSize((160, 36))
        self.SetBackgroundColour(wx.Colour(40, 40, 40))
        self.SetForegroundColour(wx.Colour(255, 255, 255))
        self.SetFont(self.font_16)
        self.text_ctrl_current_in.SetFont(self.font_14)
        self.text_ctrl_voltage_in.SetFont(self.font_14)
        self.text_ctrl_efficiency_in.SetFont(self.font_14)
        self.text_ctrl_power_factor_in.SetFont(self.font_14)
        self.text_ctrl_power_out.SetFont(self.font_14)
        self.text_ctrl_power_out_hp.SetFont(self.font_14)
        self.text_ctrl_efficiency_in.SetFont(self.font_14)
        self.text_ctrl_power_factor_in.SetFont(self.font_14)

    def __do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(9, 3, 4, 4)
        # The first row is blank for spacing
        grid_sizer_1.Add((160, 10), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((120, 26), 0, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, "3-phase Motor Power")
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Current")
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_current_in, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "amps")
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "Voltage")
        grid_sizer_1.Add(label_4, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_voltage_in, 0, wx.EXPAND, 0)
        label_41 = wx.StaticText(self, wx.ID_ANY, "volts")
        grid_sizer_1.Add(label_41, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_42 = wx.StaticText(self, wx.ID_ANY, "Effiency")
        grid_sizer_1.Add(label_42, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_efficiency_in, 0, wx.EXPAND, 0)
        label_43 = wx.StaticText(self, wx.ID_ANY, "(0-1)")
        grid_sizer_1.Add(label_43, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_44 = wx.StaticText(self, wx.ID_ANY, "Power Factor")
        grid_sizer_1.Add(label_44, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_power_factor_in, 0, wx.EXPAND, 0)
        label_45 = wx.StaticText(self, wx.ID_ANY, "(0-1)")
        grid_sizer_1.Add(label_45, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Power")
        grid_sizer_1.Add(label_5, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_power_out, 0, wx.EXPAND, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "kW")
        grid_sizer_1.Add(label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add(self.text_ctrl_power_out_hp, 0, wx.EXPAND, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, "hp")
        grid_sizer_1.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        # add a spacer row to pad the formula image
        grid_sizer_1.Add((0, 20), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        main_sizer.Add(grid_sizer_1)

        pad_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pad_sizer.Add(40, 0, 0)
        power_formula_image = wx.Image(self.data_path + 'motor_power.png', wx.BITMAP_TYPE_ANY)
        power_formula = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(power_formula_image))
        pad_sizer.Add(power_formula, 1, 0, 0)
        main_sizer.Add(pad_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def on_power_calculate(self, event):  # wxGlade: MyFrame.<event_handler>
        """
        Numbers are entered into current, voltage, efficiency
        and power factor fields. Non-numbers will not be accepted.
        Calculation is automatic upon entering valid numbers.
        """
        current = 0  # to prevent accessing variables before assignment
        voltage = 0
        efficiency = 0

        str_current = (self.text_ctrl_current_in.GetValue())
        if str_current:
            # Maker sure str_current contains only decimal numbers and decimals '.'
            for character in str_current:
                if not (character.isdigit() or character == '.'):
                    index = str_current.find(character)
                    str_current = str_current[0:index] + str_current[(index + 1):]
                    self.text_ctrl_current_in.SetValue(str_current)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_current:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_current.rfind('.'))
                str_current = str_current[0:index] + str_current[(index + 1):]
                self.text_ctrl_current_in.SetValue(str_current)
            # If the entry is too long, delete last character
            if len(str_current) > 8:
                str_current = str_current[0:-1]
                self.text_ctrl_current_in.SetValue(str_current)
            try:
                current = float(str_current)
            except ValueError:
                print("Invalid input")
                return

        str_voltage = (self.text_ctrl_voltage_in.GetValue())
        if str_voltage:
            # Maker sure str_voltage contains only decimal numbers and decimals '.'
            for character in str_voltage:
                if not (character.isdigit() or character == '.'):
                    index = str_voltage.find(character)
                    str_voltage = str_voltage[0:index] + str_voltage[(index + 1):]
                    self.text_ctrl_voltage_in.SetValue(str_voltage)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_voltage:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_voltage.rfind('.'))
                str_voltage = str_voltage[0:index] + str_voltage[(index + 1):]
                self.text_ctrl_voltage_in.SetValue(str_voltage)
            # If the entry is too long, delete last character
            if len(str_voltage) > 8:
                str_voltage = str_voltage[0:-1]
                self.text_ctrl_voltage_in.SetValue(str_voltage)
            try:
                voltage = float(str_voltage)
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

        str_power_factor = (self.text_ctrl_power_factor_in.GetValue())
        if str_power_factor:
            # Maker sure str_power_factor contains only decimal numbers and decimals '.'
            for character in str_power_factor:
                if not (character.isdigit() or character == '.'):
                    index = str_power_factor.find(character)
                    str_power_factor = str_power_factor[0:index] + str_power_factor[(index + 1):]
                    self.text_ctrl_power_factor_in.SetValue(str_power_factor)
            # if there are two decimals, delete the right most one
            counter = 0
            for character in str_power_factor:
                if character == ".":
                    counter += 1
            if counter > 1:
                index = (str_power_factor.rfind('.'))
                str_power_factor = str_power_factor[0:index] + str_power_factor[(index + 1):]
                self.text_ctrl_power_factor_in.SetValue(str_power_factor)
            # If the entry is too long, delete last character
            if len(str_power_factor) > 4:
                str_power_factor = str_power_factor[0:-1]
                self.text_ctrl_power_factor_in.SetValue(str_power_factor)
            try:
                power_factor = float(str_power_factor)
            except ValueError:
                print("Invalid input")
                return
            # power_factor has to be between 0 and 1.0
            if (power_factor < 0) or (power_factor > 1):
                str_power_factor = str_power_factor[0:-1]
                self.text_ctrl_power_factor_in.SetValue(str_power_factor)
                try:
                    power_factor = float(str_power_factor)
                except ValueError:
                    print("Invalid input")
                    return

        if current and voltage and efficiency and power_factor:
            power = current * voltage * efficiency * power_factor \
                    * 1.73 / 1000
            power_metric = power / 0.746
            power = "{0:.2f}".format(power)
            self.text_ctrl_power_out.SetValue(power)
            power_metric = "{0:.2f}".format(power_metric)
            self.text_ctrl_power_out_hp.SetValue(power_metric)
        else:
            self.text_ctrl_power_out.SetValue("")
            self.text_ctrl_power_out_hp.SetValue("")

        self.save_values()

    def save_values(self):
        values = {"current": self.text_ctrl_current_in.GetValue(),
                  "voltage": self.text_ctrl_voltage_in.GetValue(),
                  "efficiency": self.text_ctrl_efficiency_in.GetValue(),
                  "power_factor": self.text_ctrl_power_factor_in.GetValue()}

        my_dump = json.dumps(values)
        file = open(self.data_path + 'three_phase_power.json', 'w')
        file.write(my_dump)
        file.close()

    def load_values(self):
        try:
            file = open(self.data_path + 'three_phase_power.json', 'r')
            read_text = file.read()
            file.close()
            values = json.loads(read_text)
            self.text_ctrl_current_in.SetValue(values["current"])
            self.text_ctrl_voltage_in.SetValue(values["voltage"])
            self.text_ctrl_efficiency_in.SetValue(values["efficiency"])
            self.text_ctrl_power_factor_in.SetValue(values["power_factor"])
        except FileNotFoundError:
            return

# end class ThreePhasePower
