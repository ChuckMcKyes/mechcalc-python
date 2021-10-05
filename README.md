# mechcalc

Mechanical Engineering Calculators, Chuck McKyes<br>
This is a gui app based on wxPython.<br>
v1.3.2 October 2021<br>
<br>
Copyright (C) 2021 Chuck McKyes</br>
<br>
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

<br>
*** Verify calculations produced by this software. ***<br><br>

All calculations are approximate estimates. Actual specifications
are available from equipment manufacturers.

Pump power and head assume cold water being pumped.
Vapour pressure of a mixture uses Raoult's law.

wxPython is required. In Windows, Microsoft Visual C++
redistributable is required. I find that everything works
with Python 3.7.3 in Debian and Python 3.8.6 in Windows 10,
but Python 3.9.0 does not appear to work on Windows 10.

Debian requires python3-wxgtk to be installed via your package manager.
For example, on a Raspberry Pi 4 as of this writing, the version is
python3-wxgtk4.0-4.0.4+dfsg-2.

This python script can be run using "python3 -m mechcalc" on the
command line or by creating a shortcut.

In Debian, a desktop shortcut can be created by creating
a file with a .desktop extension (e.g., "MechCalc.desktop").
Make the contents this:

[Desktop Entry]<br>
Version=1.1.2<br>
Type=Application<br>
Name=MechCalc<br>
Comment=<br>
Exec=python3 -m mechcalc<br>
Icon=<br>
Path=<br>
Terminal=false<br>
StartupNotify=false<br>

In Windows, right-click on the desktop or in file explorer
and create a shortcut. Right click again and select Properties.
Enter "<your python install directory>\pythonw.exe -m mechcalc"
in the "Target:" field, and <your python install directory>
in the "Start in:" field. ("pythonw.exe" starts the script without
a command line console.)
