import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

import main


class Settings:

    WIDTH = 50
    HEIGHT = 50
    NUM_BLOCKS_X = 5
    NUM_BLOCKS_Y = 5
    INDENTATION = 2


def create_action(parent, text, slot=None,
                  shortcut=None, shortcuts=None, shortcut_context=None,
                  icon=None, tooltip=None,
                  checkable=False, checked=False):
    action = QtWidgets.QAction(text, parent)

    if icon is not None:
        action.setIcon(QIcon(':/%s.png' % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if shortcuts is not None:
        action.setShortcuts(shortcuts)
    if shortcut_context is not None:
        action.setShortcutContext(shortcut_context)
    if tooltip is not None:
        action.setToolTip(tooltip)
        action.setStatusTip(tooltip)
    if checkable:
        action.setCheckable(True)
    if checked:
        action.setChecked(True)
    if slot is not None:
        action.triggered.connect(slot) #??

    return action


class QS(QtWidgets.QGraphicsScene):

    def __init__(self, *args):
        super().__init__(*args)

        self.Table = main.Game(Settings.NUM_BLOCKS_X, Settings.NUM_BLOCKS_Y)
        self.lines = []
        self.draw_grid()
        self.set_opacity(0.1)
        # self.set_visible(False)
        # self.delete_grid()
        self.draw_cells()

    def draw_cell(self, x=0, y=0, color=1):
        pen = QPen(QtCore.Qt.NoPen)
        if color == 1:
            brush = QBrush(QtCore.Qt.black)
        else:
            brush = QBrush(QtCore.Qt.white)
        X = Settings.WIDTH * x + Settings.INDENTATION
        Y = Settings.HEIGHT * y + Settings.INDENTATION
        self.addRect(X, Y, Settings.WIDTH-2*Settings.INDENTATION, Settings.HEIGHT-2*Settings.INDENTATION, pen, brush)

    def draw_cells(self):
        for x in range(Settings.NUM_BLOCKS_X):
            for y in range(Settings.NUM_BLOCKS_Y):
                self.draw_cell(x, y, self.Table.get(x, y).color)



    def draw_grid(self):
        width = Settings.NUM_BLOCKS_X * Settings.WIDTH
        height = Settings.NUM_BLOCKS_Y * Settings.HEIGHT
        self.setSceneRect(0, 0, width, height)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)

        for x in range(0, Settings.NUM_BLOCKS_X+1):
            xc = x * Settings.WIDTH
            self.lines.append(self.addLine(xc, 0, xc, height, pen))

        for y in range(0, Settings.NUM_BLOCKS_Y+1):
            yc = y * Settings.HEIGHT
            self.lines.append(self.addLine(0, yc, width, yc, pen))

    def set_visible(self, visible=True):
        for line in self.lines:
            line.setVisible(visible)

    def delete_grid(self):
        for line in self.lines:
            self.removeItem(line)
        del self.lines[:]

    def set_opacity(self, opacity):
        for line in self.lines:
            line.setOpacity(opacity)


class QV(QtWidgets.QGraphicsView):

    def __init__(self, *args):
        super().__init__(*args)

        self.view_menu = QMenu(self)
        self.create_actions()

    def create_actions(self):
        act = create_action(self.view_menu, "Zoom in",
                            slot=self.on_zoom_in,
                            shortcut=QKeySequence("+"), shortcut_context=Qt.WidgetShortcut)
        self.view_menu.addAction(act)

        act = create_action(self.view_menu, "Zoom out",
                            slot=self.on_zoom_out,
                            shortcut=QKeySequence("-"), shortcut_context=Qt.WidgetShortcut)
        self.view_menu.addAction(act)
        self.addActions(self.view_menu.actions())

    def on_zoom_in(self):
        if not self.scene():
            return

        self.scale(1.5, 1.5)

    def on_zoom_out(self):
        if not self.scene():
            return

        self.scale(1.0 / 1.5, 1.0 / 1.5)

    def mousePressEvent(self, event):
        cell_x = event.x()//Settings.WIDTH
        cell_y = event.y()//Settings.HEIGHT
        if 0 <= cell_x <= Settings.NUM_BLOCKS_X and 0 <= cell_y <= Settings.NUM_BLOCKS_Y:
            print(cell_x, cell_y)
            # print(self.scale())
            if event.button() == Qt.LeftButton:
                a.Table.turn(cell_x, cell_y)
                #print(a.Table)
                a.draw_cells()
                #a.draw_cell(cell_x,cell_y)
            else:
                return
        else:
            return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = QS()
    b = QV()
    b.setScene(a)
    # b.resize(800,600)
    b.show()
    sys.exit(app.exec_())
