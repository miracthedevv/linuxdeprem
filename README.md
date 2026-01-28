# 🌍 Linux Deprem Bildirici

**Linux Deprem Bildirici**, Kandilli Rasathanesi (KOERI) verilerini kullanarak belirlediğiniz şehir ve büyüklük filtresine göre **gerçek zamanlı deprem uyarıları** veren, sistem tepsisinde (tray) çalışan bir Linux uygulamasıdır.

Deprem algılandığında:
- 🔊 Siren çalar  
- 🗣️ Google TTS ile sesli uyarı verir  
- 🖥️ Tam ekran görsel uyarı gösterir  

Uygulama **Ubuntu / Debian tabanlı** sistemlerle uyumludur.

---

## ✨ Özellikler

- 📡 Kandilli Rasathanesi canlı deprem verileri
- 🏙️ Şehir filtresi
- 📏 Minimum büyüklük filtresi (örn: **Mw ≥ 3.0**)
- 🔔 Tam ekran deprem uyarısı
- 🖼️ Değiştirilebilir uyarı tasarımları
- 🔊 Ses seviyesi ayarlanabilir siren sesi
- 🗣️ Google TTS ile Türkçe sesli uyarı
- 🧭 Sistem tepsisinde (tray) çalışma
- ⚙️ Grafik ayarlar menüsü
- 🧪 Test uyarısı
- 🚀 Bilgisayar açılışında otomatik başlatma (systemd user service)

---

## 🖥️ Ekran Görüntüleri

> (yakında)

- Tam ekran uyarı ekranı  
- Tray menüsü  
- Ayarlar penceresi  

---

## 📦 Kurulum (GUI – Önerilen)

### Gereksinimler

- Python 3.10 veya üzeri
- Linux (Ubuntu / Debian)
- İnternet bağlantısı

### Kurulum Adımları

```bash
git clone https://github.com/miracthedevv/linuxdeprem.git
cd linuxdeprem
python3 setup_gui.py
