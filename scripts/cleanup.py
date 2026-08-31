from pathlib import Path


def cleanup_raw(max_files: int = 1000) -> int:
    raw = Path("data/raw")
    files = sorted([p for p in raw.glob("*") if p.is_file()], key=lambda p: p.stat().st_mtime)
    removed = 0
    while len(files) > max_files:
        files.pop(0).unlink(missing_ok=True)
        removed += 1
    return removed


if __name__ == "__main__":
    print(f"Removed {cleanup_raw()} old raw data files")
