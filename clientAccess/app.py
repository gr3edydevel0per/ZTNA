import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenu, QSystemTrayIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon, QAction

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OwlGuard")
        self.setGeometry(600, 300, 1200, 800)
        self.setFixedSize(1200, 800)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon("owl.png"))  # Ensure this image exists

        # ✅ Create Web View
        self.browser = QWebEngineView()

        # ✅ Enable JavaScript, Plugins, and Media Playback
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)

        # ✅ Allow Insecure Content (For HTTP Giphy URLs, if needed)
        profile = self.browser.page().profile()
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)

        # ✅ Load external HTML file (Flask server must be running!)
        self.browser.setUrl(QUrl("http://localhost:5000/"))

        # ✅ System Tray Icon Setup
        self.tray_icon = QSystemTrayIcon(QIcon("owlhiddenActive.png"), self)  # Ensure this image exists
        self.tray_icon.setToolTip("ZTNA Secure Access")

        # ✅ Tray Menu
        tray_menu = QMenu()

        restore_action = QAction("Restore", self)
        restore_action.triggered.connect(self.show_window)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)

        tray_menu.addAction(restore_action)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)

        # ✅ Show Tray Icon
        self.tray_icon.show()

        # ✅ Handle Tray Icon Clicks (Restore on click)
        self.tray_icon.activated.connect(self.on_tray_icon_click)

        # ✅ Set Layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def closeEvent(self, event):
        """ Override close event to hide window instead of exiting """
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "ZTNA Secure Access", 
            "Minimized to system tray.", 
            QSystemTrayIcon.MessageIcon.Information, 
            3000
        )

    def on_tray_icon_click(self, reason):
        """ Restore window when clicking on the tray icon """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()

    def show_window(self):
        """ Show the application window """
        self.showNormal()
        self.activateWindow()

    def exit_app(self):
        """ Properly exit the application """
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ✅ Ensure app stays running even when window is closed
    app.setQuitOnLastWindowClosed(False)

    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())
