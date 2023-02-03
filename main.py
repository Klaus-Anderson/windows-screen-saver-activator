import os
import sys
import time
import win32api
import win32con
import threading
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon


def idle_time(time_out):
    """
    Check if the user is idle
    :param time_out: The time out in seconds
    :return: return True if the user is idle after time, otherwise never return
    """

    # Initialize the last input time to the current time and get the initial position of the mouse cursor
    last_input_time = time.time()
    initial_pos = win32api.GetCursorPos()
    while True:
        for i in range(1, 255):
            # Check if the key is being pressed
            if win32api.GetAsyncKeyState(i):
                # Update the last input time
                last_input_time = time.time()
                break  # Break out of the loop
        # Check if the mouse cursor has moved
        current_pos = win32api.GetCursorPos()
        if current_pos != initial_pos:
            # Update the last input time
            last_input_time = time.time()
            initial_pos = current_pos  # Update the initial position
        # Check if the left mouse button is being pressed
        if win32api.GetKeyState(win32con.VK_LBUTTON) < 0:
            # Update the last input time
            last_input_time = time.time()
        # Check if the elapsed time since the last input is greater than time_out
        if time.time() - last_input_time > time_out:
            return True
        time.sleep(1)  # Sleep for a short time to reduce CPU usage


def start_screen_saver():
    """
    Start the screen saver
    :return:
    """
    file_path = "C:\\Windows\\SysWOW64\\Lattice.scr"
    if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
        os.startfile(file_path)
    else:
        print(f"Error: Cannot start {file_path}")


def start_idle_time(idle_time_out):
    """
    Start the idle time thread
    :param idle_time_out:
    :return:
    """
    if idle_time(idle_time_out):
        start_screen_saver()
        start_idle_time(idle_time_out)


# Create the application
app = QApplication(sys.argv)

# Create the system tray icon
tray_icon = QSystemTrayIcon(QIcon("lattice.ico"), app)

# Create the context menu
menu = QMenu()

# Create the actions
start_screen_saver_action = QAction("Start Screen Saver")
start_screen_saver_action.triggered.connect(start_screen_saver)
exit_system_action = QAction("Exit")
exit_system_action.triggered.connect(app.quit)

# Add the actions to the menu
menu.addAction(start_screen_saver_action)
menu.addAction(exit_system_action)

# Add the menu to the system tray icon
tray_icon.setContextMenu(menu)
tray_icon.show()

# Check if the time out is passed as an argument
if len(sys.argv) > 1:
    time_out = int(sys.argv[1])
else:
    time_out = 15

# Start the idle time thread
thread = threading.Thread(target=start_idle_time, args=(time_out,))
thread.start()

# Start the application
sys.exit(app.exec_())
