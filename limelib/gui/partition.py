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

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy,
                             QStackedWidget, QButtonGroup, QTreeWidget, QTreeWidgetItem, QRadioButton, QFormLayout,
                             QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, QProcess, pyqtSignal
from ..tools import *
from .widget.diskeditwidget import DiskEditWidget
import parted
from ..tools.settings import Settings


class PartitionWidget(QStackedWidget):

    applyPage = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        partitionI = PartitionWidgetI(self)
        partitionII = PartitionWidgetII(self)

        self.addWidget(partitionI)
        self.addWidget(partitionII)

        self.retranslate()

    def retranslate(self):
        self.setWindowTitle(self.tr("Disk Partition"))


class PartitionWidgetI(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        self.layout().addLayout(hbox)

        logo = QLabel()
        logo.setFixedSize(64, 64)
        logo.setScaledContents(True)
        logo.setPixmap(QPixmap(":/images/disk-delete.svg"))
        hbox.addWidget(logo)

        self.diskDeleteRadio = QRadioButton()
        self.diskDeleteRadio.setChecked(True)
        font = self.diskDeleteRadio.font()
        font.setBold(True)
        self.diskDeleteRadio.setFont(font)
        hbox.addWidget(self.diskDeleteRadio)

        form = QFormLayout()
        form.setContentsMargins(90, 0, 0, 0)
        self.layout().addLayout(form)

        self.warning_label = QLabel()
        form.addRow(self.warning_label)

        vbox = QVBoxLayout()
        form.addRow(vbox)

        self.cryptCheck = QCheckBox()
        vbox.addWidget(self.cryptCheck)
        self.crypt_label = QLabel()
        vbox.addWidget(self.crypt_label)

        vbox = QVBoxLayout()
        form.addRow(vbox)

        self.homeCheck = QCheckBox()
        vbox.addWidget(self.homeCheck)
        self.home_label = QLabel()
        vbox.addWidget(self.home_label)

        hbox = QHBoxLayout()
        self.layout().addLayout(hbox)

        logo = QLabel()
        logo.setFixedSize(64, 64)
        logo.setScaledContents(True)
        logo.setPixmap(QPixmap(":/images/manuel-partition.svg"))
        hbox.addWidget(logo)

        self.manuelRadio = QRadioButton()
        font = self.manuelRadio.font()
        font.setBold(True)
        self.manuelRadio.setFont(font)
        hbox.addWidget(self.manuelRadio)

        self.retranslate()

    def retranslate(self):
        distro = Settings().value("distro_name")
        self.diskDeleteRadio.setText(self.tr("Diski sil ve {} kur.").format(distro))
        self.warning_label.setText(self.tr("<font size=5>Uyarı: Bu seçenek diskinizdeki TÜM veriyi silecek!</font>"))
        self.cryptCheck.setText(self.tr("Yüksek güvenlik için bu kurulumu şifrele."))
        self.crypt_label.setText(self.tr("<font size=2><i>Bir sonraki adımda size şifreleme için parola sorulacak.</i></font>"))
        self.homeCheck.setText(self.tr("Ev dizini için farklı bir disk bölümü ayarlayın."))
        self.home_label.setText(self.tr("<font size=2><i>Bu seçenek /home dizinini farklı bir disk bölümüne ayarlayacaktır.</i></font>"))
        self.manuelRadio.setText(self.tr("{} nereye kurulacağını seç.").format(distro))


class PartitionWidgetII(QWidget):

    first_show = True
    selected_disk = diskInfo(disksList()[0])
    applyPage = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setLayout(QVBoxLayout())

        self.parent.parent.lilii_settings["/"] = None
        self.parent.parent.lilii_settings["/home"] = None

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.label1 = QLabel()
        hlayout.addWidget(self.label1)

        self.combo_box = QComboBox()
        self.combo_box.setFixedWidth(400)
        for disk in disksList():
            self.combo_box.addItem("{} - {} ({})".format(disk.model, mbToGB(disk.getSize()), disk.path))

        hlayout.addWidget(self.combo_box)

        self.label2 = QPushButton()
        self.label2.setStyleSheet("border: none;")
        self.label2.setIcon(QIcon(":/images/disk.svg"))
        self.label2.setIconSize(QSize(20, 20))
        hlayout.addWidget(self.label2)

        self.refreshButton = QPushButton()
        self.refreshButton.setIcon(QIcon(":/images/refresh.svg"))
        self.refreshButton.setIconSize(QSize(24, 24))
        hlayout.addWidget(self.refreshButton)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.treePartitionWidget = QTreeWidget()
        self.layout().addWidget(self.treePartitionWidget)

        self.header = self.treePartitionWidget.headerItem()

        self.treePartitionWidget.setColumnWidth(0, 450)
        self.treePartitionWidget.setColumnWidth(1, 150)
        self.treePartitionWidget.setColumnWidth(2, 200)
        self.treePartitionWidget.setColumnWidth(3, 100)


        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.editPartitionButton = QPushButton()
        hlayout.addWidget(self.editPartitionButton)

        self.zeroPartitionButton = QPushButton()
        hlayout.addWidget(self.zeroPartitionButton)

        self.bootLabel = QLabel()
        if not is_efi():
            hlayout = QHBoxLayout()
            self.layout().addLayout(hlayout)

            hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))
            hlayout.addWidget(self.bootLabel)

            self.combo_box2 = QComboBox()
            self.combo_box2.setFixedWidth(400)
            for disk in disksList():
                self.combo_box2.addItem("{} - {} ({})".format(disk.model, mbToGB(disk.getSize()), disk.path))

            self.parent.parent.lilii_settings["bootloader"] = disksList()[0].path
            hlayout.addWidget(self.combo_box2)

            hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))
            self.combo_box2.currentIndexChanged.connect(self.bootloaderDiskSelect)


            self.parent.parent.lilii_settings["/boot"] = None

        else:
            self.parent.parent.lilii_settings["/boot/efi"] = None

        self.editPartitionButton.clicked.connect(self.diskConnect)
        self.combo_box.currentIndexChanged.connect(self.diskSelect)
        self.zeroPartitionButton.clicked.connect(self.diskPartitionClear)
        self.refreshButton.clicked.connect(self.diskRefresh)
        self.parent.parent.languageChanged.connect(self.retranslate)

        self.diskPartitionList(diskInfo(disksList()[self.combo_box.currentIndex()]))

        self.retranslate()

    def retranslate(self):
        distro_name = Settings().value("distro_name")
        self.label1.setText(self.tr("Select where the {} is going to be installed: ").format(distro_name))
        self.label2.setText("{}".format(diskType(disksList()[0]) or self.tr("Unknown")))
        self.refreshButton.setToolTip(self.tr("Refresh disk information"))
        self.header.setText(0, self.tr("Disk Part"))
        self.header.setText(1, self.tr("File System"))
        self.header.setText(2, self.tr("Mount Point"))
        self.header.setText(3, self.tr("Size"))
        self.editPartitionButton.setText(self.tr("Edit"))
        self.zeroPartitionButton.setText(self.tr("Reset"))
        self.bootLabel.setText(self.tr("Where to install the bootloader:"))

    def diskSelect(self, index):
        self.label2.setText("{}".format(diskType(disksList()[index])))
        self.selected_disk = diskInfo(disksList()[0])
        self.diskPartitionList(diskInfo(disksList()[self.combo_box.currentIndex()]))

    def diskRefresh(self):
        self.diskPartitionList(diskInfo(disksList()[self.combo_box.currentIndex()]))

    def bootloaderDiskSelect(self, index):
        self.parent.lilii_settings["bootloader"] = disksList()[index].path

    def diskPartitionClear(self):
        for index in list(range(self.treePartitionWidget.topLevelItemCount())):
            item = self.treePartitionWidget.topLevelItem(index)
            item.setText(2, "")

        self.parent.lilii_settings["/"] = None
        self.parent.lilii_settings["/home"] = None

        if is_efi():
            self.parent.lilii_settings["/boot/efi"] = None

        else:
            self.parent.lilii_settings["/boot"] = None

        self.partitionSelectControl()

    def diskPartitionList(self, disk):
        self.treePartitionWidget.clear()
        try:
            for partition in disk.partitions:
                try:
                    part_item = QTreeWidgetItem()
                    part_item.setText(0, partition.path)
                    part_item.setText(1, partition.fileSystem.type)
                    part_item.setText(2, "")
                    part_item.setText(3, mbToGB(partition.getSize()))
                    self.treePartitionWidget.addTopLevelItem(part_item)

                except AttributeError:
                    part_item = QTreeWidgetItem()
                    part_item.setText(0, partition.path)
                    part_item.setText(1, self.tr("Unknown"))
                    part_item.setText(2, "")
                    part_item.setText(3, mbToGB(partition.getSize()))
                    self.treePartitionWidget.addTopLevelItem(part_item)

        except (parted.DiskLabelException, AttributeError):
            part_item = QTreeWidgetItem()
            part_item.setText(0, self.tr("Partition table not Found"))
            self.treePartitionWidget.addTopLevelItem(part_item)


    def diskConnect(self):
        if self.treePartitionWidget.selectedItems():
            item = self.treePartitionWidget.selectedItems()[0]
            disk = DiskEditWidget(self)
            disk.partition = item
            disk.exec_()


    def showEvent(self, event):
        if self.first_show:
            QProcess.startDetached("sudo gparted")
            self.first_show = False

        self.partitionSelectControl()

    def partitionSelectControl(self):
        if self.parent.lilii_settings["/"] != None:
            if is_efi() and self.parent.lilii_settings["/boot/efi"] != None:
                self.applyPage.emit(True)

            elif not is_efi():
                self.applyPage.emit(True)

        else:
            self.applyPage.emit(False)