# SLIT -- a Stack Language Intended for Training
# SLIT main file
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from lexer import Lexer, Token
from vm import VirtualMachine

VAR_OR_NUM: str = r'(\d+|[a-zA-Z_][a-zA-Z_0-9]?$)'

def main() -> None:
    lexer: Lexer = None

    with open('ex.slit', encoding="utf-8") as f:
        lexer = Lexer(f.readlines())
    
    lexer.add_rule('step', Token.STEP)
    lexer.add_rule('quit(?: (\d+))?', Token.QUIT)

    lexer.add_rule(f'pushn {VAR_OR_NUM}'  , Token.PUSHN)
    lexer.add_rule('pushs "(\D+)"', Token.PUSHS)

    lexer.add_rule('pop', Token.POP)
    lexer.add_rule('clear', Token.CLEAR)

    lexer.add_rule('swap', Token.SWAP)
    lexer.add_rule('dup', Token.DUP)

    lexer.add_rule('add|\+', Token.ADD)
    lexer.add_rule('sub|\-', Token.SUB)
    lexer.add_rule('div|\/', Token.DIV)
    lexer.add_rule('mul|\*', Token.MUL)

    lexer.add_rule('mod|\%', Token.MOD)

    lexer.add_rule('sqrt', Token.SQRT)
    lexer.add_rule('pow|\^', Token.POW)

    lexer.add_rule('sind', Token.SIND)
    lexer.add_rule('sinr', Token.SINR)

    lexer.add_rule('cosd', Token.COSD)
    lexer.add_rule('cosr', Token.COSR)

    lexer.add_rule('tand', Token.TAND)
    lexer.add_rule('tanr', Token.TANR)

    lexer.add_rule(f'(?:ifeq |== ){VAR_OR_NUM}' , Token.IFEQ)
    lexer.add_rule(f'(?:ifneq |!= ){VAR_OR_NUM}', Token.IFNEQ)
    lexer.add_rule(f'(?:iflt |< ){VAR_OR_NUM}'  , Token.IFLT)
    lexer.add_rule(f'(?:iflet |<= ){VAR_OR_NUM}', Token.IFLET)
    lexer.add_rule(f'(?:ifgt |> ){VAR_OR_NUM}'  , Token.IFGT)
    lexer.add_rule(f'(?:ifget |>= ){VAR_OR_NUM}', Token.IFGET)

    lexer.add_rule('strcmp' , Token.STRCMP)

    lexer.add_rule('else' , Token.ELSE)
    lexer.add_rule('endif', Token.ENDIF)
    
    lexer.add_rule('loop', Token.LOOP)
    lexer.add_rule('eloop', Token.ENDLOOP)

    lexer.add_rule('break', Token.BREAK)
    lexer.add_rule('rerun', Token.RERUN)

    lexer.add_rule('put$', Token.PUT)
    lexer.add_rule('putraw', Token.PUTRAW)

    lexer.add_rule('dump', Token.DUMP)

    lexer.add_rule('print "(.+)"', Token.PRINT)

    lexer.add_rule('read', Token.READ)
    lexer.add_rule('anykey', Token.ANYKEY)

    lexer.add_rule('(^[a-zA-Z_][a-zA-Z_0-9]?)= (\d+)', Token.DECL)

    vm: VirtualMachine = VirtualMachine(lexer.lex())
    vm.interpret()

if __name__ == '__main__':
    main()
