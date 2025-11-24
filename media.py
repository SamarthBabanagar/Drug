#!/usr/bin/env python3
# media.py
"""
Build/normalize media.json so each media folder (media/<drugX>) has an entry.
Behavior:
 - If media.json already lists image/video/audio items for a folder, those are normalized (basename + prefix).
 - If a list is missing or empty, the script will scan the corresponding folder for files
   and populate image/video/audio lists automatically based on file extensions.
 - youtube entries are preserved as-is.
 - Ensures every subfolder under media/ has a corresponding key in media.json (with lists).
 - Creates a backup media.json.bak before overwriting.
"""

import json
from pathlib import Path
import shutil
import sys

# Config: file extensions (lowercase) to recognize
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.m4a', '.flac'}
VIDEO_EXTS = {'.mp4', '.webm', '.mov', '.mkv', '.avi'}

PROJECT_ROOT = Path('.')
MEDIA_JSON = PROJECT_ROOT / 'media.json'
MEDIA_DIR = PROJECT_ROOT / 'media'

if not MEDIA_JSON.exists():
    sys.exit("media.json not found in current directory.")
if not MEDIA_DIR.exists():
    sys.exit("media/ directory not found in current directory.")

# make backup
bak = MEDIA_JSON.with_suffix('.json.bak')
shutil.copy2(MEDIA_JSON, bak)
print(f"Backup created: {bak}")

# load existing JSON
try:
    data = json.loads(MEDIA_JSON.read_text(encoding='utf-8'))
except Exception as e:
    sys.exit(f"Failed to read/parse media.json: {e}")

# discover all folder names under media/ (only directories)
folders = [p.name for p in MEDIA_DIR.iterdir() if p.is_dir()]
folders.sort()

out = {}

def scan_folder_for_media(folder_path: Path):
    """Return dict with lists 'images','videos','audio' found in folder (as basenames)."""
    images, videos, audio = [], [], []
    for p in sorted(folder_path.iterdir()):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext in IMAGE_EXTS:
            images.append(p.name)
        elif ext in AUDIO_EXTS:
            audio.append(p.name)
        elif ext in VIDEO_EXTS:
            videos.append(p.name)
        else:
            # ignore unknown extensions by default
            pass
    return {'images': images, 'videos': videos, 'audio': audio}

# Process each real folder: prefer JSON lists if non-empty, else scan the folder
for folder in folders:
    folder_path = MEDIA_DIR / folder
    entry = data.get(folder, {})  # may be {} if missing
    new = {}

    # For each kind, check json list; if provided and non-empty -> normalize it.
    # Otherwise scan the folder and populate from real files.
    for kind in ('images', 'videos', 'audio'):
        json_items = (entry.get(kind) or [])  # ensure list or []
        if json_items:
            # normalize each item to basename then prefix media/<folder>/
            normalized = []
            for item in json_items:
                basename = Path(item).name
                normalized.append(f"media/{folder}/{basename}")
            new[kind] = normalized
        else:
            # json list empty or missing -> scan folder for files of this kind
            scanned = scan_folder_for_media(folder_path)
            names = scanned.get(kind, [])
            normalized = [f"media/{folder}/{name}" for name in names]
            new[kind] = normalized

    # youtube: preserve existing (could be urls) or empty list
    new['youtube'] = entry.get('youtube', []) or []

    out[folder] = new

# Preserve any JSON-only keys (those with no matching folder on disk), normalize them
for key, entry in data.items():
    if key not in out:
        print(f"Preserving JSON-only key (no folder found): {key}")
        new = {}
        for kind in ('images', 'videos', 'audio'):
            items = entry.get(kind, []) or []
            normalized = [f"media/{key}/{Path(i).name}" for i in items]
            new[kind] = normalized
        new['youtube'] = entry.get('youtube', []) or []
        out[key] = new

# Ensure keys are sorted for nicer output (optional)
ordered = {k: out[k] for k in sorted(out.keys())}

# Write back
MEDIA_JSON.write_text(json.dumps(ordered, indent=2, ensure_ascii=False), encoding='utf-8')
print("media.json updated with normalized paths and entries for all media/* folders.")
