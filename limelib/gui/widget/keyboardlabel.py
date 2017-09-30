from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import QPoint, pyqtSignal
import subprocess


keyboard_model = {
"pc104" : [
    [0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd],
    [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x2b],
    [0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28],
    [0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35]
],

"pc105" : [
    [0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd],
    [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b],
    [0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2b],
    [0x56, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35]
],

"pc106" : [
    [0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe],
    [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b],
    [0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29],
    [0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36]
]
}


class KeyboardLabel(QLabel):

    keyboardInfo = pyqtSignal(str, str, str) # model, layout, variant = pc105, tr, f

    is_paint = False
    keymap = None
    keyboard_model = None

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setFixedSize(900, 253)
        self.keyboard_image = QPixmap(":/images/keyboard.png")


        self.keyboardInfo.connect(self.proc)

    def proc(self, model, layout, variant):
        if model in keyboard_model:
            self.is_paint = True
            self.keymap = self.unicodeToString(model, layout, variant)
            self.keyboard_model = model
        else:
            self.is_paint = False

        self.update()

    def unicodeToString(self, model, layout, variant=""):
        keycodes = {}
        keymap_command = subprocess.Popen(["ckbcomp", "-model", model, "-layout", layout, "-variant", variant],
                               stdout=subprocess.PIPE)
        output = keymap_command.stdout.read()
        for out in output.decode("utf-8").split("\n"):
            if out.startswith("keycode") and out.count("="):
                out = out.split()
                if out[3].startswith("U+") or out[3].startswith("+U"):
                    first = bytes("\\u" + out[3][2:].replace("+", ""), "ascii").decode("unicode-escape")
                    second = bytes("\\u" + out[4][2:].replace("+", ""), "ascii").decode("unicode-escape")
                    keycodes[int(out[1])] = [first, second]

        return keycodes

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform|QPainter.Antialiasing|QPainter.HighQualityAntialiasing)

        painter.drawPixmap(QPoint(0, 0), self.keyboard_image)

        coordinat_list = ((10, 30), (90, 90), (115, 150), (80, 215))
        count = 0
        if self.is_paint:
            for key_list in keyboard_model[self.keyboard_model]:
                coordinat = coordinat_list[count]
                count += 1
                for num, key in enumerate(key_list):
                    print(num)
                    try:
                        font = painter.font()
                        font.setPointSize(12)
                        painter.setFont(font)

                        big = QPen(QColor("#ccff00"))
                        painter.setPen(big)
                        painter.drawText(coordinat[0]+(60*num), coordinat[1], self.keymap[key][1])

                        font = painter.font()
                        font.setPointSize(14)
                        painter.setFont(font)

                        little = QPen(QColor(255, 255, 255))
                        painter.setPen(little)
                        painter.drawText(coordinat[0]+15+(60*num), coordinat[1]+20, self.keymap[key][0])

                    except KeyError as err:
                        print(self.keymap, key)

