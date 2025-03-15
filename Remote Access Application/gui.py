import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenu, QSystemTrayIcon, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, Qt
import PyQt6.QtCore as QtCore
from PyQt6.QtGui import QIcon, QAction
import server
import threading

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.init_ui()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to initialize UI: {str(e)}")
            sys.exit(1)

    def init_ui(self):
        self.setWindowTitle("OwlGuard")
        self.setGeometry(600, 300, 1200, 800)
        self.setFixedSize(1200, 800)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # Ensure icon path is correct in packaged app
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "owl.png")
        self.setWindowIcon(QIcon(icon_path))

        self.browser = QWebEngineView()
        self.setup_browser_settings()
        
        # Wait for Flask server to start
        self.wait_for_server()
        
        # Setup system tray
        self.setup_system_tray()

        # Setup central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def setup_browser_settings(self):
        """Configure browser settings"""
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)

        profile = self.browser.page().profile()
        profile.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)

        # Set the URL after settings are configured
        self.browser.setUrl(QUrl("http://localhost:5000/"))

    def wait_for_server(self, max_retries=5):
        """Wait for Flask server to start"""
        import requests
        retry_count = 0
        while retry_count < max_retries:
            try:
                requests.get("http://localhost:5000/")
                return
            except requests.exceptions.ConnectionError:
                retry_count += 1
                time.sleep(1)
        
        QMessageBox.warning(None, "Warning", "Server startup is taking longer than expected. The application may not work correctly.")

    def setup_system_tray(self):
        """Setup system tray icon and menu"""
        try:
            tray_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images", "owlhiddenActive.png")
            self.tray_icon = QSystemTrayIcon(QIcon(tray_icon_path), self)
            self.tray_icon.setToolTip("OwlGuard")

            # Create tray menu
            tray_menu = QMenu()

            # Add actions
            restore_action = QAction("Show", self)
            restore_action.triggered.connect(self.show_window)

            minimize_action = QAction("Minimize to Tray", self)
            minimize_action.triggered.connect(self.hide_to_tray)

            exit_action = QAction("Exit", self)
            exit_action.triggered.connect(self.exit_app)

            # Add actions to menu
            tray_menu.addAction(restore_action)
            tray_menu.addAction(minimize_action)
            tray_menu.addSeparator()
            tray_menu.addAction(exit_action)

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
            self.tray_icon.activated.connect(self.on_tray_icon_click)
        except Exception as e:
            QMessageBox.warning(None, "Warning", f"Failed to initialize system tray: {str(e)}")

    def closeEvent(self, event):
        """Override close event to hide window instead of exiting"""
        event.ignore()
        self.hide_to_tray()

    def changeEvent(self, event):
        """Handle window state changes"""
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            if self.windowState() == Qt.WindowState.Minimized:
                self.hide_to_tray()
                event.accept()  # Prevents recursive calls
            else:
                super().changeEvent(event)
        else:
            super().changeEvent(event)


    def hide_to_tray(self):
        """Hide the window to system tray"""
        self.hide()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.showMessage(
                "OwlGuard",
                "Application minimized to system tray",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

    def on_tray_icon_click(self, reason):
        """Handle tray icon clicks"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide_to_tray()
            else:
                self.show_window()

    def show_window(self):
        """Show and activate the window"""
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def exit_app(self):
        """Properly exit the application"""
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        QApplication.quit()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        # Start Flask server in a daemon thread
        flaskThread = threading.Thread(target=server.startApp, daemon=True)
        flaskThread.start()

        app.setQuitOnLastWindowClosed(False)

        window = BrowserWindow()
        window.show()
        
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Fatal Error", f"Application failed to start: {str(e)}")
        sys.exit(1)
