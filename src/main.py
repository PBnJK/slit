# SLIT -- a Stack Language Intended for Training
# SLIT main file
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from math  import sqrt, isclose
from lexer import Lexer, Token

def interpret(tokens: list[Instruction]) -> None:
    stack: list = []

    for t in tokens:
        token: Token = t.token
        value = t.value

        if token in (Token.PUSHN, Token.PUSHS):
            stack.append(value)
        elif token == Token.POP:
            stack.pop()

        elif token == Token.ADD:
            stack.append(stack.pop() + stack.pop())
        elif token == Token.SUB:
            stack.append(stack.pop() - stack.pop())
        elif token == Token.MUL:
            stack.append(stack.pop() * stack.pop())
        elif token == Token.DIV:
            stack.append(stack.pop() / stack.pop())
        elif token == Token.SQRT:
            stack.append(sqrt(stack.pop()))
        elif token == Token.POW:
            stack.append(stack.pop() ** stack.pop())

        elif token == Token.PUT:
            print(stack[-1])

def main() -> None:
    lexer: Lexer = None

    with open('ex.slit') as f:
        lexer = Lexer(f.readlines())
    
    lexer.add_rule('pushn (\d+)'    , Token.PUSHN)
    lexer.add_rule('pushs \"(\w+)\"', Token.PUSHS)

    lexer.add_rule('pop', Token.POP)

    lexer.add_rule('add', Token.ADD)
    lexer.add_rule('sub', Token.SUB)
    lexer.add_rule('div', Token.DIV)
    lexer.add_rule('mul', Token.MUL)

    lexer.add_rule('sqrt', Token.SQRT)
    lexer.add_rule('pow', Token.POW)

    lexer.add_rule('ifeq (\d+)' , Token.IFEQ)
    lexer.add_rule('ifneq (\d+)', Token.IFNEQ)
    lexer.add_rule('iflt (\d+)' , Token.IFLT)
    lexer.add_rule('iflet (\d+)', Token.IFLET)
    lexer.add_rule('ifgt (\d+)' , Token.IFGT)
    lexer.add_rule('ifget (\d+)', Token.IFGET)

    lexer.add_rule('else' , Token.ELSE)
    lexer.add_rule('endif', Token.ENDIF)

    lexer.add_rule('put', Token.PUT)
    
    tokens: list[Instruction] = lexer.lex()
    interpret(tokens)

if __name__ == '__main__':
    main()
