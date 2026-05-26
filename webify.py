"""
Macht Kopien der Original-.py-Dateien pygbag-tauglich (async).
Die Dateien im PU-Projekt-Ordner bleiben unverändert.
"""
from __future__ import annotations

import re


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
    def repl(m: re.Match) -> str:
        ind, stmt = m.group(1), m.group(2)
        return f"{ind}{stmt}\n{ind}await asyncio.sleep(0)"

    return re.sub(r"^(\s*)(clock\.tick\([^)]*\))", repl, code, flags=re.M)


def _sleep_after_display(code: str) -> str:
    def repl(m: re.Match) -> str:
        ind, stmt = m.group(1), m.group(2)
        return f"{ind}{stmt}\n{ind}await asyncio.sleep(0)"

    return re.sub(
        r"^(\s*)(pygame\.display\.(?:update|flip)\(\))",
        repl,
        code,
        flags=re.M,
    )


def _strip_tail(code: str) -> str:
    code = re.sub(r"^if __name__ == ['\"]__main__['\"]:\s*\n\s*main\(\)\s*\n?", "", code, flags=re.M)
    code = re.sub(r"^start_game\(\)\s*\n?", "", code, flags=re.M)
    code = re.sub(r"^pygame\.quit\(\)\s*\n?", "", code, flags=re.M)
    code = re.sub(r"^sys\.exit\(\)\s*\n?", "", code, flags=re.M)
    return code


def _indent_block(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "".join(pad + line if line.strip() else line for line in text.splitlines(keepends=True))


def _wrap_module_while(code: str, footer_globals: str = "") -> str:
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
    return (
        head
        + "async def main():\n"
        + footer_globals
        + _indent_block(tail, 4)
        + "\nasyncio.run(main())\n"
    )


def webify(code: str, game_id: str) -> str:
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
        if "asyncio.run(main())" not in code:
            code += "\nasyncio.run(main())\n"
        return code

    if game_id == "zahl":
        return _webify_zahl(code)

    if game_id in ("flappy", "hangman", "pacman", "reaction", "tictactoe", "rps"):
        if game_id in ("tictactoe", "rps"):
            code = code.replace("while True:", "while running:")
        extra = ""
        if game_id == "flappy":
            extra = "    global running, flap_timer\n"
        elif game_id in ("hangman", "reaction", "tictactoe", "rps"):
            extra = "    global running\n    running = True\n"
        elif game_id == "pacman":
            extra = "    global running, player_x, player_y, ghosts, dots, score\n"
        return _wrap_module_while(code, extra)

    return _wrap_module_while(code)


def _webify_zahl(code: str) -> str:
    return '''import asyncio
import random

async def main():
    geheime_zahl = random.randint(1, 100)
    moegliche_versuche = 3

    while moegliche_versuche > 0:
        print('Errate die Zahl zwischen 1 und 100')
        print('Du hast', moegliche_versuche, 'Versuche')
        eingabe = await input('Deine Eingabe:')

        try:
            geratene_zahl = int(eingabe)
            if geratene_zahl > 100:
                print('Die Zahl liegt doch unter 100!')
                continue
            if geratene_zahl > geheime_zahl:
                print("Zu hoch! Versuch's nochmal!")
                moegliche_versuche -= 1
            elif geratene_zahl < geheime_zahl:
                print("Zu niedrig! Versuch's nochmal!")
                moegliche_versuche -= 1
            else:
                print('Richtig geraten!')
                return
        except ValueError:
            print('Ganz vergessen.. nur ganze Zahlen bitte!')
            moegliche_versuche -= 1

    print('Leider nicht erraten. Die Zahl war', geheime_zahl)

asyncio.run(main())
'''
