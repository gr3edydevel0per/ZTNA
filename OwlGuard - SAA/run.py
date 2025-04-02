import sys
from PyQt6.QtWidgets import QApplication
from ui.app import BrowserWindow
from core.server import start_app
import multiprocessing


def run_flask():
    """ Start the Flask server in a separate process """
    start_app()


def main():
    """ Start both Flask server and PyQt6 application """
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
