#!/usr/bin/env python3
"""Prepare uploaded photography: python3 build/prepare_images.py (requires Pillow)."""
import json
from pathlib import Path
from PIL import Image, ImageOps
from photos import UPLOADED_PHOTOS

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'assets/img/photos'


def main():
    manifest = {}
    for name, (source, _) in UPLOADED_PHOTOS.items():
        with Image.open(ROOT / source) as original:
            image = ImageOps.exif_transpose(original).convert('RGB')
            image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
            width, height = image.size
            image.save(DEST / f'{name}.webp', 'WEBP', quality=82, method=6)
            small = image.copy()
            small.thumbnail((900, 900), Image.Resampling.LANCZOS)
            small.save(DEST / f'{name}-sm.webp', 'WEBP', quality=80, method=6)
            manifest[name] = {'width': width, 'height': height, 'small_width': small.width}
    # Record the original library too: its images do not all share a 3:2 ratio.
    for path in sorted(DEST.glob('*.webp')):
        if path.stem.endswith('-sm'):
            continue
        with Image.open(path) as full, Image.open(path.with_name(path.stem + '-sm.webp')) as small:
            manifest[path.stem] = {'width': full.width, 'height': full.height, 'small_width': small.width}
    (DEST / 'uploaded.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Prepared {len(UPLOADED_PHOTOS)} uploads; recorded {len(manifest)} image dimensions.')


if __name__ == '__main__':
    main()
