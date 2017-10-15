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

from PyQt5.QtWidgets import (QDialog, QLabel, QComboBox, QVBoxLayout, QVBoxLayout, QDialogButtonBox,
                             QFormLayout, QLineEdit, QCheckBox, QSpinBox, QRadioButton)
from PyQt5.QtCore import Qt
import  os

def is_efi():
    return os.path.isdir("/sys/firmware/efi")

class DiskCreateWidget(QDialog):

    partition = None

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedSize(350, 300)
        self.setLayout(QVBoxLayout())

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight|Qt.AlignTop)
        self.layout().addLayout(form_layout)

        self.size_spin = QSpinBox()

        self.type_layout = QVBoxLayout()
        self.primary_radio = QRadioButton("Birincil")
        self.primary_radio.setChecked(True)
        self.type_layout.addWidget(self.primary_radio)
        self.extended_radio = QRadioButton("Genişletilmiş")
        self.type_layout.addWidget(self.extended_radio)

        self.location_layout = QVBoxLayout()
        self.start_radio = QRadioButton("Bu boşluğun başlangıcı")
        self.start_radio.setChecked(True)
        self.location_layout.addWidget(self.start_radio)
        self.end_radio = QRadioButton("Bu boşluğun sonu")
        self.location_layout.addWidget(self.end_radio)

        self.file_system_combo = QComboBox()
        self.file_system_combo.addItems(["ext4", "fat32", "ntfs", "exfat", "swap"])
        self.partition_label_line = QLineEdit()
        self.mount_point_combo = QComboBox()
        self.is_format_check = QCheckBox()

        form_layout.addRow(self.tr("Boyut:"), self.size_spin)
        form_layout.addRow(self.tr("Tür:"), self.type_layout)
        form_layout.addRow(self.tr("Location:"), self.location_layout)
        form_layout.addRow(self.tr("Olarak Kullan:"), self.file_system_combo)
        form_layout.addRow(self.tr("Etiket(İsteğe bağlı):"), self.partition_label_line)
        form_layout.addRow(self.tr("Bağlama Noktası:"), self.mount_point_combo)

        self.dialbutton = QDialogButtonBox()
        self.dialbutton.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel)
        self.layout().addWidget(self.dialbutton)

        self.dialbutton.button(QDialogButtonBox.Apply).setText(self.tr("Apply"))
        self.dialbutton.button(QDialogButtonBox.Cancel).setText(self.tr("Cancel"))

        self.dialbutton.accepted.connect(self.editAccept)
        self.dialbutton.rejected.connect(self.close)


    def editAccept(self):
        self.partition.setText(2, self.combobox.currentText())
        #self.parent.parent.lilii_settings[self.combobox.currentText()] = self.partition.text(0)
        #self.parent.partitionSelectControl()
        self.accept()

    def showEvent(self, event):
        self.setWindowTitle(self.tr("Disk Partition")+" - "+self.partition.text(0))
        self.mount_point_combo.addItem("/")
        self.mount_point_combo.addItem("/home")

        if is_efi():
            self.mount_point_combo.addItem("/boot/efi")

        else:
            self.mount_point_combo.addItem("/boot")