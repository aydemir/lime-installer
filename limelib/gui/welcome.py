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

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, qApp, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QSize, QTranslator, QLocale, QUrl, QFile


class WelcomeWidget(QWidget):

    lang_list = {"ca_ES.UTF-8" : "Català", "de_DE.UTF-8" : "Deutsch", "en_US.UTF-8" : "English (US)", "es_ES.UTF-8" : "Español",
                 "fr_FR.UTF-8" : "Français", "hu.UTF-8" : "Magyar", "it_IT.UTF-8" : "Italiano", "nl_NL.UTF-8" : "Nederlands",
                 "pl.UTF-8" : "Polski", "pt_BR.UTF-8" : "Português (Brasil)", "ru_RU.UTF-8" : "Pусский",
                 "sv_SE.UTF-8" : "Svenska", "tr_TR.UTF-8" : "Türkçe"}

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        self.titleLabel = QLabel()
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.titleLabel)

        self.descLabel = QLabel()
        self.descLabel.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.descLabel)

        lLayout = QHBoxLayout()
        lLayout.setAlignment(Qt.AlignCenter)
        self.layout().addLayout(lLayout)

        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap(":/images/welcome.svg"))
        imageLabel.setScaledContents(True)
        imageLabel.setFixedSize(256, 256)
        lLayout.addWidget(imageLabel)

        langLayout = QHBoxLayout()
        langLayout.setAlignment(Qt.AlignCenter)
        self.layout().addLayout(langLayout)

        self.langLabel = QLabel()
        langLayout.addWidget(self.langLabel)

        langComboBox = QComboBox()
        langComboBox.setFixedWidth(250)
        langLayout.addWidget(langComboBox)

        linkLayout = QHBoxLayout()
        linkLayout.setAlignment(Qt.AlignCenter)
        self.layout().addLayout(linkLayout)

        self.aboutButton = QPushButton()
        self.aboutButton.setFlat(True)
        self.aboutButton.setIcon(QIcon(":/images/about.svg"))
        self.aboutButton.setIconSize(QSize(18, 18))
        linkLayout.addWidget(self.aboutButton)

        self.bugButton = QPushButton()
        self.bugButton.setFlat(True)
        self.bugButton.setIcon(QIcon(":/images/bug.svg"))
        self.bugButton.setIconSize(QSize(18, 18))
        linkLayout.addWidget(self.bugButton)

        self.releaseButton = QPushButton()
        self.releaseButton.setFlat(True)
        self.releaseButton.setIcon(QIcon(":/images/release-note.svg"))
        self.releaseButton.setIconSize(QSize(18, 18))
        linkLayout.addWidget(self.releaseButton)

        langComboBox.addItems(self.lang_list.values())

        for k, v in self.lang_list.items():
            if QLocale.system().name()+".UTF-8" == k:
                langComboBox.setCurrentText(v)
                self.parent.lilii_settings["lang"] = k

        langComboBox.currentTextChanged.connect(self.langSelect)
        self.aboutButton.clicked.connect(self.aboutDialog)
        self.bugButton.clicked.connect(self.bugAdressConnect)
        self.releaseButton.clicked.connect(self.releaseInfoConnect)
        self.parent.languageChanged.connect(self.retranslate)

        self.retranslate()

    def retranslate(self):
        self.setWindowTitle(self.tr("Welcome"))
        self.titleLabel.setText(self.tr("<h1>Welcome to Lime GNU/Linux System Installer.</h1>"))
        self.descLabel.setText(self.tr(
            "This program is going to ask you some questions and then will install the Lime GNU/Linux to your device."))
        self.langLabel.setText(self.tr("Language:"))
        self.aboutButton.setText(self.tr("About"))
        self.bugButton.setText(self.tr("Found Bug"))
        self.releaseButton.setText(self.tr("Release Notes"))


    def langSelect(self, lang):
        for k, v in self.lang_list.items():
            if lang == v:
                self.parent.lilii_settings["lang"] = k
                translator = QTranslator(qApp)
                path = "/usr/share/lime-installer/languages/{}.qm".format(k.split(".")[0])
                if QFile().exists(path):
                    translator.load(path)
                else:
                    translator.load("languages/{}.qm".format(k.split(".")[0]))
                qApp.installTranslator(translator)
                self.parent.languageChanged.emit()

    def aboutDialog(self):
        self.aboutBox = QMessageBox()
        self.aboutBox.setWindowTitle(self.tr("About Lime Installer"))
        self.aboutBox.setText(self.tr("<h1>Lime Installer {}</h1>"
                                      "<b>System installer for Lime GNU/Linux</b>"
                                      "<p>Copyright 2017 Metehan Ozbek - <b>metehan@limelinux.com</b><br>"
                                      "Thanks to: Fatih Kaya - <b>trlinux41@gmail.com</b></p>").format(
                                      qApp.applicationVersion()))
        self.aboutBox.exec_()

    def bugAdressConnect(self):
        QDesktopServices.openUrl(QUrl("https://github.com/lime-installer/lime-installer/issues"))

    def releaseInfoConnect(self):
        QDesktopServices.openUrl(QUrl("http://limelinux.com/limelinux-indir.html"))