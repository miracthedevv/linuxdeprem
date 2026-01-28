import os
import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox

APP_NAME = "Linux Deprem Bildirici"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
DESKTOP_FILE = os.path.join(AUTOSTART_DIR, "LinuxDepremBildirici.desktop")

REQUIRED_PACKAGES = [
    "pygame",
    "pystray",
    "PyQt6",
    "gTTS",
    "requests"
]

# -----------------------
# Python paketlerini kur
# -----------------------
def install_packages():
    for pkg in REQUIRED_PACKAGES:
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", pkg])

# -----------------------
# Autostart .desktop dosyası
# -----------------------
def create_autostart():
    os.makedirs(AUTOSTART_DIR, exist_ok=True)
    exec_path = os.path.join(APP_DIR, "trayservice.py")
    content = f"""[Desktop Entry]
Type=Application
Name=Linux Deprem Bildirici
Exec={sys.executable} {exec_path}
X-GNOME-Autostart-enabled=true
"""
    with open(DESKTOP_FILE, "w") as f:
        f.write(content)

# -----------------------
# Basit GUI
# -----------------------
class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} Kurulum")
        self.setFixedSize(400, 250)

        label = QLabel("Linux Deprem Bildirici kurulumu yapılacak.\n\nOtomatik başlatma ve bağımlılıklar kurulacak.")
        label.setWordWrap(True)
        btn_install = QPushButton("Kurulumu Başlat")
        btn_install.clicked.connect(self.run_setup)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(btn_install)
        self.setLayout(layout)

    def run_setup(self):
        try:
            install_packages()
            create_autostart()
            QMessageBox.information(self, "Tamamlandı", "Kurulum tamamlandı!\nBilgisayar açıldığında uygulama otomatik başlayacak.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kurulum sırasında hata oluştu:\n{e}")

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SetupWindow()
    window.show()
    sys.exit(app.exec())
