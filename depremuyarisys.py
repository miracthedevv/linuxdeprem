import pygame
import sys
import threading
import time
import os
import requests
import re
from gtts import gTTS
import json

# =========================
# Ayarlar dosyası
# =========================
SETTINGS_FILE = "settings.json"
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {
        "tts": True,
        "siren_volume": 50,
        "uyari_screen": "U1_uyari.png",
        "city_filter": "TRABZON",
        "mw_threshold": 3.0
    }

# =========================
# Kandilli URL
# =========================
URL = "http://www.koeri.boun.edu.tr/scripts/lst0.asp"

# =========================
# TTS Düzenleme
# =========================
def tts_duzelt(metin: str) -> str:
    m = metin.lower()
    m = re.sub(r"\(.*?\)", "", m)
    m = re.sub(r"[-_/]", " ", m)
    m = re.sub(r"\s+", " ", m).strip()
    return m.title()

# =========================
# Kandilli Veri Çek
# =========================
def deprem_cek():
    try:
        r = requests.get(URL, timeout=10)
        r.encoding = "iso-8859-9"
        lines = r.text.splitlines()

        for s in lines:
            s = s.strip()
            if len(s) < 80 or not s[0:4].isdigit() or s[4] != ".":
                continue

            yer = s[71:110].strip()
            mw_raw = s[60:63].strip().replace("-", "")
            try:
                mw = float(mw_raw)
            except:
                mw = 0.0

            # İlk satır = en son deprem
            if settings["city_filter"].upper() not in yer.upper():
                return None

            if mw < float(settings["mw_threshold"]):
                return None

            return {
                "yer": yer,
                "tarih": s[0:10],
                "saat": s[11:19],
                "mw": mw
            }
    except:
        return None

# =========================
# Google TTS
# =========================
def google_tts(text):
    tts = gTTS(text=text, lang="tr")
    tts.save("tts.mp3")

    pygame.mixer.music.set_volume(settings["siren_volume"]/200)
    sound = pygame.mixer.Sound("tts.mp3")
    sound.play()

    while pygame.mixer.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.set_volume(settings["siren_volume"]/100)
    os.remove("tts.mp3")

# =========================
# Ana Uyarı Fonksiyonu
# =========================
def show_alert(eq):
    pygame.init()
    pygame.mixer.init()

    W, H = 1920, 1080
    screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    bg_file = settings.get("uyari_screen", "U1_uyari.png")
    bg = pygame.image.load(bg_file)
    bg = pygame.transform.scale(bg, (W, H))

    title_font = pygame.font.SysFont("DejaVu Sans", 64, bold=True)
    label_font = pygame.font.SysFont("DejaVu Sans", 30, bold=True)
    value_font = pygame.font.SysFont("DejaVu Sans", 42, bold=True)

    RED   = (220, 0, 0)
    WHITE = (255, 255, 255)
    GRAY  = (190, 190, 190)

    # Siren çal
    if eq["mw"] >= settings["mw_threshold"]:
        pygame.mixer.music.load("siren.mp3")
        pygame.mixer.music.set_volume(settings["siren_volume"]/100)
        pygame.mixer.music.play(-1)

        if settings["tts"]:
            yer_tts = tts_duzelt(eq["yer"])
            threading.Thread(
                target=google_tts,
                args=(f"{yer_tts} merkezli deprem. Büyüklük {eq['mw']}",),
                daemon=True
            ).start()

    running = True
    while running:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        screen.blit(bg, (0, 0))

        # Üst saydam bant
        band_h = 200
        band = pygame.Surface((W, band_h), pygame.SRCALPHA)
        band.fill((0,0,0,128))
        screen.blit(band, (0,0))

        # Başlık
        title = title_font.render("DEPREM UYARISI", True, RED)
        screen.blit(title, title.get_rect(center=(W//2,35)))

        # Sütunlar
        cols = 3
        margin = 120
        usable_w = W - margin*2
        col_w = usable_w // cols
        base_y = 80

        def draw_column(index, label, value):
            cx = margin + col_w*index + col_w//2
            lbl = label_font.render(label, True, GRAY)
            val = value_font.render(value, True, WHITE)
            screen.blit(lbl, lbl.get_rect(center=(cx, base_y)))
            screen.blit(val, val.get_rect(center=(cx, base_y+38)))

        draw_column(0, "ŞEHİR", eq["yer"])
        draw_column(1, "ZAMAN", f"{eq['tarih']} {eq['saat']}")
        draw_column(2, "BÜYÜKLÜK", f"{eq['mw']} Mw")

        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()
