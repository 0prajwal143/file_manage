# Downloads Folder Organizer
# Organizes Downloads by file type.
# Skips: FORMFOR -- left completely untouched.

import os
import shutil
from pathlib import Path

DOWNLOADS = Path(r"C:\Users\Lenovo\Downloads")

# ── Folder → extensions mapping ──────────────────────────────────────────────
CATEGORIES = {
    "Images":        [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
                      ".webp", ".ico", ".tiff", ".heic", ".raw"],
    "Videos":        [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv",
                      ".webm", ".m4v", ".3gp", ".mpeg"],
    "Audio":         [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma",
                      ".m4a", ".opus", ".aiff"],
    "Documents":     [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
                      ".pptx", ".odt", ".ods", ".odp", ".txt", ".rtf",
                      ".csv", ".epub", ".mobi"],
    "Archives":      [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
                      ".xz", ".iso", ".dmg", ".tar.gz"],
    "Installers":    [".exe", ".msi", ".msix", ".appx", ".deb", ".rpm",
                      ".pkg", ".run"],
    "Code":          [".py", ".js", ".ts", ".html", ".css", ".php",
                      ".java", ".c", ".cpp", ".h", ".cs", ".json",
                      ".xml", ".yaml", ".yml", ".sh", ".bat", ".ps1",
                      ".sql", ".rb", ".go", ".rs", ".kt", ".swift"],
    "Fonts":         [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "Torrents":      [".torrent"],
    "Shortcuts":     [".lnk", ".url"],
}

SKIP_NAMES = {"FORMFOR"}  # Add more names here if needed

def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Misc"

def safe_move(src: Path, dest_folder: Path):
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest = dest_folder / src.name

    # If a file with that name already exists, append a counter
    counter = 1
    while dest.exists():
        dest = dest_folder / f"{src.stem} ({counter}){src.suffix}"
        counter += 1

    shutil.move(str(src), str(dest))
    return dest

def organize():
    if not DOWNLOADS.exists():
        print(f"[ERROR] Folder not found: {DOWNLOADS}")
        return

    moved   = 0
    skipped = 0
    errors  = 0

    for item in list(DOWNLOADS.iterdir()):
        # ── Skip protected names ─────────────────────────────────────────────
        if item.name in SKIP_NAMES:
            print(f"[SKIP]  {item.name}  ← protected, not touched")
            skipped += 1
            continue

        # ── Skip category folders themselves ─────────────────────────────────
        if item.is_dir():
            all_categories = set(CATEGORIES.keys()) | {"Misc"}
            if item.name in all_categories:
                print(f"[SKIP]  {item.name}/  ← organizer folder")
                skipped += 1
                continue
            # Non-category directories → move to "Folders"
            dest = safe_move(item, DOWNLOADS / "Folders")
            print(f"[MOVE]  {item.name}  →  Folders/")
            moved += 1
            continue

        # ── Move files ───────────────────────────────────────────────────────
        try:
            category = get_category(item.suffix)
            dest = safe_move(item, DOWNLOADS / category)
            print(f"[MOVE]  {item.name}  →  {category}/")
            moved += 1
        except Exception as e:
            print(f"[ERR]   {item.name}  — {e}")
            errors += 1

    print(f"\n✓  Done — {moved} moved | {skipped} skipped | {errors} errors")

if __name__ == "__main__":
    print(f"Organizing: {DOWNLOADS}\n")
    organize()
