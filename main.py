import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "output"
sys.path.insert(0, str(ROOT / "lib"))

NEED = ("W", "H", "FPS", "DUR", "frame")


def main():
    files = sorted(SRC.glob("*.py"))
    if len(files) != 1:
        sys.exit(f"src/ harus berisi tepat 1 file .py, ditemukan {len(files)}: {[f.name for f in files]}")
    f = files[0]
    spec = importlib.util.spec_from_file_location(f.stem, f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    missing = [n for n in NEED if not hasattr(mod, n)]
    if missing:
        sys.exit(f"{f.name} belum mendefinisikan: {', '.join(missing)}")
    import kit
    OUT.mkdir(exist_ok=True)
    print(f"Render {f.name}: {mod.W}x{mod.H}, {mod.FPS} fps, {mod.DUR} detik")
    kit.encode(mod.frame, mod.W, mod.H, mod.FPS, mod.DUR, OUT / f"{f.stem}.mp4")


if __name__ == "__main__":
    main()
