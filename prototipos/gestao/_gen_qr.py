"""Gera QR Code do GitHub Pages URL pra usar no slide demo."""
import qrcode
from pathlib import Path

URL = "https://cronos-locaweb.netlify.app/"
OUT = Path(__file__).parent / "qr.png"

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=20,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(fill_color="#0A0F1A", back_color="white")
img.save(str(OUT))
print(f"QR salvo: {OUT}  ({OUT.stat().st_size / 1024:.1f} KB)")
