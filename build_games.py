"""
Baut die Original-Python-Spiele mit pygbag für den Browser.
PU-Projekt-Dateien bleiben unverändert — nur Kopien werden angepasst.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from webify import webify

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
    ("pacman", "pacman game.py"),
    ("zahl", "Zahl_raten.py"),
]

BACK_BAR = """
<div id="pu-bar" style="position:fixed;top:0;left:0;right:0;z-index:99999;display:flex;align-items:center;gap:12px;padding:10px 14px;background:rgba(10,10,15,0.95);border-bottom:1px solid rgba(255,255,255,0.12);font-family:Outfit,system-ui,sans-serif;">
  <a href="../../index.html" style="color:#00f5d4;font-weight:700;text-decoration:none;">← Arcade</a>
  <span style="color:#9b9bb8;font-size:13px;">Echtes Python · 1. Mal ~30–60 Sek. laden · dann auf Seite tippen</span>
</div>
<style>body { padding-top: 48px !important; }</style>
"""


def patch_index(html_path: Path) -> None:
    text = html_path.read_text(encoding="utf-8")
    text = text.replace(
        "if platform.window.location.host.find('.itch.zone')>0:",
        "if True:  # .apk für GitHub Pages",
    )
    if "pu-bar" not in text:
        text = text.replace("<body", BACK_BAR + "<body", 1)
    html_path.write_text(text, encoding="utf-8")


def build_one(game_id: str, source_name: str) -> bool:
    src_file = PU / source_name
    if not src_file.exists():
        print(f"  SKIP {game_id}: {source_name} fehlt")
        return False

    SOURCES.mkdir(exist_ok=True)
    safe = source_name.replace(" ", "_")
    shutil.copy2(src_file, SOURCES / safe)

    work = BUILD / game_id
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    original = src_file.read_text(encoding="utf-8")
    web_code = webify(original, game_id)
    (work / "main.py").write_text(web_code, encoding="utf-8")

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
        timeout=300,
    )
    if r.returncode != 0:
        print((r.stderr or r.stdout)[-2000:])
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

    # APK-Größe prüfen
    apks = list(out.glob("*.apk"))
    if apks and apks[0].stat().st_size < 500:
        print(f"  WARN {game_id}: APK sehr klein ({apks[0].stat().st_size} B)")

    patch_index(out / "index.html")
    print(f"  OK {game_id}")
    return True


def main() -> None:
    PLAY.mkdir(exist_ok=True)
    ok = sum(1 for gid, fn in GAMES if build_one(gid, fn))
    print(f"\nFertig: {ok}/{len(GAMES)} -> {PLAY}")


if __name__ == "__main__":
    main()
