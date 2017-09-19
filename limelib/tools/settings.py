from PyQt5.QtCore import QSettings, QFile


def Settings():
    file_path = "/usr/share/lime-installer/distro_custom.conf"
    if QFile().exists(file_path):
        return QSettings(file_path, QSettings.IniFormat)
    else:
        return QSettings("distro_custom.conf", QSettings.IniFormat)