#
#
#  Copyright 2017 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from setuptools import setup, find_packages
from os import listdir, system
import glob

langs = []
for l in listdir('languages'):
    if l.endswith('ts'):
        system('lrelease languages/%s' % l)
        langs.append(('languages/%s' % l).replace('.ts', '.qm'))


system('pyrcc5 lime-installer.qrc -o limelib/limerc.py')

datas = [('/usr/share/applications', ['data/lime-installer.desktop']),
         #('/etc/skel/.config/autostart', ['data/lime-installer.desktop']), # system start autostart uncomment
         ('/usr/share/icons/hicolor/scalable/apps', ['images/lime-installer.svg']),
         ('/usr/share/lime-installer/languages', langs),
         ('/usr/share/lime-installer/data', glob.glob("data/*.json")),
         ('/usr/share/lime-installer/', ["distro_custom.conf"])
         ]

setup(
    name = "lime-installer",
    scripts = ["lime-installer"],
    packages = find_packages(),
    version = "1.0 Beta",
    license = "GPL v3",
    description = "Lime GNU/Linux System Installer",
    author = "Metehan Özbek",
    author_email = "mthnzbk@gmail.com",
    url = "https://github.com/mthnzbk/lime-installer",
    keywords = ["PyQt5", "installer"],
    data_files = datas
)
