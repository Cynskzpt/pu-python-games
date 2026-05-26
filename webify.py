"""
Macht Kopien der Original-.py-Dateien pygbag-tauglich (async).
Die Dateien im PU-Projekt-Ordner bleiben unverändert.
"""
from __future__ import annotations

import re
from pathlib import Path

WEB_VERSIONS = Path(__file__).resolve().parent / "web_versions"

# Variablen, die in async main() zugewiesen werden (sonst lokale Kopien → Spiel hängt)
GAME_GLOBALS: dict[str, str] = {
    "flappy": "running, flap_timer, game_active, bird_movement, bird_y, pipes, score, best_score, pipe_spawn_cd",
    "hangman": "running, word, guessed, wrong_guesses, game_over, win, letters",
    "reaction": "running, state, round_number, wait_time, game_start, start_time, reaction_times",
    "tictactoe": "running, player, board, game_over, vs_bot",
    "rps": "running",
    "pacman": "running, player_x, player_y, ghosts, dots, score",
}


def _add_asyncio(code: str) -> str:
    if "import asyncio" in code:
        return code
    lines = code.splitlines(keepends=True)
    pos = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("import ") or s.startswith("from "):
            pos = i + 1
    lines.insert(pos, "import asyncio\n")
    return "".join(lines)


def _sleep_after_ticks(code: str) -> str:
    """await nur im Körper von async def (nicht in normalen def-Hilfsfunktionen)."""

    def repl(m: re.Match) -> str:
        ind, stmt = m.group(1), m.group(2)
        return f"{ind}{stmt}\n{ind}await asyncio.sleep(0)"

    lines = code.splitlines(keepends=True)
    out: list[str] = []
    in_async = False
    for line in lines:
        if re.match(r"^async def ", line):
            in_async = True
        elif in_async and re.match(r"^def ", line):
            in_async = False
        elif in_async and line.strip() and not line[0].isspace():
            if not line.startswith("asyncio.run"):
                in_async = False
        out.append(line)
        if in_async and re.match(r"^(\s*)clock\.tick\([^)]*\)\s*$", line):
            ind = re.match(r"^(\s*)", line).group(1)
            out.append(f"{ind}await asyncio.sleep(0)\n")
    return "".join(out)


def _sleep_after_display(code: str) -> str:
    """pygame.display.update nur in async def — vermeidet SyntaxError in draw_lost_message etc."""

    lines = code.splitlines(keepends=True)
    out: list[str] = []
    in_async = False
    for line in lines:
        if re.match(r"^async def ", line):
            in_async = True
        elif in_async and re.match(r"^def ", line):
            in_async = False
        elif in_async and line.strip() and not line[0].isspace():
            if not line.startswith("asyncio.run"):
                in_async = False
        out.append(line)
        if in_async and re.search(r"pygame\.display\.(?:update|flip)\(\)", line):
            ind = re.match(r"^(\s*)", line).group(1)
            out.append(f"{ind}await asyncio.sleep(0)\n")
    return "".join(out)


def _strip_tail(code: str) -> str:
    code = re.sub(r"^if __name__ == ['\"]__main__['\"]:\s*\n\s*main\(\)\s*\n?", "", code, flags=re.M)
    code = re.sub(r"^start_game\(\)\s*\n?", "", code, flags=re.M)
    code = re.sub(r"^pygame\.quit\(\)\s*\n?", "", code, flags=re.M)
    code = re.sub(r"^sys\.exit\(\)\s*\n?", "", code, flags=re.M)
    return code


