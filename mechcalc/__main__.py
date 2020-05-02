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
from mechcalc import MyFrame


class MyApp(wx.App):
    def OnInit(self):
        self.my_frame = MyFrame(None, wx.ID_ANY)
        self.SetTopWindow(self.my_frame)
        self.my_frame.Show()
        return True
# end of class MyApp


def main():
    app = MyApp(0)
    app.MainLoop()


if __name__ == "__main__":
    main()
