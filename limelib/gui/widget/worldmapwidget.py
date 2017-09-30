from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QPoint, QFile, pyqtSignal
import json

class WorldMapWidget(QWidget):

    zone = pyqtSignal(str, str)
    zoneName = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedSize(900, 376)
        self.world_image = QPixmap(":/images/locale/world.png")
        self.pin_image = QPixmap(":/images/locale/pin.png")
        self.pin_point = QPoint(-50, -50)


        self.coordinat_to_position = {}
        self.coordinat_list = None

        self.coordinat_path = "data/coordinates.json"
        if QFile().exists(self.coordinat_path):
            self.coordinat_list = json.loads(open(self.coordinat_path).read())

        else:
            self.coordinat_list = json.loads(open("/usr/share/lime-installer/"+self.coordinat_path).read())


        for zone, coordinats in self.coordinat_list.items():
            pos = self.locationToPosition(coordinats[1], coordinats[0], zone)
            self.coordinat_to_position[pos[0]] = pos[1]

        self.zoneName.connect(self.pinPush)

    def search(self, x, y):
        deger = 1000
        returner = ()
        for i in list(self.coordinat_to_position.keys()):
            deger_ = (i[0]-x)**2 + (i[1]-y)**2
            if deger_ < deger:
                deger = deger_
                returner = (i[0],i[1])

        return returner

    def locationToPosition(self, longitude, latitude, time_zone=""):
        height = 450 #orjinalindeki yükseklik. antartikayı kesince hesaplamada bu baz alınacak.
        x = (self.width()/2)*(longitude/180)+(self.width()/2)
        y = (height/2)-((height/2)*(latitude/90))
        return ((x, y), time_zone)

    def mousePressEvent(self, event):
        self.pin_point.setX(event.x()-(self.pin_image.width()//2))
        self.pin_point.setY(event.y()-(self.pin_image.height()//2))
        zone = self.search(event.x(), event.y())
        if len(zone):
            a = self.coordinat_to_position[zone].split("/")
            b = "/".join(a[1:])
            self.zone.emit(a[0], b)
        self.update()

    def pinPush(self, zone_name):
        pos = self.coordinat_list[zone_name]
        coordinat = self.locationToPosition(pos[-1], pos[0])
        self.pin_point.setX(coordinat[0][0] - (self.pin_image.width() // 2))
        self.pin_point.setY(coordinat[0][1] - (self.pin_image.height() // 2))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform|QPainter.Antialiasing|QPainter.HighQualityAntialiasing)

        painter.drawPixmap(QPoint(0, 0), self.world_image)
        painter.drawPixmap(self.pin_point, self.pin_image)