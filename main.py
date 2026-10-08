import sys
import os
import socket
import threading
import time
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
import streamlit.web.cli as stcli

def get_resource_path(relative_path):
    if hasattr(sys, "frozen"):
        base_path = os.path.dirname(os.path.abspath(__file__))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_streamlit(port):
    app_path = get_resource_path("app.py")
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.port", str(port),
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false"
    ]
    stcli.main()

class MainWindow(QMainWindow):
    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Tyre Contact Area Analysis")
        self.resize(1300, 850)
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(f"http://localhost:{port}"))
        layout.addWidget(self.browser)
        
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    port = find_free_port()
    t = threading.Thread(target=run_streamlit, args=(port,), daemon=True)
    t.start()
    
    time.sleep(1.5)
    
    window = MainWindow(port)
    window.show()
    
    sys.exit(app.exec())