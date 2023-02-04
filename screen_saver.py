import os


def start_screen_saver(path_to_screen_saver):
    """
    Start the screen saver
    :return:
    """
    if os.path.isfile(path_to_screen_saver) and os.access(path_to_screen_saver, os.X_OK):
        os.startfile(path_to_screen_saver)
    else:
        print(f"Error: Cannot start {path_to_screen_saver}")