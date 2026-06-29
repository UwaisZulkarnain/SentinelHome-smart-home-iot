from gtts import gTTS
import os

warnings = {
    "class1_bm": "Perhatian. Keadaan tidak selesa dikesan. Sila semak persekitaran anda.",
    "class1_en": "Attention. Comfort alert detected. Please check your environment.",
    "class2_bm": "Amaran. Situasi membimbangkan dikesan. Sila ambil tindakan segera.",
    "class2_en": "Warning. Concerning situation detected. Please take action immediately.",
    "class3_bm": "Bahaya! Keadaan berbahaya dikesan! Sila keluar dari kawasan ini sekarang!",
    "class3_en": "Danger! Hazardous condition detected! Please evacuate the area immediately!",
}

os.makedirs("warnings", exist_ok=True)
for name, text in warnings.items():
    path = f"warnings/{name}.mp3"
    gTTS(text=text, lang='ms' if name.endswith('_bm') else 'en').save(path)
    print(f"[OK] {path}")

print("Done.")