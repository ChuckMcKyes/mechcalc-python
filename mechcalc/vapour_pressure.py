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
import wx.grid
import pkg_resources
import json
import platform


class VapourPressure(wx.Panel):
    def __init__(self, notebook, wx_id, style):
        super().__init__(notebook, wx_id, style=style)

        self.grid_1 = wx.grid.Grid(self, wx.ID_ANY, size=(1, 1))
        self.text_ctrl_mixture_vapour_pressure = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_3 = wx.StaticText(self, wx.ID_ANY, "")
        self.label_3.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        self.data_path = pkg_resources.resource_filename('mechcalc', 'data/')

        # Bind event handlers
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_CHANGED, self.calculate_vapour_pressure, self.grid_1)

        self.__set_properties()
        self.__do_layout()
        self.load_values()

        # Force calculation in __init__.
        self.calculate_vapour_pressure(wx.grid.EVT_GRID_CMD_CELL_CHANGED)

    def __set_properties(self):
        self.grid_1.CreateGrid(4, 7)
        self.grid_1.SetColLabelValue(0, "Liquid")
        self.grid_1.SetColLabelValue(1, "Molar Mass")
        self.grid_1.SetColLabelValue(2, "Mass Fraction")
        self.grid_1.SetColLabelValue(3, "Moles in 1 gram")
        self.grid_1.SetColLabelValue(4, "Mole Fraction")
        self.grid_1.SetColLabelValue(5, "Vapour Pressure")
        self.grid_1.SetColLabelValue(6, "Partial Pressure")
        self.grid_1.SetMinSize((4, 7))
        self.grid_1.SetColSize(0, 100)
        self.grid_1.SetColSize(1, -1)
        self.grid_1.SetColSize(2, -1)
        self.grid_1.SetColSize(3, -1)
        self.grid_1.SetColSize(4, -1)
        self.grid_1.SetColSize(5, -1)
        self.grid_1.SetColSize(6, -1)
        self.grid_1.SetColFormatFloat(1, -1, 1)
        self.grid_1.SetColFormatFloat(2, -1, 2)
        self.grid_1.SetColFormatFloat(3, -1, 6)
        self.grid_1.SetColFormatFloat(4, -1, 6)
        self.grid_1.SetColFormatFloat(5, -1, 2)
        self.grid_1.SetColFormatFloat(6, -1, 6)
        self.grid_1.SetReadOnly(0, 3)
        self.grid_1.SetReadOnly(1, 3)
        self.grid_1.SetReadOnly(2, 3)
        self.grid_1.SetReadOnly(3, 3)
        self.grid_1.SetReadOnly(0, 4)
        self.grid_1.SetReadOnly(1, 4)
        self.grid_1.SetReadOnly(2, 4)
        self.grid_1.SetReadOnly(3, 4)
        self.grid_1.SetReadOnly(0, 6)
        self.grid_1.SetReadOnly(1, 6)
        self.grid_1.SetReadOnly(2, 6)
        self.grid_1.SetReadOnly(3, 6)
        self.grid_1.HideRowLabels()

        # Set a lighter background colour for changeable cells
        changeable_cell_attributes = wx.grid.GridCellAttr()
        # Set a darker background for Linux
        if platform.system() == "Linux":
            changeable_cell_attributes.SetBackgroundColour(wx.Colour(80, 80, 80))
        else:
            changeable_cell_attributes.SetBackgroundColour(wx.Colour(120, 120, 120))

        self.grid_1.SetColAttr(0, changeable_cell_attributes)
        self.grid_1.SetColAttr(1, changeable_cell_attributes)
        self.grid_1.SetColAttr(2, changeable_cell_attributes)
        self.grid_1.SetColAttr(5, changeable_cell_attributes)

        # Set default values for testing
        self.grid_1.SetCellValue(0, 0, 'Water')
        self.grid_1.SetCellValue(1, 0, 'Ethanol')
        self.grid_1.SetCellValue(0, 1, '18.01')
        self.grid_1.SetCellValue(1, 1, '46.07')
        self.grid_1.SetCellValue(0, 2, '0.80')
        self.grid_1.SetCellValue(1, 2, '0.20')
        self.grid_1.SetCellValue(0, 5, '289')
        self.grid_1.SetCellValue(1, 5, '12.4')

    def __do_layout(self):
        # main sizer
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        # sizer for result
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        label_0 = wx.StaticText(self, wx.ID_ANY, "Vapour Pressure of a Mixture")
        sizer_2.Add(label_0, 0, wx.ALL, 4)
        sizer_2.Add(self.grid_1, 3, wx.EXPAND | wx.ALL, 4)
        label_1 = wx.StaticText(self, wx.ID_ANY, "Mixture Vapour Pressure")
        sizer_3.Add(label_1, 0, 0, 0)
        sizer_3.Add((20, 0), 0, 0, 0)
        sizer_3.Add(self.text_ctrl_mixture_vapour_pressure, 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "mmHg")
        sizer_3.Add((20, 0), 0, 0, 0)
        sizer_3.Add(label_2, 0, wx.RIGHT, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_2.Add(self.label_3, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        self.Layout()

    def calculate_vapour_pressure(self, event):  # wxGlade: MyFrame.<event_handler>
        try:
            total_moles = 0.0
            mixture_vapour_pressure = 0.0
            self.label_3.SetLabelText("")
            number_of_rows = self.grid_1.NumberRows

            # If there is no input data in a row then
            # clear the results to get a valid calculation
            for row_index in range(number_of_rows):
                if not (self.grid_1.GetCellValue(row_index, 0)
                        and self.grid_1.GetCellValue(row_index, 1)
                        and self.grid_1.GetCellValue(row_index, 2)
                        and self.grid_1.GetCellValue(row_index, 5)):
                    self.grid_1.SetCellValue(row_index, 3, "")
                    self.grid_1.SetCellValue(row_index, 4, "")
                    self.grid_1.SetCellValue(row_index, 6, "")

            # Check that sum of mass fractions equal 1
            total_mass_fraction = 0.0
            for row_index in range(0, number_of_rows):
                if self.grid_1.GetCellValue(row_index, 2):
                    mass_fraction = float(self.grid_1.GetCellValue(row_index, 2))
                    total_mass_fraction += mass_fraction

            if total_mass_fraction != 1.0:
                self.label_3.SetLabelText("Warning: total mass fraction not equal to 1.0!")
                self.text_ctrl_mixture_vapour_pressure.SetValue("")
                return

            # Calculate the total number of moles in one gram of mixture
            for row_index in range(0, number_of_rows):
                # Number of moles in 1 gram total = mass fraction / molar mass
                if self.grid_1.GetCellValue(row_index, 2) and self.grid_1.GetCellValue(row_index, 1):
                    moles = float(self.grid_1.GetCellValue(row_index, 2)) / \
                            float(self.grid_1.GetCellValue(row_index, 1))
                    self.grid_1.SetCellValue(row_index, 3, str(moles))
                    total_moles += moles

            # Calculate the partial pressures of the liquids
            for row_index in range(0, number_of_rows):
                if self.grid_1.GetCellValue(row_index, 3):
                    # mole_fraction = moles / total_moles
                    mole_fraction = float(self.grid_1.GetCellValue(row_index, 3)) / total_moles
                    self.grid_1.SetCellValue(row_index, 4, str(mole_fraction))
                    # partial_pressure = mole_fraction * vapour_pressure
                    partial_pressure = mole_fraction * float(self.grid_1.GetCellValue(row_index, 5))
                    self.grid_1.SetCellValue(row_index, 6, str(partial_pressure))
                    mixture_vapour_pressure += partial_pressure

            self.text_ctrl_mixture_vapour_pressure.SetValue(
                f"{mixture_vapour_pressure:.2f}")

            self.save_values()
        except:
            return

    def save_values(self):
        values = {}
        for row_index in range(self.grid_1.NumberRows):
            values[row_index] = \
                {"liquid": self.grid_1.GetCellValue(row_index, 0),
                 "molar_mass": self.grid_1.GetCellValue(row_index, 1),
                 "mass_fraction": self.grid_1.GetCellValue(row_index, 2),
                 "vapour_pressure": self.grid_1.GetCellValue(row_index, 5)}

        my_dump = json.dumps(values)
        file = open(self.data_path + 'vapour_pressure.json', 'w')
        file.write(my_dump)
        file.close()

    def load_values(self):
        try:
            file = open(self.data_path + 'vapour_pressure.json', 'r')
            read_text = file.read()
            file.close()
            values = json.loads(read_text)
            for row_index in range(len(values)):
                values[row_index] = \
                    {self.grid_1.SetCellValue(row_index, 0, values[str(row_index)]["liquid"]),
                     self.grid_1.SetCellValue(row_index, 1, values[str(row_index)]["molar_mass"]),
                     self.grid_1.SetCellValue(row_index, 2, values[str(row_index)]["mass_fraction"]),
                     self.grid_1.SetCellValue(row_index, 5, values[str(row_index)]["vapour_pressure"])}

        except FileNotFoundError:
            return

# end class VapourPressure
