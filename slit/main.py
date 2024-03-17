# SLIT -- a Stack Language Intended for Training
# SLIT main file
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from .vm    import VirtualMachine
from .lexer import Lexer

def run_program(program_path: str) -> int:
    lexer: Lexer = None

    with open(program_path, encoding="utf-8") as f:
        lexer = Lexer(f.readlines())

    vm: VirtualMachine = VirtualMachine(lexer.lex())
    return vm.interpret()

