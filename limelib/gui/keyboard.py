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

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from .widget.keyboardlabel import KeyboardLabel
import os
import json


class KeyboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        centerLayout = QHBoxLayout()
        self.layout().addLayout(centerLayout)

        self.keyLabel = KeyboardLabel(self)
        centerLayout.addWidget(self.keyLabel)

        self.layout().addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        hlayoutx = QHBoxLayout()
        self.layout().addLayout(hlayoutx)

        self.modelLabel = QLabel()
        #self.modelLabel.setFixedWidth(150)
        hlayoutx.addWidget(self.modelLabel)

        self.modelList = QComboBox()
        hlayoutx.addWidget(self.modelList)

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        self.countryLabel = QLabel()
        hlayout.addWidget(self.countryLabel)

        self.countryList = QComboBox()
        #self.countryList.setFixedWidth(325)
        hlayout.addWidget(self.countryList)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Expanding))

        self.keyboardLabel = QLabel()
        hlayout.addWidget(self.keyboardLabel)

        self.keyboardVList = QComboBox()
        #self.keyboardVList.setFixedWidth(325)
        hlayout.addWidget(self.keyboardVList)

        self.testEdit = QLineEdit()
        #self.testEdit.setFixedWidth(800)
        self.layout().addWidget(self.testEdit)

        self.layout().addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        self.keyboard_list = None
        if os.path.isfile("/usr/share/lime-installer/data/models.json"):
            self.keyboard_list = json.loads(open("/usr/share/lime-installer/data/models.json").read())
        else:
            self.keyboard_list = json.loads(open("data/models.json").read())

        self.layout_list = None
        if os.path.isfile("/usr/share/lime-installer/data/layouts.json"):
            self.layout_list = json.loads(open("/usr/share/lime-installer/data/layouts.json").read())
        else:
            self.layout_list = json.loads(open("data/layouts.json").read())

        self.variant_list = None
        if os.path.isfile("/usr/share/lime-installer/data/variants.json"):
            self.variant_list = json.loads(open("/usr/share/lime-installer/data/variants.json").read())
        else:
            self.variant_list = json.loads(open("data/variants.json").read())

        model = list(self.keyboard_list.keys())
        model.sort()
        for i in model:
            self.modelList.addItem(self.keyboard_list[i])
            if i == "pc105":
                self.modelList.setCurrentText(self.keyboard_list[i])
                self.parent.lilii_settings["keyboard_model"] = i, self.keyboard_list[i]

        keys = list(self.layout_list.keys())
        keys.sort()
        for i in keys:
            self.countryList.addItem(self.layout_list[i])

        default = self.layout_list.get(self.parent.lilii_settings["lang"][:2], "us")
        if default == "us":
            self.countryList.setCurrentText(self.layout_list[default])
            self.parent.lilii_settings["keyboard_layout"] = default, self.layout_list[default]

        else:
            self.countryList.setCurrentText(default)
            self.parent.lilii_settings["keyboard_layout"] = self.parent.lilii_settings["lang"][:2], default

        self.keyboardVList.addItem("Default")
        for k, v in self.variant_list.items():
            if k == self.parent.lilii_settings["keyboard_layout"][0]:
                for i in v:
                    self.keyboardVList.addItems(i.values())
        self.parent.lilii_settings["keyboard_variant"] = None

        self.modelList.currentTextChanged.connect(self.keyboardModelSelect)
        self.countryList.currentTextChanged.connect(self.countrySelect)
        self.keyboardVList.currentTextChanged.connect(self.keyboardTypeSelect)
        self.parent.languageChanged.connect(self.retranslate)

        self.keyLabel.keyboardInfo.emit(self.parent.lilii_settings["keyboard_model"][0],
                                        self.parent.lilii_settings["keyboard_layout"][0],
                                        self.parent.lilii_settings["keyboard_variant"])

        self.retranslate()

    def retranslate(self):
        self.setWindowTitle(self.tr("Keyboard Layout"))
        self.modelLabel.setText(self.tr("Keyboard Model:"))
        self.countryLabel.setText(self.tr("Language:"))
        self.keyboardLabel.setText(self.tr("Keyboard Kind:"))
        self.testEdit.setPlaceholderText(self.tr("Test out your keyboard."))

    def keyboardModelSelect(self, value):
        for model in self.keyboard_list.keys():
            if self.keyboard_list[model] == value:
                self.parent.lilii_settings["keyboard_model"] = model, value

        self.keyLabel.keyboardInfo.emit(self.parent.lilii_settings["keyboard_model"][0],
                                        self.parent.lilii_settings["keyboard_layout"][0],
                                        self.parent.lilii_settings["keyboard_variant"])

    def countrySelect(self, value):
        for layout in self.layout_list.keys():
            if self.layout_list[layout] == value:
                self.parent.lilii_settings["keyboard_layout"] = layout, value

        self.keyboardVList.clear()
        self.parent.lilii_settings["keyboard_variant"] = None
        self.keyboardVList.addItem("Default")
        for k, v in self.variant_list.items():
            if k == self.parent.lilii_settings["keyboard_layout"][0]:
                for i in v:
                    self.keyboardVList.addItems(i.values())

        os.system("setxkbmap -layout {} -variant \"\"".format(self.parent.lilii_settings["keyboard_layout"][0]))
        self.keyLabel.keyboardInfo.emit(self.parent.lilii_settings["keyboard_model"][0],
                                        self.parent.lilii_settings["keyboard_layout"][0],
                                        self.parent.lilii_settings["keyboard_variant"])

    def keyboardTypeSelect(self, value):
        if value == "Default":
            os.system("setxkbmap -variant \"\"")
            self.parent.lilii_settings["keyboard_variant"] = None
            self.keyLabel.keyboardInfo.emit(self.parent.lilii_settings["keyboard_model"][0],
                                            self.parent.lilii_settings["keyboard_layout"][0],
                                            self.parent.lilii_settings["keyboard_variant"])

        else:
            for variant in self.variant_list.keys():
                if variant in self.parent.lilii_settings["keyboard_layout"]:
                    for key in self.variant_list[variant]:
                        if key[list(key.keys())[0]] == value:
                            self.parent.lilii_settings["keyboard_variant"] = list(key.keys())[0], list(key.values())[0]
                            os.system("setxkbmap -variant {}".format(self.parent.lilii_settings["keyboard_variant"][0]))

            self.keyLabel.keyboardInfo.emit(self.parent.lilii_settings["keyboard_model"][0],
                                            self.parent.lilii_settings["keyboard_layout"][0],
                                            self.parent.lilii_settings["keyboard_variant"][0])