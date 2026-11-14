"""Emit the staged Tonkotsu photograph for the food-picture entry.

The picture ships inside this repository as entry.png (JPEG bytes,
1024 by 1024). Running this program drops an exact copy of it where
the grader looks, $MAKEFUN_OUTPUT_DIR/entry.png, after checking the
picture is present, small enough, and really a JPEG. It never touches
the network and never rolls dice, so two runs always write the same
bytes. Standard library only, Python 3.13.
"""

import hashlib
import os
from pathlib import Path

PICTURE = "entry.png"
BYTE_LIMIT = 1024 * 1024
JPEG_HEAD = b"\xff\xd8\xff"
JPEG_TAIL = b"\xff\xd9"


def abort(why):
    print(f"entry failed: {why}", file=__import__("sys").stderr)
    raise SystemExit(1)


def load_picture():
    here = Path(__file__).resolve().parent
    picture_path = here / PICTURE
    if not picture_path.is_file():
        abort(f"bundled picture {PICTURE} is missing from {here}")
    blob = picture_path.read_bytes()
    if len(blob) > BYTE_LIMIT:
        abort(f"picture is {len(blob)} bytes, over the {BYTE_LIMIT} limit")
    if blob[:3] != JPEG_HEAD or blob[-2:] != JPEG_TAIL:
        abort("picture is not a JPEG (bad start or end marker)")
    return blob


def run():
    blob = load_picture()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / PICTURE
    destination.write_bytes(blob)
    written = destination.read_bytes()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(blob).hexdigest():
        abort("written picture does not match the bundled picture")
    print(
        f"wrote {destination} "
        f"({len(written)} bytes, sha256 {hashlib.sha256(written).hexdigest()[:16]}...)"
    )
    return 0


code = run()
raise SystemExit(code)
