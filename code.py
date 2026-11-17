# Turns birthday.html + photos/ into ONE self-contained file: birthday-share.html
import base64, io, re, pathlib
try:
    from PIL import Image, ImageOps   # optional: shrinks photos so the file stays small
except ImportError:
    Image = None

def data_uri(path):
    p = pathlib.Path(path)
    if Image:
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        im.thumbnail((1100, 1100))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=80)
        raw, mime = buf.getvalue(), "image/jpeg"
    else:
        raw = p.read_bytes()
        mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())

def swap(m):
    return 'src: "%s"' % data_uri(m.group(1)) if pathlib.Path(m.group(1)).exists() else m.group(0)

html = pathlib.Path("birthday.html").read_text(encoding="utf-8")
pathlib.Path("birthday-share.html").write_text(re.sub(r'src:\s*"(photos/[^"]+)"', swap, html), encoding="utf-8")
print("Done -> birthday-share.html")
