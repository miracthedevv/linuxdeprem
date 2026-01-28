import sys
import os
import subprocess
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt

# =========================
# SABİTLER
# =========================
APP_NAME = "Linux Deprem Bildirici Kurulumu"

INSTALL_DIR = os.path.expanduser("~/.local/share/linux-deprem-bildirici")
SERVICE_DIR = os.path.expanduser("~/.config/systemd/user")
SERVICE_FILE = os.path.join(SERVICE_DIR, "linux-deprem-bildirici.service")

FILES = [
    "depremuyarisys.py",
    "trayservice.py",
    "settings.json",
    "siren.mp3",
    "logo.png",
    "U1_uyari.png",
    "U2_uyari.png",
    "U3_uyari.png",
]

# =========================
# SETUP GUI
# =========================
class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME + " - Kurulum")
        self.setFixedSize(460, 280)

        layout = QVBoxLayout()

        self.label = QLabel(
            "<h3>Linux Deprem Bildirici</h3>"
            "<p>Bu sihirbaz programı sistemine kurar ve<br>"
            "bilgisayar açılışında otomatik başlatır.</p>"
        )
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.button = QPushButton("Kurulumu Başlat")
        self.button.clicked.connect(self.install)
        layout.addWidget(self.button)

        self.setLayout(layout)

    # =========================
    # KURULUM
    # =========================
    def install(self):
        try:
            self.button.setEnabled(False)

            # 1️⃣ Python paketleri
            self.progress.setValue(10)
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "--user",
                "--break-system-packages",
                "-r", "requirements.txt"
            ])

            # 2️⃣ Dosyaları kopyala
            self.progress.setValue(40)
            os.makedirs(INSTALL_DIR, exist_ok=True)
            for f in FILES:
                shutil.copy(f, INSTALL_DIR)

            # 3️⃣ systemd user service
            self.progress.setValue(70)
            os.makedirs(SERVICE_DIR, exist_ok=True)

            service_text = f"""[Unit]
Description=Linux Deprem Bildirici
After=network.target

[Service]
ExecStart=/usr/bin/python3 {INSTALL_DIR}/trayservice.py
Restart=always

[Install]
WantedBy=default.target
"""

            with open(SERVICE_FILE, "w") as f:
                f.write(service_text)

            subprocess.call(["systemctl", "--user", "daemon-reload"])
            subprocess.call(["systemctl", "--user", "enable", "linux-deprem-bildirici"])
            subprocess.call(["systemctl", "--user", "start", "linux-deprem-bildirici"])

            # 4️⃣ KURULUM BİTER BİTMEZ ÇALIŞTIR
            subprocess.Popen(
                ["/usr/bin/python3", f"{INSTALL_DIR}/trayservice.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            self.progress.setValue(100)

            QMessageBox.information(
                self,
                "Kurulum Tamamlandı",
                "Linux Deprem Bildirici başarıyla kuruldu ve çalıştırıldı.\n\n"
                "Sistem tepsisinde (sağ altta) aktif."
            )
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Kurulum Hatası", str(e))
            self.button.setEnabled(True)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SetupWindow()
    win.show()
    sys.exit(app.exec())
