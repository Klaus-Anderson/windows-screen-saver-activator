import os
import time
import win32api
import win32con
import win32gui


def idle_time(time_out):
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

        # Check if the elapsed time since the last input is greater than 5 minutes
        if time.time() - last_input_time > time_out:
            return True
        time.sleep(1)  # Sleep for a short time to reduce CPU usage


def create_icon_hidden_window():
    # Create a window class for the icon
    wc = win32gui.WNDCLASS()
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.lpszClassName = "Idle Time"
    wc.lpfnWndProc = WndProc  # Set the window procedure to the custom function defined below
    class_atom = win32gui.RegisterClass(wc)

    # Create the icon window
    hwnd = win32gui.CreateWindow(
        class_atom,
        "Idle Time",
        win32con.WS_OVERLAPPED | win32con.WS_SYSMENU,
        0,
        0,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        0,
        0,
        wc.hInstance,
        None
    )
    win32gui.UpdateWindow(hwnd)

    # Load the icon image and set it as the icon for the window
    icon_path = "lattice.ico"  # Replace with the path to your icon file
    icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
    hicon = win32gui.LoadIcon(icon_path, win32con.IMAGE_ICON, 0, 0, icon_flags)
    win32api.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)

    # Create a menu for the icon
    menu = win32gui.CreatePopupMenu()
    win32gui.AppendMenu(menu, win32con.MF_STRING, 1000, "Stop script")
    win32gui.SetMenuDefaultItem(menu, 1000, 0)

    # Show the icon on the taskbar with the menu
    win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, (hwnd, 0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP, win32con.WM_USER + 20, (hicon, 0), "Idle Time", menu))

    return hwnd


def WndProc(hwnd, msg, wparam, lparam):
    if msg == win32con.WM_COMMAND:
        # The "Stop script" option was selected from the menu
        if wparam == 1000:
            # Remove the icon from the taskbar
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, (hwnd, 0))
            win32gui.PostQuitMessage(0)  # Quit the message loop
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)


if __name__ == '__main__':
    hidden_window = create_icon_hidden_window()
    if idle_time(15):
        # Remove the icon from the taskbar
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, (hidden_window, 0))
        win32gui.PostQuitMessage(0)  # Quit the message loop
        print("The mouse and keyboard have been idle for 5 minutes.")
        # Run the executable file "example.exe"
        os.startfile("C:\\Windows\\SysWOW64\\Lattice.scr")
