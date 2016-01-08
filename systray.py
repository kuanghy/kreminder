#! /usr/bin/env python
# -*- coding:utf8 -*-

# *************************************************************
#     Filename @  systray.py
#       Author @  Huoty
#  Create date @  2016-01-07 21:16:16
#  Description @ pyqt4 system tray icon
# *************************************************************

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys

class SysTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(SysTray, self).__init__(parent)
        self.initObjects()
        self.setObjects()

        self.activated.connect(self.iconClicked)
    def initObjects(self):
        self.menu = QMenu()
        self.helpAction = QAction(u'帮助', self, triggered=self.showHelp)
        self.quitAction = QAction(u"退出", self, triggered=self.exitApp)
        self.icon = QIcon('./icon/clock_32x32.png')

    def setObjects(self):
        self.menu.addAction(self.helpAction)
        self.menu.addAction(self.quitAction)
        self.setIcon(self.icon)
        self.setContextMenu(self.menu)

    def iconClicked(self, reason):
        print reason
        if reason==2 or reason==3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()
    def exitApp(self):
        self.setVisible(False)
        qApp.quit()
        sys.exit()

    def showHelp(self):
        os.system("xdg-open man/readme.html")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ti = SysTray()
    ti.show()
    ti.showMessage(u"提示", u"程序启动", 2)
    sys.exit(app.exec_())
