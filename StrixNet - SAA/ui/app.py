import sys
import multiprocessing
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenu, QSystemTrayIcon, QSplashScreen
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap
import core.server as server
import requests

# Constants
APP_NAME = "OwlGuard"
WINDOW_SIZE = (1000, 800)
ICON_PATH = os.path.abspath("assets/images/owl.ico")
TRAY_ICON_PATH = os.path.abspath("assets/images/owlhiddenActive.png")
FLASK_URL = "http://localhost:5000/"

def start_flask_server():
    """Run Flask server in a separate process for better performance."""
    multiprocessing.Process(target=server.start_app, daemon=True).start()

class BrowserWindow(QMainWindow):
    """Main PyQt6 Browser Window with Optimizations"""

    def __init__(self):
        super().__init__()
        self.tray_icon = None
        self.browser = None
        self.is_minimized = False
        self._init_ui()
        QTimer.singleShot(100, self._load_browser)
        QTimer.singleShot(500, self._init_tray_icon)

    def _init_ui(self):
        """Initialize UI components quickly."""
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(*WINDOW_SIZE)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # Set window icon
        icon = QIcon(ICON_PATH)
        self.setWindowIcon(icon)
        
        # Set taskbar icon
        if hasattr(self, 'setWindowIcon'):
            self.setWindowIcon(icon)
            if hasattr(self, 'setWindowIconVisible'):
                self.setWindowIconVisible(True)

        self.browser = QWebEngineView()
        self._configure_browser()

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.browser)
        self.setCentralWidget(self.central_widget)

    def _load_browser(self):
        """Lazy-load the browser's URL to speed up UI launch."""
        self.browser.setUrl(QUrl(FLASK_URL))

    def _configure_browser(self):
        """Optimized browser settings for speed and security."""
        settings = self.browser.settings()
        for feature in [
            QWebEngineSettings.WebAttribute.JavascriptEnabled,
            QWebEngineSettings.WebAttribute.PluginsEnabled,
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
            QWebEngineSettings.WebAttribute.AutoLoadImages,
            QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled,
            QWebEngineSettings.WebAttribute.WebGLEnabled,
        ]:
            settings.setAttribute(feature, True)

    def _init_tray_icon(self):
        """Initialize system tray icon with minimal delay."""
        self.tray_icon = QSystemTrayIcon(QIcon(TRAY_ICON_PATH), self)
        self.tray_icon.setToolTip(APP_NAME)

        tray_menu = QMenu(self)
        tray_menu.addAction(QAction("Restore", self, triggered=self.show_window))
        tray_menu.addAction(QAction("Exit", self, triggered=self.exit_app))
        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.activated.connect(lambda reason: self.show_window() if reason == QSystemTrayIcon.ActivationReason.Trigger else None)
        self.tray_icon.show()

    def closeEvent(self, event):
        """Override close event to minimize instead of quitting."""
        event.ignore()
        self.hide()
        self.is_minimized = True
        self.tray_icon.showMessage(APP_NAME, "Minimized to system tray.", QSystemTrayIcon.MessageIcon.Information, 2000)

    def show_window(self):
        """Restore application window."""
        self.showNormal()
        self.activateWindow()
        self.is_minimized = False

    def exit_app(self):
        """Properly exit application."""
        try:
            requests.get(f"{FLASK_URL}logout")
        except:
            pass
        self.tray_icon.hide()
        QApplication.quit()


