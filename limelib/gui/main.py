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

from PyQt5.QtWidgets import (QWidget, QApplication, QStackedWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy,
                             QPushButton, QDesktopWidget, QLabel, qApp, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QObject, QTranslator, QLocale, pyqtSignal, QFile
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from .welcome import WelcomeWidget
from .finish import FinishWidget
from .install import InstallWidget
from .keyboard import KeyboardWidget
from .location import LocationWidget
from .partition import PartitionWidget
from .summary import SummaryWidget
from .user import UserWidget
from .widget.lprogressbar import LProgressBar

import sys
from .. import limerc
from ..tools.settings import Settings


class SingleApplication(QObject):

    newInstance = pyqtSignal()
    urlPost = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.mServer = QLocalServer()
        self.mServer.newConnection.connect(self.newConnection)

    def listen(self, client):
        self.mServer.removeServer(client)
        self.mServer.listen(client)
        print(self.mServer.errorString())

    def hasPrevious(self, name, args):
        socket = QLocalSocket()
        socket.connectToServer(name, QLocalSocket.ReadWrite)
        if socket.waitForConnected():
            if len(args) > 1:
                socket.write(args[1])

            socket.flush()
            return True
        return False

    def newConnection(self):
        self.newInstance.emit()
        self.mSocket = self.mServer.nextPendingConnection()
        self.mSocket.readyRead.connect(self.readyRead)

    def readyRead(self):
        self.urlPost.emit(str(self.mSocket.readAll()))
        self.mSocket.close()


class TitleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedHeight(90)
        self.setLayout(QHBoxLayout())
        self.layout().addSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.logo = QLabel()
        self.logo.setFixedSize(96, 96)
        self.logo.setScaledContents(True)
        self.logo.setPixmap(QPixmap(":/images/lime-logo.svg"))
        self.layout().addWidget(self.logo)

        self.layout().addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.lprogressBar = LProgressBar(self.parent)
        self.layout().addWidget(self.lprogressBar)

        self.parent.currentChanged.connect(self.lprogressBar.setIndex)


class FooterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedHeight(35)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.cancelButton = QPushButton()
        self.cancelButton.setIcon(QIcon(":/images/cancel.svg"))
        self.layout().addWidget(self.cancelButton)

        self.layout().addItem(QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Maximum))

        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon(":/images/back.svg"))
        self.layout().addWidget(self.backButton)

        self.continueButton = QPushButton()
        self.continueButton.setIcon(QIcon(":/images/forward.svg"))
        self.layout().addWidget(self.continueButton)

        self.applyButton = QPushButton()
        self.applyButton.setIcon(QIcon(":/images/apply.svg"))
        self.layout().addWidget(self.continueButton)

        self.parent.currentChanged.connect(self.buttonStatus)
        self.continueButton.clicked.connect(self.nextWidget)
        self.backButton.clicked.connect(self.proviousWidget)
        self.cancelButton.clicked.connect(self.cancelQuestion)

        self.retranslate()

        if self.parent.currentIndex() == 0:
            self.backButton.setDisabled(True)

    def retranslate(self):
        self.cancelButton.setText(self.tr("Cancel"))
        self.backButton.setText(self.tr("Back"))
        self.continueButton.setText(self.tr("Continue"))
        self.applyButton.setText(self.tr("Finish"))

    def cancelQuestion(self):
        self.questionBox = QMessageBox()
        self.questionBox.setIcon(QMessageBox.Question)
        self.questionBox.setWindowTitle(self.tr("Do you want to quit?"))
        distro_name = Settings().value("distro_name")
        self.questionBox.setText(self.tr("Do you want to quit from {} System Installer?").format(distro_name))

        yes = self.questionBox.addButton(self.tr("Yes"), QMessageBox.ActionRole)
        no = self.questionBox.addButton(self.tr("No"), QMessageBox.NoRole)
        self.questionBox.setDefaultButton(yes)
        self.questionBox.exec()

        if self.questionBox.clickedButton() == yes:
            qApp.quit()

    def buttonStatus(self, current):
        self.backButton.setEnabled(True)
        if current == 0:
            self.backButton.setDisabled(True)

        if current+1 == self.parent.count():
            self.continueButton.setText(self.tr("Exit"))
            self.continueButton.setIcon(QIcon(":/images/exit.svg"))
            self.continueButton.clicked.connect(qApp.quit)
            self.backButton.setDisabled(True)
            self.cancelButton.setDisabled(True)

        if current == 6:
            self.backButton.setDisabled(True)
            self.cancelButton.setDisabled(True)

    def nextWidget(self):
        if self.parent.currentIndex() == 5:
            self.warningBox = QMessageBox()
            self.warningBox.setIcon(QMessageBox.Warning)
            self.warningBox.setWindowTitle(self.tr("Be Carefull!"))
            self.warningBox.setText(self.tr("Setup is going to start in the next step and "
                                    "stated steps are going to be applied to your system."))

            yes = self.warningBox.addButton(self.tr("Yes"), QMessageBox.ActionRole)
            no = self.warningBox.addButton(self.tr("No"), QMessageBox.NoRole)
            self.warningBox.setDefaultButton(yes)
            self.warningBox.exec()

            if self.warningBox.clickedButton() == yes:
                self.parent.setCurrentIndex(self.parent.currentIndex() + 1)

        else:
            self.parent.setCurrentIndex(self.parent.currentIndex()+1)

    def proviousWidget(self):
        self.parent.setCurrentIndex(self.parent.currentIndex() - 1)

        if self.parent.currentIndex() == 4 or 3:
            self.continueButton.setEnabled(True)


