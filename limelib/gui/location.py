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

from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .widget.worldmapwidget import WorldMapWidget
import json
import os

zone = set()

is_zone_system = os.path.isfile("/usr/share/lime-installer/data/zone.json")

if is_zone_system:
    zone_info = json.loads(open("/usr/share/lime-installer/data/zone.json").read())

    for k, v in zone_info.items():
        zone.add(k)

else:
    zone_info = json.loads(open("data/zone.json").read())

    for k, v in zone_info.items():
        zone.add(k)

zone = list(zone)
zone.sort()


class LocationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        self.worldMap = WorldMapWidget(self)
        self.layout().addWidget(self.worldMap)

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        self.cLabel = QLabel()
        hlayout.addWidget(self.cLabel)

        self.cBox = QComboBox()
        self.cBox.setFixedWidth(300)
        hlayout.addWidget(self.cBox)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Expanding))

        self.iLabel = QLabel()
        hlayout.addWidget(self.iLabel)

        self.iBox = QComboBox()
        self.iBox.setFixedWidth(300)
        hlayout.addWidget(self.iBox)

        self.cBox.addItems(zone)

        info = zone_info[self.cBox.currentText()]
        info.sort()
        self.iBox.addItems(info)

        self.parent.lilii_settings["timezone"] = "{}/{}".format(self.cBox.currentText() , self.iBox.currentText())

        self.cBox.currentTextChanged.connect(self.zoneChanged)
        self.iBox.currentTextChanged.connect(self.cityChanged)
        self.worldMap.zoneName.emit("{}/{}".format(self.cBox.currentText(), self.iBox.currentText()))
        self.parent.languageChanged.connect(self.retranslate)
        self.worldMap.zone.connect(self.zoneChange)


        self.retranslate()

    def retranslate(self):
        self.setWindowTitle(self.tr("System Location"))
        self.cLabel.setText(self.tr("Region:"))
        self.iLabel.setText(self.tr("City:"))

    def zoneChange(self, a, b):
        self.cBox.setCurrentText(a)
        self.iBox.setCurrentText(b)

    def zoneChanged(self, zone):
        info = zone_info[self.cBox.currentText()]
        info.sort()
        self.iBox.clear()
        self.iBox.addItems(info)
        self.parent.lilii_settings["timezone"] = "{}/{}".format(self.cBox.currentText(), self.iBox.currentText())
        self.worldMap.zoneName.emit("{}/{}".format(self.cBox.currentText(), self.iBox.currentText()))

    def cityChanged(self, city):
        self.parent.lilii_settings["timezone"] = "{}/{}".format(self.cBox.currentText(), self.iBox.currentText())
        if self.iBox.currentText():
            self.worldMap.zoneName.emit("{}/{}".format(self.cBox.currentText(), self.iBox.currentText()))
