"""Isola a pessoa, aumenta o contraste local e compõe em branco.

Uso: python scripts/prep_photo.py [foto]
A saída é assets/source-prepped.png. A foto original não entra no Git.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PHOTO = ROOT / "assets" / "source-photo.jpg"
PREPPED = ROOT / "assets" / "source-prepped.png"


def prep(photo: Path, dest: Path) -> None:
    import cv2
    import numpy as np
    from PIL import Image
    from rembg import remove

    source = Image.open(photo).convert("RGBA")
    cut = remove(source)
    arr = np.array(cut)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3].astype(np.float32) / 255.0

    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    lightness, green_red, blue_yellow = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    boosted = cv2.merge((clahe.apply(lightness), green_red, blue_yellow))
    rgb = cv2.cvtColor(boosted, cv2.COLOR_LAB2RGB)

    white = np.full_like(rgb, 255)
    mask = alpha[..., None]
    flat = rgb.astype(np.float32) * mask + white.astype(np.float32) * (1.0 - mask)
    dest.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(flat.astype(np.uint8), mode="RGB").save(dest)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepara a foto para o retrato ASCII.")
    parser.add_argument("photo", nargs="?", default=str(DEFAULT_PHOTO))
    args = parser.parse_args()
    photo = Path(args.photo)
    if not photo.is_file():
        raise SystemExit(f"foto não encontrada: {photo}")
    prep(photo, PREPPED)
    print(PREPPED)


if __name__ == "__main__":
    main()
