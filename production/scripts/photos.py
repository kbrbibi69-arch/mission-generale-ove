"""Prépare les photographies fournies : agrandissement Lanczos ×2 (le panneau à l'écran fait ~1,65× la source)
et détourage du ciel (zone claire et désaturée reliée au bord supérieur) pour une mise en profondeur multicouche.
Aucun traitement colorimétrique : seuls la taille et la couche alpha changent."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PJ = os.path.join(ROOT, "production", "pieces-jointes")
OUT = os.path.join(ROOT, "assets", "img", "photos")
os.makedirs(OUT, exist_ok=True)

def sky_cutout(src, name, xmax):
    im = Image.open(os.path.join(PJ, src)).convert("RGB")
    a = np.asarray(im).astype(int)
    cand = Image.fromarray((((a.mean(2) > 170) & ((a.max(2) - a.min(2)) < 28)) * 255).astype(np.uint8)).copy()
    for x in range(0, min(xmax, im.width), 4):
        if cand.getpixel((x, 0)) == 255:
            ImageDraw.floodfill(cand, (x, 0), 128)
    sky = np.asarray(cand) == 128
    sky[:, xmax:] = False                      # reflets des vitrages et végétation en toiture : conservés
    alpha = Image.fromarray(((~sky) * 255).astype(np.uint8))
    big = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    alpha = alpha.resize(big.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
    big.save(os.path.join(OUT, name + ".jpg"), quality=93)
    rgba = big.copy(); rgba.putalpha(alpha)
    rgba.save(os.path.join(OUT, name + "-detoure.png"), optimize=True)
    print(name, big.size, f"ciel {sky.mean():.0%}")

sky_cutout("PJ02-photo-batiment-non-identifie.webp", "batiment", 300)
