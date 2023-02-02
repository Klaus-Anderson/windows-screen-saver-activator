import os
import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

def start_screen_saver():
    file_path = "C:\\Windows\\SysWOW64\\Lattice.scr"
    if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
        os.startfile(file_path)
    else:
        print(f"Error: Cannot start {file_path}")

app = QApplication(sys.argv)

tray_icon = QSystemTrayIcon(QIcon("lattice.ico"), app)
tray_icon.show()

menu = QMenu()

start_screen_saver_action = QAction("Start Screen Saver")
start_screen_saver_action.triggered.connect(start_screen_saver)

menu.addAction(start_screen_saver_action)

tray_icon.setContextMenu(menu)

sys.exit(app.exec_())