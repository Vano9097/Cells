from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QAction, qApp, QSizePolicy
from PyQt5.QtWidgets import QMenu, QMainWindow
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

import sys

from PyQt5.QtWidgets import QMessageBox

import main

import Settings


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
        action.triggered.connect(slot)  # ??

    return action


class QS(QtWidgets.QGraphicsScene):
    def __init__(self, *args):
        super().__init__(*args)
        self.Table = main.Game(Settings.num_blocks_x, Settings.num_blocks_y, Settings.presetting)
        self.lines = []
        self.draw_grid()
        self.set_opacity(0.3)
        # self.set_visible(False)
        self.draw_cells()

    def draw_cell(self, x=0, y=0, color=1):
        pen = QPen(QtCore.Qt.NoPen)
        if color == 1:
            brush = QBrush(QtCore.Qt.black)
        else:
            brush = QBrush(QtCore.Qt.white)
        x = Settings.width * x + Settings.indentation
        y = Settings.height * y + Settings.indentation
        self.addRect(x, y, Settings.width - 2 * Settings.indentation, Settings.height - 2 * Settings.indentation, pen,
                     brush)

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

        for x in range(0, Settings.num_blocks_x + 1):
            xc = x * Settings.width
            self.lines.append(self.addLine(xc, 0, xc, height, pen))

        for y in range(0, Settings.num_blocks_y + 1):
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
        self.a = QS()
        self.setScene(self.a)

        # self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft ) # зафиксировать клетку в верхнем левом угле

        self.view_menu = QMenu(self)
        self.create_actions()
        self.create_dock()


    def create_dock(self):

        self.dockWidget = QtWidgets.QDockWidget()
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.verticalLayoutWidget = QtWidgets.QWidget(self.dockWidgetContents)
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 150, 600))  # разобраться

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.label, stretch=0)

        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        self.verticalLayout.addWidget(self.textBrowser, stretch=0)

        self.dockWidget.setWidget(self.dockWidgetContents)

        self.dockWidget.setMinimumWidth(150)
        self.dockWidget.setMinimumHeight(230)
        self.textBrowser.setMaximumWidth(148)

        self.label.setText("Совершено ходов: " + str(self.a.Table.NumberOfTurn))

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
        cell_x = int(point.x() // Settings.width)
        cell_y = int(point.y() // Settings.height)

        if 0 <= cell_x < Settings.num_blocks_x and 0 <= cell_y < Settings.num_blocks_y:

            if event.button() == Qt.LeftButton:
                self.a.Table.turn(cell_x, cell_y)
                self.a.draw_cells()

                self.label.setText("Совершено ходов: " + str(self.a.Table.NumberOfTurn))
                if self.is_win():
                    self.a.Table.log.append("You Win : " + str(self.a.Table.NumberOfTurn))
                    # добавить всплывающее диалоговое окно с поздравлением и началом новой игры
                self.textBrowser.setText(self.str_log())  # сделать красиво

            else:
                return
        else:
            return

    def str_log(self):

        rez = ""
        for point in reversed(self.a.Table.log):
            if type(point) == tuple:
                rez += "шаг " + str(point[0]) + ": " + str(point[1] + 1) + " " + str(
                    Settings.num_blocks_y - point[2]) + "\n"
            else:
                rez += point + "\n"

        return rez

    def is_win(self):
        return ("0" not in set(str(self.a.Table))) or ("1" not in set(str(self.a.Table)))  # переписать нормально


class Window(QMainWindow):
    def __init__(self, *args):
        super().__init__(*args)
        self.b = QV()
        self.setCentralWidget(self.b)

        self.menu = self.menuBar()
        self.create_menu()
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.b.dockWidget)

    def new_random(self):
        self.b.a = QS()
        self.b.setScene(self.b.a)
        self.b.label.setText("Совершено ходов: " + str(self.b.a.Table.NumberOfTurn))

        self.b.textBrowser.setText(self.b.str_log())

    def create_menu(self):
        self.file = self.menu.addMenu("Файл")
        new_game = create_action(self.menu, "Заново", slot=self.new_random)

        self.file.addAction(new_game)

        action_open = create_action(self.menu, "Открыть", slot=None,
                                    shortcut=None, shortcuts=None, shortcut_context=None,
                                    icon=None, tooltip=None,
                                    checkable=False, checked=False)
        self.file.addAction(action_open)

        self.file.addSeparator()

        action_save = create_action(self.menu, "Сохранить", slot=None,
                                    shortcut=None, shortcuts=None, shortcut_context=None,
                                    icon=None, tooltip=None,
                                    checkable=False, checked=False)
        self.file.addAction(action_save)

        self.file.addSeparator()

        action_settings = create_action(self.menu, "Настройки", slot=self.change_menu,
                                        shortcut=None, shortcuts=None, shortcut_context=None,
                                        icon=None, tooltip=None,
                                        checkable=False, checked=False)
        self.file.addAction(action_settings)

        # self.file.addSeparator()
        #
        # action_exit = create_action(self.menu, "Выход", slot=None,
        #                             shortcut=None, shortcuts=None, shortcut_context=None,
        #                             icon=None, tooltip=None,
        #                             checkable=False, checked=False)
        #
        # self.file.addAction(action_exit)

        self.information = self.menu.addMenu("Справка")

        self.setMenuBar(self.menu)

    def change_menu(self):
        dialog = QtWidgets.QInputDialog(self)
        dialog.setLabelText("Размер поля")
        dialog.setOkButtonText("&Bвoд")
        dialog.setCancelButtonText("&Oтмeнa")
        dialog.setInputMode(QtWidgets.QInputDialog.IntInput)

        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            Settings.num_blocks_x = dialog.intValue()
            Settings.num_blocks_y = dialog.intValue()
            self.new_random()
            return True
        else:
            return False



    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Подтверждение закрытия',
                                     "Вы уверены что хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def resizeEvent(self, еvent):
        self.b.verticalLayoutWidget.setFixedHeight(еvent.size().height() - 70)
        QtWidgets.QWidget.resizeEvent(self, еvent)


def start():
    app = QtWidgets.QApplication(sys.argv)
    c = Window()
    c.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # c = Window()
    # c.show()
    # sys.exit(app.exec_())
    start()
