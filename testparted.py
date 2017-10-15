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
                             QApplication, QButtonGroup, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QProcess, pyqtSignal
from diskeditwidget import DiskEditWidget
from diskcreatewidget import DiskCreateWidget
import parted, os
from limelib.tools.settings import Settings


def disksList():
    return parted.getAllDevices()


def diskInfo(disk):
    try:
        return parted.Disk(disk)

    except parted.DiskLabelException:
        pass


def diskType(disk):
    try:
        return parted.Disk(disk).type.upper()

    except parted.DiskLabelException:
        return None

def mbToGB(size):
    if size < 1024:
        return str(size)+" MB"
    else:
        return str(int(size)//1024)+" GB"

def is_efi():
    return os.path.isdir("/sys/firmware/efi")

class PartitionWidget(QWidget):

    first_show = True
    selected_disk = diskInfo(disksList()[0])
    applyPage = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setLayout(QVBoxLayout())

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.label1 = QLabel()
        hlayout.addWidget(self.label1)

        # self.combo_box = QComboBox()
        # self.combo_box.setFixedWidth(400)
        # for disk in disksList():
        #     self.combo_box.addItem("{} - {} ({})".format(disk.model, mbToGB(disk.getSize()), disk.path))

        # hlayout.addWidget(self.combo_box)

        self.label2 = QPushButton()
        self.label2.setStyleSheet("border: none;")
        self.label2.setIcon(QIcon(":/images/disk.svg"))
        self.label2.setIconSize(QSize(20, 20))
        hlayout.addWidget(self.label2)

        self.resetButton = QPushButton()
        hlayout.addWidget(self.resetButton)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.treePartitionWidget = QTreeWidget()
        self.layout().addWidget(self.treePartitionWidget)

        self.header = self.treePartitionWidget.headerItem()

        self.treePartitionWidget.setColumnWidth(0, 150)
        self.treePartitionWidget.setColumnWidth(1, 150)
        self.treePartitionWidget.setColumnWidth(2, 150)
        self.treePartitionWidget.setColumnWidth(3, 100)
        self.treePartitionWidget.setColumnWidth(4, 50)
        self.treePartitionWidget.setColumnWidth(5, 100)
        self.treePartitionWidget.setColumnWidth(6, 100)


        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))

        self.createPartitionButton = QPushButton()
        hlayout.addWidget(self.createPartitionButton)

        self.editPartitionButton = QPushButton()
        hlayout.addWidget(self.editPartitionButton)

        self.deletePartitionButton = QPushButton()
        hlayout.addWidget(self.deletePartitionButton)

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

            hlayout.addWidget(self.combo_box2)

            hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Maximum))
            self.combo_box2.currentIndexChanged.connect(self.bootloaderDiskSelect)

        self.treePartitionWidget.itemClicked.connect(self.buttonState)
        self.editPartitionButton.clicked.connect(self.diskEditConnect)
        # self.combo_box.currentIndexChanged.connect(self.diskSelect)
        #self.deletePartitionButton.clicked.connect(self.diskPartitionClear)
        self.resetButton.clicked.connect(self.diskPartitionClear)
        self.createPartitionButton.clicked.connect(self.createPartition)
        self.deletePartitionButton.clicked.connect(self.partitionDelete)
        #self.parent.languageChanged.connect(self.retranslate)

        # self.diskPartitionList(diskInfo(disksList()[self.combo_box.currentIndex()]))

        self.diskPartitionList()
        self.retranslate()

    def retranslate(self):
        distro_name = Settings().value("distro_name")
        self.setWindowTitle(self.tr("Disk Partition"))
        self.label1.setText(self.tr("Select where the {} is going to be installed: ").format(distro_name))
        self.label2.setText("{}".format(diskType(disksList()[0]) or self.tr("Unknown")))
        self.resetButton.setText(self.tr("Reset"))
        self.header.setText(0, self.tr("Device"))
        self.header.setText(1, self.tr("File System"))
        self.header.setText(2, self.tr("Mount Point"))
        self.header.setText(3, self.tr("Label"))
        self.header.setText(4, self.tr("Format"))
        self.header.setText(5, self.tr("Size"))
        self.header.setText(6, self.tr("Used"))
        self.createPartitionButton.setText(self.tr("Create"))
        self.editPartitionButton.setText(self.tr("Edit"))
        self.deletePartitionButton.setText(self.tr("Delete"))
        self.bootLabel.setText(self.tr("Where to install the bootloader:"))

    def buttonState(self, item, column):
        if not isinstance(item.parent(), QTreeWidgetItem):
            self.createPartitionButton.setEnabled(False)
            self.editPartitionButton.setEnabled(False)
            self.deletePartitionButton.setEnabled(False)

        elif isinstance(item.parent(), QTreeWidgetItem) and item.text(0).startswith("/dev"):
            self.editPartitionButton.setEnabled(True)
            self.deletePartitionButton.setEnabled(True)
            self.createPartitionButton.setEnabled(False)

        else:
            self.createPartitionButton.setEnabled(True)
            self.editPartitionButton.setEnabled(False)
            self.deletePartitionButton.setEnabled(False)

    def bootloaderDiskSelect(self, index):
        pass#self.parent.lilii_settings["bootloader"] = disksList()[index].path

    def createPartition(self):
        if self.treePartitionWidget.selectedItems():
            select = self.treePartitionWidget.selectedItems()[0]
            if isinstance(select.parent(), QTreeWidgetItem):
                d = DiskCreateWidget(self)
                d.partition = select
                d.exec()

    def partitionDelete(self):
        if self.treePartitionWidget.selectedItems():
            select = self.treePartitionWidget.selectedItems()[0]
            if isinstance(select.parent(), QTreeWidgetItem):
                try:
                    print(select.parent().text(0))
                    disk = parted.Disk(parted.Device(select.parent().text(0)))

                    for partition in disk.partitions:
                        if partition.path == select.text(0):
                            print(partition.path)
                            #disk.deletePartition(partition)

                except parted.PartitionException as err:
                    print(err)

    def diskPartitionClear(self):
        for index in list(range(self.treePartitionWidget.topLevelItemCount())):
            item = self.treePartitionWidget.topLevelItem(index)
            item.setText(2, "")

        self.partitionSelectControl()

    def diskPartitionList(self):
        self.treePartitionWidget.clear()
        for device in parted.getAllDevices():
            top_item = QTreeWidgetItem(self.treePartitionWidget)
            top_item.setExpanded(True)
            top_item.setText(0, device.path)
            self.treePartitionWidget.addTopLevelItem(top_item)
            try:
                for partition in parted.Disk(device).partitions:
                    try:
                        part_item = QTreeWidgetItem(top_item)
                        part_item.setText(0, partition.path)
                        part_item.setText(1, partition.fileSystem.type)
                        part_item.setText(2, "")
                        part_item.setText(3, partition.name or "")
                        part_item.setText(4, "✔")
                        part_item.setText(5, mbToGB(partition.getSize()))

                    except AttributeError:
                        part_item = QTreeWidgetItem(top_item)
                        part_item.setText(0, partition.path)
                        part_item.setText(1, self.tr("Unknown"))
                        part_item.setText(2, "")
                        part_item.setText(3, partition.name or "")
                        part_item.setText(4, "✔")
                        part_item.setText(5, mbToGB(partition.getSize()))

            except parted.DiskLabelException as err:

                if is_efi():
                    disk = parted.freshDisk(device, "gpt")
                else:
                    disk = parted.freshDisk(device, "msdos")

                try:
                    disk.commit()
                except parted.IOException as err:
                    print(err)
                    self.diskPartitionList()


    def diskEditConnect(self):
        if self.treePartitionWidget.selectedItems():
            select = self.treePartitionWidget.selectedItems()[0]
            if isinstance(select.parent(), QTreeWidgetItem):
                disk = DiskEditWidget(self)
                disk.partition = select
                disk.exec_()


app = QApplication([])
w = PartitionWidget()
w.show()
app.exec_()