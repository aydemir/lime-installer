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

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QToolButton, QCheckBox, QFileDialog,
                             QSizePolicy, QSpacerItem)
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QDir, QTimer
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture, QCameraInfo
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PIL import Image, ImageQt
from ..tools import imageCrop, avatarCreate

class CustomToolButton(QToolButton):

    enter_icon = None
    leave_icon = None

    def setEnterIcon(self, QIcon):
        self.enter_icon = QIcon

    def setLeaveIcon(self, QIcon):
        self.leave_icon = QIcon

    def enterEvent(self, event):
        self.setIcon(self.enter_icon)

    def leaveEvent(self, event):
        self.setIcon(self.leave_icon)


class UserWidget(QWidget):

    host_name = None
    full_name = None
    user_name = None
    passwd = None
    repasswd = None
    rpasswd = None
    rrepasswd = None

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("QToolButton {border: none;}")
        self.setLayout(QHBoxLayout())

        left_layout = QVBoxLayout()
        self.layout().addLayout(left_layout)

        self.name_label = QLabel()
        left_layout.addWidget(self.name_label)

        name_layout = QHBoxLayout()
        left_layout.addLayout(name_layout)

        self.name_line = QLineEdit()
        self.name_line.setFixedWidth(450)
        name_layout.addWidget(self.name_line)

        self.name_icon = QLabel()
        self.name_icon.setFixedSize(24, 24)
        self.name_icon.setScaledContents(True)
        name_layout.addWidget(self.name_icon)

        self.user_label = QLabel()
        left_layout.addWidget(self.user_label)

        user_layout = QHBoxLayout()
        left_layout.addLayout(user_layout)

        self.user_line = QLineEdit()
        user_layout.addWidget(self.user_line)

        self.user_icon = QLabel()
        self.user_icon.setScaledContents(True)
        self.user_icon.setFixedSize(24, 24)
        user_layout.addWidget(self.user_icon)

        self.host_label = QLabel()
        left_layout.addWidget(self.host_label)

        host_layout = QHBoxLayout()
        left_layout.addLayout(host_layout)

        self.host_line = QLineEdit()
        host_layout.addWidget(self.host_line)

        self.host_icon = QLabel()
        self.host_icon.setFixedSize(24, 24)
        self.host_icon.setScaledContents(True)
        host_layout.addWidget(self.host_icon)

        self.pass_label = QLabel()
        left_layout.addWidget(self.pass_label)

        pass_layout = QHBoxLayout()
        left_layout.addLayout(pass_layout)

        self.pass_line = QLineEdit()
        self.pass_line.setEchoMode(QLineEdit.Password)
        pass_layout.addWidget(self.pass_line)

        self.pass_icon = QLabel()
        self.pass_icon.setScaledContents(True)
        self.pass_icon.setFixedSize(24, 24)
        pass_layout.addWidget(self.pass_icon)

        repass_layout = QHBoxLayout()
        left_layout.addLayout(repass_layout)

        self.repass_line = QLineEdit()
        self.repass_line.setEchoMode(QLineEdit.Password)
        repass_layout.addWidget(self.repass_line)

        self.repass_icon = QLabel()
        self.repass_icon.setScaledContents(True)
        self.repass_icon.setFixedSize(24, 24)
        repass_layout.addWidget(self.repass_icon)

        self.auto_box = QCheckBox()
        self.auto_box.setChecked(True)
        left_layout.addWidget(self.auto_box)

        self.root_box = QCheckBox()
        self.root_box.setChecked(True)
        left_layout.addWidget(self.root_box)

        rpass_layout = QHBoxLayout()
        left_layout.addLayout(rpass_layout)

        rpass_layout.addSpacerItem(QSpacerItem(0, 40, QSizePolicy.Maximum, QSizePolicy.Expanding))

        self.rpass_line = QLineEdit()
        self.rpass_line.hide()
        self.rpass_line.setEchoMode(QLineEdit.Password)
        rpass_layout.addWidget(self.rpass_line)

        self.rpass_icon = QLabel()
        self.rpass_icon.hide()
        self.rpass_icon.setScaledContents(True)
        self.rpass_icon.setFixedSize(24, 24)
        rpass_layout.addWidget(self.rpass_icon)

        rrepass_layout = QHBoxLayout()
        left_layout.addLayout(rrepass_layout)

        self.rrepass_line = QLineEdit()
        self.rrepass_line.hide()
        self.rrepass_line.setEchoMode(QLineEdit.Password)
        rrepass_layout.addWidget(self.rrepass_line)

        self.rrepass_icon = QLabel()
        self.rrepass_icon.hide()
        self.rrepass_icon.setScaledContents(True)
        self.rrepass_icon.setFixedSize(24, 24)
        rrepass_layout.addWidget(self.rrepass_icon)

        left_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Maximum, QSizePolicy.Expanding))

        self.layout().addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        right_layout = QVBoxLayout()
        self.layout().addLayout(right_layout)

        ######## Camera

        self.cameras = QCameraInfo.availableCameras()

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(192, 192)
        self.photo_label.setScaledContents(True)
        self.photo_label.setPixmap(QPixmap(":/images/user-avatar.svg"))
        self.parent.lilii_settings["avatar"] = None
        right_layout.addWidget(self.photo_label)

        if len(self.cameras):
            self.camera = QCamera(self.cameras[0])
            self.camera.setCaptureMode(QCamera.CaptureStillImage)

            self.image_capture = QCameraImageCapture(self.camera)
            self.image_capture.imageSaved.connect(self.imageConvert)

        button_layout = QHBoxLayout()
        right_layout.addLayout(button_layout)

        self.take_photo = CustomToolButton()
        self.take_photo.setEnabled(len(self.cameras))
        self.take_photo.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.take_photo.setIconSize(QSize(32, 32))
        self.take_photo.setIcon(QIcon(":/images/camera.svg"))
        self.take_photo.setEnterIcon(QIcon(":/images/camera-red.svg"))
        self.take_photo.setLeaveIcon(QIcon(":/images/camera.svg"))
        button_layout.addWidget(self.take_photo)

        self.retake_photo = CustomToolButton()
        self.retake_photo.hide()
        self.retake_photo.setEnabled(len(self.cameras))
        self.retake_photo.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.retake_photo.setIconSize(QSize(32, 32))
        self.retake_photo.setIcon(QIcon(":/images/camera.svg"))
        self.retake_photo.setEnterIcon(QIcon(":/images/camera-red.svg"))
        self.retake_photo.setLeaveIcon(QIcon(":/images/camera.svg"))
        button_layout.addWidget(self.retake_photo)

        self.select_photo = CustomToolButton()
        self.select_photo.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.select_photo.setIconSize(QSize(32, 32))
        self.select_photo.setIcon(QIcon(":/images/users.svg"))
        self.select_photo.setLeaveIcon(QIcon(":/images/users.svg"))
        self.select_photo.setEnterIcon(QIcon(":/images/users-red.svg"))
        button_layout.addWidget(self.select_photo)

        self.layout().addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.parent.lilii_settings["auto_login"] = self.auto_box.isChecked()
        self.parent.lilii_settings["root_user"] = self.root_box.isChecked()

        self.auto_box.toggled.connect(self.autoControl)
        self.root_box.toggled.connect(self.rootControl)
        self.host_line.textChanged.connect(self.hostnameControl)
        self.name_line.textChanged.connect(self.fullnameControl)
        self.name_line.textChanged.connect(self.fullnameToUsername)
        self.user_line.textChanged.connect(self.usernameControl)
        self.pass_line.textChanged.connect(self.passwordControl)
        self.repass_line.textChanged.connect(self.repasswordControl)
        self.rpass_line.textChanged.connect(self.rpasswordControl)
        self.rrepass_line.textChanged.connect(self.rrepasswordControl)

        self.root_box.toggled.connect(self.lineEditsControl)
        self.host_line.textChanged.connect(self.lineEditsControl)
        self.name_line.textChanged.connect(self.lineEditsControl)
        self.user_line.textChanged.connect(self.lineEditsControl)
        self.pass_line.textChanged.connect(self.lineEditsControl)
        self.repass_line.textChanged.connect(self.lineEditsControl)
        self.rpass_line.textChanged.connect(self.lineEditsControl)
        self.rrepass_line.textChanged.connect(self.lineEditsControl)

        self.select_photo.clicked.connect(self.selectPhoto)
        self.take_photo.clicked.connect(self.takePhoto)
        self.retake_photo.clicked.connect(self.retakePhoto)
        self.parent.languageChanged.connect(self.retranslate)

        self.image_timer = QTimer(self)
        self.image_timer.timeout.connect(self.cameraView)

        self.retranslate()

    def retranslate(self):
        self.select_photo.setText(self.tr("Select Photo"))
        self.retake_photo.setText(self.tr("Retake Photo"))
        self.take_photo.setText(self.tr("Take Photo"))
        self.rrepass_line.setPlaceholderText(self.tr("Root Repassword"))
        self.rpass_line.setPlaceholderText(self.tr("Root Password"))
        self.root_box.setText(self.tr("Should the administrator and the user use the same password?"))
        self.auto_box.setText(self.tr("Sign in without password."))
        self.repass_line.setPlaceholderText(self.tr("Repassword"))
        self.pass_line.setPlaceholderText(self.tr("Password"))
        self.pass_label.setText(self.tr("Enter your user password."))
        self.host_line.setPlaceholderText(self.tr("Hostname"))
        self.host_label.setText(self.tr("What should this computer be named?"))
        self.user_line.setPlaceholderText(self.tr("Username"))
        self.user_label.setText(self.tr("Username to sign in?"))
        self.name_line.setPlaceholderText(self.tr("Fullname"))
        self.name_label.setText(self.tr("What is your name?"))
        self.setWindowTitle(self.tr("User Creation"))

    def showEvent(self, event):
        self.lineEditsControl()
        if len(self.cameras):
            self.retakePhoto()

    def autoControl(self):
        self.parent.lilii_settings["auto_login"] = self.auto_box.isChecked()

    def rootControl(self):
        self.parent.lilii_settings["root_user"] = self.root_box.isChecked()
        if not self.root_box.isChecked():
            self.rpass_line.show()
            self.rpass_icon.show()
            self.rrepass_line.show()
            self.rrepass_icon.show()
        else:
            self.rpass_line.hide()
            self.rpass_icon.hide()
            self.rrepass_line.hide()
            self.rrepass_icon.hide()

    def hostnameControl(self, hostname):
        if hostname.isalnum() and len(hostname) > 3:
            self.host_name = True
            self.host_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.host_name = False
            self.host_icon.setPixmap(QPixmap(":/images/xxx.svg"))

    def fullnameControl(self, fullname):
        if len(fullname) > 2:
            self.full_name = True
            self.name_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.full_name = False
            self.name_icon.setPixmap(QPixmap(":/images/xxx.svg"))

    def usernameControl(self, username):
        if username.isalnum() and len(username) > 3:
            self.user_name = True
            self.user_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.user_name = False
            self.user_icon.setPixmap(QPixmap(":/images/xxx.svg"))

    def fullnameToUsername(self, text):
        self.user_line.setText(text.lower().replace(" ", ""))

    def passwordControl(self, passwd):
        if len(passwd) > 5:
            self.passwd = True
            self.pass_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.passwd = False
            self.pass_icon.setPixmap(QPixmap(":/images/xxx.svg"))

        if passwd == self.repass_line.text():
            self.repasswd = True
            self.repass_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.repasswd = False
            self.repass_icon.setPixmap(QPixmap(":/images/xxx.svg"))

    def repasswordControl(self, repasswd):
        if repasswd == self.pass_line.text():
            self.repasswd = True
            self.repass_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.repasswd = False
            self.repass_icon.setPixmap(QPixmap(":/images/xxx.svg"))

    def rpasswordControl(self, passwd):
        if len(passwd) > 5:
            self.rpasswd = True
            self.rpass_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.rpasswd = False
            self.rpass_icon.setPixmap(QPixmap(":/images/xxx.svg"))

        if passwd == self.rrepass_line.text():
            self.rrepasswd = True
            self.rrepass_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.rrepasswd = False
            self.rrepass_icon.setPixmap(QPixmap(":/images/xxx.svg"))

    def rrepasswordControl(self, repasswd):
        if repasswd == self.rpass_line.text():
            self.rrepasswd = True
            self.rrepass_icon.setPixmap(QPixmap(":/images/apply.svg"))
        else:
            self.rrepasswd = False
            self.rrepass_icon.setPixmap(QPixmap(":/images/xxx.svg"))

    applyPage = pyqtSignal(bool)

    def lineEditsControl(self):
        if not self.root_box.isChecked():
            if self.host_name and self.full_name and self.user_name and self.passwd and self.repasswd and self.rpasswd \
                                                                                                    and self.rrepasswd:

                self.parent.lilii_settings["root_pass"] = self.rpass_line.text()
                self.applyPage.emit(True)

                self.parent.lilii_settings["fullname"] = self.name_line.text()
                self.parent.lilii_settings["username"] = self.user_line.text()
                self.parent.lilii_settings["password"] = self.pass_line.text()
                self.parent.lilii_settings["hostname"] = self.host_line.text()

            else:
                self.applyPage.emit(False)

        elif self.host_name and self.full_name and self.user_name and self.passwd and self.repasswd:
            self.parent.lilii_settings["fullname"] = self.name_line.text()
            self.parent.lilii_settings["username"] = self.user_line.text()
            self.parent.lilii_settings["password"] = self.pass_line.text()
            self.parent.lilii_settings["hostname"] = self.host_line.text()
            self.applyPage.emit(True)

        else:
            self.applyPage.emit(False)

    def selectPhoto(self):
        avatar_path = QDir.homePath() + "/.face.icon"
        file_path = QFileDialog.getOpenFileName(self, self.tr("Choose a user icon"), QDir.homePath(), "Image (*.png *.jpg)")

        if file_path[0]:
            image = Image.open(file_path[0])
            crop_image = image.crop(imageCrop(image))
            new_image = avatarCreate(crop_image)
            new_image.save(avatar_path, "PNG")
            self.photo_label.setPixmap(QPixmap(avatar_path))

            self.parent.lilii_settings["avatar"] = True

    def takePhoto(self):
        self.take_photo.hide()
        self.retake_photo.show()

        self.parent.lilii_settings["avatar"] = True
        self.image_timer.stop()
        self.camera.stop()

    def retakePhoto(self):
        self.retake_photo.hide()
        self.take_photo.show()
        self.camera.start()
        self.parent.lilii_settings["avatar"] = False
        self.image_timer.start(1000//30)

    def cameraView(self):
        self.image_capture.capture("/tmp/frame")

    def imageConvert(self, id, image):
        path = QDir.homePath() + "/.face.icon"
        im = Image.open(image)
        crop_image = im.crop(imageCrop(im))
        new_image = avatarCreate(crop_image)
        new_image.save(path, "PNG")
        self.photo_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(new_image)))