class MainWindow(QWidget):

    lilii_settings = {}
    languageChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.setFixedSize(950, 640)
        self.setWindowIcon(QIcon(":/images/lime-installer.svg"))
        self.setWindowFlags(Qt.WindowTitleHint|Qt.WindowMinimizeButtonHint) #Qt.WindowStaysOnTopHint

        x, y = ((QDesktopWidget().width()-self.width())//2,
               (QDesktopWidget().availableGeometry().height()-self.height())//2)
        self.move(x, y)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.wizardWidget = QStackedWidget()
        self.wizardWidget.addWidget(WelcomeWidget(self))
        self.wizardWidget.addWidget(LocationWidget(self))
        self.wizardWidget.addWidget(KeyboardWidget(self))
        self.wizardWidget.addWidget(PartitionWidget(self))
        self.wizardWidget.addWidget(UserWidget(self))
        self.wizardWidget.addWidget(SummaryWidget(self))
        self.wizardWidget.addWidget(InstallWidget(self))
        self.wizardWidget.addWidget(FinishWidget(self))

        self.titleWidget = TitleWidget(self.wizardWidget)
        self.footerWidget = FooterWidget(self.wizardWidget)

        layout.addWidget(self.titleWidget)
        layout.addWidget(self.wizardWidget)
        layout.addWidget(self.footerWidget)

        self.footerWidget.cancelButton.clicked.connect(self.close)
        self.wizardWidget.widget(4).applyPage.connect(self.footerWidget.continueButton.setEnabled)
        self.wizardWidget.widget(3).applyPage.connect(self.footerWidget.continueButton.setEnabled)
        self.wizardWidget.widget(6).applyPage.connect(self.footerWidget.continueButton.setEnabled)
        self.languageChanged.connect(self.retranslate)
        self.languageChanged.connect(self.footerWidget.retranslate)

        self.retranslate()

    def retranslate(self):
        self.setWindowTitle(self.tr("{} System Installer").format(Settings().value("distro_name")))


    def closeEvent(self, event):
        if not qApp.quitOnLastWindowClosed():
            event.ignore()

        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationVersion("1.0 Beta")
    locale = QLocale.system().name()
    translator = QTranslator(app)
    path = "/usr/share/lime-installer/languages/{}.qm".format(locale)
    if not QFile().exists(path):
        path = "languages/{}.qm".format(locale)
    translator.load(path)
    app.installTranslator(translator)

    single = SingleApplication()
    if single.hasPrevious("lime-installer", app.arguments()):
        return False

    single.listen("lime-installer")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())