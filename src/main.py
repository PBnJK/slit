# SLIT -- a Stack Language Intended for Training
# SLIT main file
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from lexer import Lexer, Token
from vm import VirtualMachine


def main() -> None:
    lexer: Lexer = None

    with open('ex.slit', encoding="utf-8") as f:
        lexer = Lexer(f.readlines())

    vm: VirtualMachine = VirtualMachine(lexer.lex())
    res = vm.interpret()

if __name__ == '__main__':
    main()
