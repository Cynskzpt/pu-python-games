"""
Baut Python-Spiele mit pygbag (--archive) für GitHub Pages.
Originale im PU-Projekt bleiben unverändert — hier werden Kopien gebaut.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PU = ROOT.parent
PLAY = ROOT / "play"
SOURCES = ROOT / "sources"
BUILD = ROOT / "_build"

GAMES = [
    ("snake", "snake game.py"),
    ("tetris", "tetris3.py"),
    ("flappy", "flappy bird.py"),
    ("hangman", "Hangman.py"),
    ("tictactoe", "tic tac toe.py"),
    ("rps", "rock paper scissors2.py"),
    ("reaction", "reaction time test.py"),
    ("pacman", "pacman.py"),
    ("zahl", "Zahl_raten.py"),
]

BACK_BAR = """
<div id="pu-bar" style="position:fixed;top:0;left:0;right:0;z-index:99999;display:flex;align-items:center;gap:12px;padding:10px 14px;background:rgba(10,10,15,0.92);border-bottom:1px solid rgba(255,255,255,0.12);font-family:system-ui,sans-serif;">
  <a href="../../index.html" style="color:#00f5d4;font-weight:700;text-decoration:none;">← Arcade</a>
  <span style="color:#9b9bb8;font-size:14px;">Python · Klick ins Spiel · ggf. kurz laden</span>
</div>
<style>body { padding-top: 48px !important; }</style>
"""


def patch_index(html_path: Path) -> None:
    text = html_path.read_text(encoding="utf-8")
    # GitHub Pages: nur .apk liegt vor, nicht .tar.gz (sonst endloses Loading)
    text = text.replace(
        "if platform.window.location.host.find('.itch.zone')>0:",
        "if True:  # .apk für Web-Hosting",
    )
    if "pu-bar" not in text:
        text = text.replace("<body", BACK_BAR + "<body", 1)
    html_path.write_text(text, encoding="utf-8")


def build_one(game_id: str, source_name: str) -> bool:
    src_file = PU / source_name
    if not src_file.exists():
        print(f"  SKIP {game_id}: {source_name} nicht gefunden")
        return False

    SOURCES.mkdir(exist_ok=True)
    safe = source_name.replace(" ", "_")
    shutil.copy2(src_file, SOURCES / safe)

    work = BUILD / game_id
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    code = src_file.read_text(encoding="utf-8")
    (work / "main.py").write_text(code, encoding="utf-8")

    if game_id == "pacman":
        import freegames

        fg = Path(freegames.__file__).parent
        shutil.copytree(fg, work / "freegames")

    print(f"  BUILD {game_id} ...")
    env = {**dict(__import__("os").environ), "PYTHONUTF8": "1"}
    r = subprocess.run(
        [sys.executable, "-m", "pygbag", "--archive", "."],
        cwd=work,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=180,
    )
    if r.returncode != 0:
        print((r.stderr or r.stdout)[-1500:])
        return False

    zpath = work / "build" / "web.zip"
    if not zpath.exists():
        print(f"  FAIL {game_id}: keine web.zip")
        return False

    out = PLAY / game_id
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    with zipfile.ZipFile(zpath, "r") as zf:
        zf.extractall(out)

    patch_index(out / "index.html")
    print(f"  OK {game_id}")
    return True


def main() -> None:
    PLAY.mkdir(exist_ok=True)
    ok = sum(1 for gid, fn in GAMES if build_one(gid, fn))
    print(f"\nFertig: {ok}/{len(GAMES)} -> {PLAY}")


if __name__ == "__main__":
    main()
