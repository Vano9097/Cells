import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

import main


class Settings:

    width = 50
    height = 50
    num_blocks_x = 10
    num_blocks_y = 10
    indentation = 2
    table_size_x = width * num_blocks_x
    table_size_y = height * num_blocks_y


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
        self.Table = main.Game(Settings.num_blocks_x, Settings.num_blocks_y)
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
        x = Settings.width * x + Settings.indentation
        y = Settings.height * y + Settings.indentation
        self.addRect(x, y, Settings.width-2*Settings.indentation, Settings.height-2*Settings.indentation, pen, brush)

    def draw_cells(self):
        for x in range(Settings.num_blocks_x):
            for y in range(Settings.num_blocks_y):
                self.draw_cell(x, y, self.Table.get(x, y).color)

    def draw_grid(self):
        width = Settings.num_blocks_x * Settings.width
        height = Settings.num_blocks_y * Settings.height
        self.setSceneRect(0, 0, width, height)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)

        for x in range(0, Settings.num_blocks_x+1):
            xc = x * Settings.width
            self.lines.append(self.addLine(xc, 0, xc, height, pen))

        for y in range(0, Settings.num_blocks_y+1):
            yc = y * Settings.height
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

        # self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft ) # зафиксировать клетку в верхнем левом угле

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

        point = self.mapToScene(event.x(), event.y())

        cell_x = int(point.x()//Settings.width)
        cell_y = int(point.y()//Settings.height)
        if 0 <= cell_x <= Settings.num_blocks_x and 0 <= cell_y <= Settings.num_blocks_y:

            if event.button() == Qt.LeftButton:
                a.Table.turn(cell_x, cell_y)
                a.draw_cells()

                if self.is_win():
                    print("You Win", a.Table.NumberOfTurn)
                    pass

            else:
                return
        else:
            return

    def is_win(self):
        return len(set(str(a.Table))) <= 2


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = QS()
    b = QV()
    b.setScene(a)
    b.show()
    sys.exit(app.exec_())
