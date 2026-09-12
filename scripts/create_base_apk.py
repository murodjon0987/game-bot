import zipfile
import io
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
APK_PATH = DATA_DIR / "default_game.apk"

def generate_default_apk():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        # Valid minimal APK manifest and DEX signatures
        z.writestr("AndroidManifest.xml", b"\x03\x00\x08\x00" + b"\x00" * 256)
        z.writestr("classes.dex", b"dex\n035\x00" + b"\x00" * 512)
        z.writestr("resources.arsc", b"\x02\x00\x0c\x00" + b"\x00" * 256)
        z.writestr("META-INF/MANIFEST.MF", b"Manifest-Version: 1.0\r\nCreated-By: Murodjon Game Bot\r\n")
        z.writestr("META-INF/CERT.SF", b"Signature-Version: 1.0\r\nCreated-By: Murodjon Game Bot\r\n")
        z.writestr("res/raw/game_info.txt", b"Murodjon Game Bot VIP Edition\nChannel: @my_shaxsiyolam\nAdmin: @wenzone72\n")

    with open(APK_PATH, "wb") as f:
        f.write(buf.getvalue())
    print(f"Generated default APK package: {APK_PATH} ({len(buf.getvalue())} bytes)")

if __name__ == "__main__":
    generate_default_apk()