def _indent_block(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "".join(pad + line if line.strip() else line for line in text.splitlines(keepends=True))


def _globals_footer(game_id: str) -> str:
    names = GAME_GLOBALS.get(game_id, "running")
    return f"    global {names}\n"


def _wrap_module_while(code: str, game_id: str) -> str:
    m = re.search(r"^while\s+.+:\s*$", code, flags=re.M)
    if not m:
        return code
    head, tail = code[: m.start()], code[m.start() :]
    tail = _strip_tail(tail)
    tail = _sleep_after_ticks(tail)
    tail = _sleep_after_display(tail)
    tail = re.sub(
        r"pygame\.time\.delay\((\d+)\)",
        r"await asyncio.sleep(\1 / 1000)",
        tail,
    )
    tail = re.sub(
        r"if event\.type == pygame\.QUIT:\s*\n\s*pygame\.quit\(\)\s*\n\s*sys\.exit\(\)",
        "if event.type == pygame.QUIT:\n            running = False",
        tail,
    )
    extra = _globals_footer(game_id)
    if game_id in ("hangman", "reaction", "tictactoe", "rps"):
        extra += "    running = True\n"
    return head + "async def main():\n" + extra + _indent_block(tail, 4) + "\nasyncio.run(main())\n"


def _fix_flappy(code: str) -> str:
    code = re.sub(
        r"SPAWNPIPE = pygame\.USEREVENT\s*\npygame\.time\.set_timer\(SPAWNPIPE, \d+\)\s*\n",
        "",
        code,
    )
    if "pipe_spawn_cd = 0" not in code:
        code = code.replace(
            "running = True\nflap_timer = 0",
            "running = True\nflap_timer = 0\npipe_spawn_cd = 0",
        )
    code = code.replace(
        "        flap_timer += 1\n",
        "        flap_timer += 1\n"
        "        pipe_spawn_cd += 1\n"
        "        if pipe_spawn_cd >= 84 and game_active:\n"
        "            pipe_spawn_cd = 0\n"
        "            pipes.extend(create_pipe())\n",
    )
    code = re.sub(
        r"\s*if event\.type == SPAWNPIPE and game_active:\s*\n\s*pipes\.extend\(create_pipe\(\)\)\s*\n",
        "\n",
        code,
    )
    return code


def _fix_tetris_draw_lost(code: str) -> str:
    """draw_lost_message: kein await in sync def; Verzögerung im Hauptloop."""
    code = re.sub(
        r"def draw_lost_message\(\):.*?pygame\.time\.delay\(\d+\)\s*\n",
        "def draw_lost_message():\n"
        "    label = font.render('You lost!', True, white)\n"
        "    screen.blit(label, (width // 2 - label.get_width() // 2, height // 2 - label.get_height() // 2))\n"
        "    pygame.display.update()\n\n",
        code,
        flags=re.DOTALL,
    )
    # await in draw_lost_message entfernen (falls von alter webify-Version)
    code = re.sub(
        r"(def draw_lost_message\(\):.*?)\n\s*await asyncio\.sleep\([^)]+\)\s*\n",
        r"\1\n",
        code,
        flags=re.DOTALL,
    )
    if "await asyncio.sleep(1.5)" not in code:
        code = code.replace(
            "            draw_lost_message()  # Muestra el mensaje de \"Perdiste\"\n"
            "            run = False  # Termina el juego",
            "            draw_lost_message()\n"
            "            await asyncio.sleep(1.5)\n"
            "            run = False\n",
        )
    return code


def webify(code: str, game_id: str) -> str:
    if game_id == "zahl":
        return (WEB_VERSIONS / "zahl_pygame.py").read_text(encoding="utf-8")

    code = _add_asyncio(code)
    code = _strip_tail(code)

    if game_id == "snake":
        code = code.replace("def start_game():", "async def main():")
        code = _sleep_after_ticks(code)
        if "asyncio.run(main())" not in code:
            code += "\nasyncio.run(main())\n"
        return code

    if game_id == "tetris":
        code = code.replace("def main():", "async def main():")
        code = _sleep_after_ticks(code)
        code = _sleep_after_display(code)
        code = _fix_tetris_draw_lost(code)
        if "asyncio.run(main())" not in code:
            code += "\nasyncio.run(main())\n"
        return code

    if game_id in ("flappy", "hangman", "pacman", "reaction", "tictactoe", "rps"):
        if game_id in ("tictactoe", "rps"):
            code = code.replace("while True:", "while running:")
        code = _wrap_module_while(code, game_id)
        if game_id == "flappy":
            code = _fix_flappy(code)
        return code

    return _wrap_module_while(code, game_id)
