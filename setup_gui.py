import os
import sys
import subprocess
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QProgressBar, QMessageBox
)

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
# Paket kurulum fonksiyonu
# -----------------------
def install_packages(progress_callback=None):
    total = len(REQUIRED_PACKAGES)
    for i, pkg in enumerate(REQUIRED_PACKAGES, start=1):
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", pkg])
        if progress_callback:
            progress_callback(int((i/total)*100))

# -----------------------
# Autostart dosyası oluştur
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
# Kurulum GUI
# -----------------------
class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} Kurulum")
        self.setFixedSize(400, 250)

        # Başlık ve bilgi
        label = QLabel("Linux Deprem Bildirici kurulumu yapılacak.\n\nOtomatik başlatma ve bağımlılıklar kurulacak.")
        label.setWordWrap(True)

        # Kurulum başlat butonu
        self.btn_install = QPushButton("Kurulumu Başlat")
        self.btn_install.clicked.connect(self.run_setup)

        # İlerleme çubuğu
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFormat("%p%%")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.progress)
        layout.addWidget(self.btn_install)
        self.setLayout(layout)

    # -----------------------
    # Kurulum işlemi
    # -----------------------
    def run_setup(self):
        self.btn_install.setEnabled(False)
        threading.Thread(target=self._setup_thread, daemon=True).start()

    def _setup_thread(self):
        try:
            # Paketleri yükle ve ilerlemeyi güncelle
            install_packages(progress_callback=lambda val: self.progress.setValue(val))
            # Autostart oluştur
            create_autostart()
            # Tray servisi başlat
            subprocess.Popen([sys.executable, os.path.join(APP_DIR, "trayservice.py")])
            # Başarı mesajı
            QMessageBox.information(self, "Tamamlandı",
                "Kurulum tamamlandı!\nBilgisayar açıldığında uygulama otomatik başlayacak.")
        except Exception as e:
            QMessageBox.critical(self, "Hata",
                f"Kurulum sırasında hata oluştu:\n{e}")
        finally:
            self.btn_install.setEnabled(True)
            self.progress.setValue(100)

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SetupWindow()
    window.show()
    sys.exit(app.exec())
