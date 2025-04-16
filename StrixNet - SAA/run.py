import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.app import BrowserWindow
from core.server import start_app
import multiprocessing
import ctypes
import os


def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)





def run_flask():
    """ Start the Flask server in a separate process """
    start_app()


def main():
    """ Start both Flask server and PyQt6 application """
    # Check for admin privileges
    run_as_admin()
    multiprocessing.freeze_support()  # Fix for Windows multiprocessing issues

    flask_process = multiprocessing.Process(target=run_flask, daemon=True)
    flask_process.start()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
