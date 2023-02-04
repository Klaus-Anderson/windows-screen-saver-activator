import time

import win32api
import win32con

from screen_saver import start_screen_saver


def idle_time(time_out, kill_thread):
    """
    Check if the user is idle
    :param kill_thread: if this flag is set to true somewhere else, the thread will stop
    :param time_out: The timeout in seconds
    :return: return True if the user is idle after time, otherwise never return
    """

    # Initialize the last input time to the current time and get the initial position of the mouse cursor
    last_input_time = time.time()
    initial_pos = win32api.GetCursorPos()

    # Loop until the user is idle for time_out seconds or the kill_thread flag is set to true
    while not kill_thread.is_set():
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
        time.sleep(1) # Sleep for a short time to reduce CPU usage
    return False


def start_idle_time(idle_time_out, kill_thread):
    """
    Start the idle time thread
    :param kill_thread:
    :param idle_time_out:
    :return:
    """
    if idle_time(idle_time_out, kill_thread):
        # Start the screen saver
        start_screen_saver()
        # Start the idle time thread again
        start_idle_time(idle_time_out, kill_thread)
