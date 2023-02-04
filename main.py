import functools
import os
import sys
import time
import win32api
import win32con
import threading
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

from idle_time import start_idle_time
from screen_saver import start_screen_saver


def end_program():
    """
    End the program
    :return:
    """
    keep_running.set()
    thread.join()


# Check if the time_out is passed as an argument
if len(sys.argv) > 1:
    time_out = int(sys.argv[1])
else:
    time_out = 60

# Check if the screen saver is passed as an argument
if len(sys.argv) > 2:
    screen_saver = sys.argv[2]
else:
    screen_saver = "C:\\Windows\\System32\\scrnsave.scr"

# Start the idle time thread
keep_running = threading.Event()
thread = threading.Thread(target=start_idle_time, args=(time_out, keep_running))
thread.start()

# Create the application
app = QApplication(sys.argv)

# Create the system tray icon
tray_icon = QSystemTrayIcon(QIcon("lattice.ico"), app)

# Create the context menu
menu = QMenu()

# Create the actions
start_screen_saver_action = QAction("Start Screen Saver")
start_screen_saver_action.triggered.connect(functools.partial(start_screen_saver, "parameter"))
exit_system_action = QAction("Exit")

exit_system_action.triggered.connect(app.quit)
exit_system_action.triggered.connect(end_program)

# Add the actions to the menu
menu.addAction(start_screen_saver_action)
menu.addAction(exit_system_action)

# Add the menu to the system tray icon
tray_icon.setContextMenu(menu)
tray_icon.show()

# Start the application
sys.exit(app.exec_())
