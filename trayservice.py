import sys
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QSlider, QPushButton, QRadioButton, QButtonGroup, QLineEdit
from PyQt6.QtCore import Qt
import json
import depremuyarisys
import pygame

pygame.init()
pygame.mixer.init()

# =========================
# Ayarlar Penceresi
# =========================
class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Deprem Bildirici Ayarlar")
        self.setGeometry(100,100,400,550)
        layout = QVBoxLayout()

        # TTS checkbox
        self.tts_checkbox = QCheckBox("Google TTS ile deprem bilgilerini sesli oku")
        self.tts_checkbox.setChecked(depremuyarisys.settings.get("tts",True))
        layout.addWidget(self.tts_checkbox)

        # Siren slider ve label
        layout.addWidget(QLabel("Siren Ses Seviyesi"))
        self.siren_slider = QSlider()
        self.siren_slider.setOrientation(Qt.Orientation.Horizontal)
        self.siren_slider.setMinimum(0)
        self.siren_slider.setMaximum(100)
        self.siren_slider.setValue(depremuyarisys.settings.get("siren_volume",50))
        layout.addWidget(self.siren_slider)
        self.siren_value_label = QLabel(f"{self.siren_slider.value()} %")
        layout.addWidget(self.siren_value_label)
        self.siren_slider.valueChanged.connect(lambda: self.siren_value_label.setText(f"{self.siren_slider.value()} %"))

        # Uyarı ekranı seçimi
        layout.addWidget(QLabel("Uyarı Ekranını Seç"))
        uyari_list = ["U1_uyari.png","U2_uyari.png","U3_uyari.png"]
        self.radio_group = QButtonGroup(self)
        for ufile in uyari_list:
            radio = QRadioButton(ufile)
            if ufile == depremuyarisys.settings.get("uyari_screen","U1_uyari.png"):
                radio.setChecked(True)
            self.radio_group.addButton(radio)
            layout.addWidget(radio)

        # Şehir filtresi
        layout.addWidget(QLabel("Deprem Şehri Filtresi"))
        self.city_input = QLineEdit()
        self.city_input.setText(depremuyarisys.settings.get("city_filter","TRABZON"))
        layout.addWidget(self.city_input)

        # Minimum büyüklük slider ve label
        layout.addWidget(QLabel("Minimum Deprem Büyüklüğü (Mw)"))
        self.mw_slider = QSlider()
        self.mw_slider.setOrientation(Qt.Orientation.Horizontal)
        self.mw_slider.setMinimum(0)
        self.mw_slider.setMaximum(10)
        self.mw_slider.setValue(int(depremuyarisys.settings.get("mw_threshold",3.0)))
        layout.addWidget(self.mw_slider)
        self.mw_value_label = QLabel(f"{self.mw_slider.value()} Mw")
        layout.addWidget(self.mw_value_label)
        self.mw_slider.valueChanged.connect(lambda: self.mw_value_label.setText(f"{self.mw_slider.value()} Mw"))

        layout.addWidget(QLabel("\n2026 © miracthedev"))
        # Önizle ve Kaydet
        self.preview_btn = QPushButton("Önizle")
        self.preview_btn.clicked.connect(self.preview)
        layout.addWidget(self.preview_btn)

        self.save_btn = QPushButton("Kaydet")
        self.save_btn.clicked.connect(self.save)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def preview(self):
        sel = [b.text() for b in self.radio_group.buttons() if b.isChecked()]
        if sel:
            depremuyarisys.settings["uyari_screen"] = sel[0]
            eq_demo = {"yer":"Trabzon","tarih":"28.01.2026","saat":"21:42","mw":4.5}
            threading.Thread(target=depremuyarisys.show_alert,args=(eq_demo,),daemon=True).start()

    def save(self):
        depremuyarisys.settings["tts"] = self.tts_checkbox.isChecked()
        depremuyarisys.settings["siren_volume"] = self.siren_slider.value()
        sel = [b.text() for b in self.radio_group.buttons() if b.isChecked()]
        if sel:
            depremuyarisys.settings["uyari_screen"] = sel[0]
        depremuyarisys.settings["city_filter"] = self.city_input.text().upper()
        depremuyarisys.settings["mw_threshold"] = self.mw_slider.value()
        with open("settings.json","w") as f:
            json.dump(depremuyarisys.settings,f)
        self.close()

# =========================
# Test Uyarısı
# =========================
def test_alert(icon=None, item=None):
    eq_demo = {"yer":"Trabzon","tarih":"28.01.2026","saat":"21:42","mw":4.5}
    threading.Thread(target=depremuyarisys.show_alert,args=(eq_demo,),daemon=True).start()

# =========================
# Tray Menüsü
# =========================
def create_tray():
    def on_settings(icon, item):
        if not hasattr(on_settings, "app"):
            on_settings.app = QApplication(sys.argv)
        win = SettingsWindow()
        win.show()

    def on_test(icon, item):
        test_alert()

    def on_quit(icon, item):
        icon.stop()

    menu = Menu(
        MenuItem("Ayarlar", on_settings),
        MenuItem("Test Uyarısı", on_test),
        MenuItem("Linux Deprem Bildirici'yi Kapat", on_quit)
    )

    image = Image.open("traylogo.png")
    icon = Icon("DepremBildirici", image, "Linux Deprem Bildirici", menu)
    icon.run()

# =========================
# Başlat
# =========================
if __name__ == "__main__":
    create_tray()
