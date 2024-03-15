# SLIT -- a Stack Language Intended for Training
# SLIT main file
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from math  import sqrt, isclose
from lexer import Lexer, Token, Instruction

def loop_until_else(tokens: list[Instruction], idx: int) -> int:
    idx += 1

    token: Token = tokens[idx].token
    sif_stack: list[bool] = []
    
    while idx < len(tokens):
        token = tokens[idx].token

        if token == Token.ELSE:
            if sif_stack:
                sif_stack.pop()
            else:
                break

        elif token in (Token.IFEQ, Token.IFNEQ, Token.IFLT, Token.IFLET, Token.IFGT, Token.IFGET):
            sif_stack.append(True)
        
        idx += 1

    return idx

def loop_until_endif(tokens: list[Instruction], idx: int) -> int:
    idx += 1

    token: Token = tokens[idx].token
    sif_stack: list[bool] = []
    
    while idx < len(tokens):
        token = tokens[idx].token

        if token == Token.ENDIF:
            if sif_stack:
                sif_stack.pop()
            else:
                break

        elif token in (Token.IFEQ, Token.IFNEQ, Token.IFLT, Token.IFLET, Token.IFGT, Token.IFGET):
            sif_stack.append(True)

        idx += 1
    
    return idx

def interpret(tokens: list[Instruction]) -> None:
    stack: list = []
    if_stack: list = []

    t_idx: int = 0

    while t_idx < len(tokens):
        token: Token = tokens[t_idx].token
        value = tokens[t_idx].value

        if token in (Token.PUSHN, Token.PUSHS):
            stack.append(value)

        elif token == Token.POP:
            stack.pop()
        elif token == Token.CLEAR:
            stack.clear()

        elif token == Token.ADD:
            b: float = stack.pop()
            a: float = stack.pop()

            stack.append(a + b)
        elif token == Token.SUB:
            b: float = stack.pop()
            a: float = stack.pop()

            stack.append(a - b)
        elif token == Token.MUL:
            b: float = stack.pop()
            a: float = stack.pop()

            stack.append(a * b)
        elif token == Token.DIV:
            b: float = stack.pop()
            a: float = stack.pop()

            stack.append(a / b)
        
        elif token == Token.SQRT:
            stack.append(sqrt(stack.pop()))
        elif token == Token.POW:
            b: float = stack.pop()
            a: float = stack.pop()

            stack.append(a ** b)
        
        elif token == Token.IFEQ:
            if isclose(stack[-1], value):
                t_idx += 1
                if_stack.append(True)
                continue
            
            t_idx = loop_until_else(tokens, t_idx)

        elif token == Token.ELSE:
            if if_stack:
                if_stack.pop()
                t_idx = loop_until_endif(tokens, t_idx)

        elif token == Token.ENDIF:
            pass

        elif token == Token.PUT:
            print(stack[-1] if stack else "Empty stack")
        elif token == Token.DUMP:
            print(stack if stack else "Empty stack")

        t_idx += 1

def main() -> None:
    lexer: Lexer = None

    with open('./ex.slit') as f:
        lexer = Lexer(f.readlines())
    
    lexer.add_rule('pushn (\d+)'    , Token.PUSHN)
    lexer.add_rule('pushs \"(\w+)\"', Token.PUSHS)

    lexer.add_rule('pop', Token.POP)
    lexer.add_rule('clear', Token.CLEAR)

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
    lexer.add_rule('dump', Token.DUMP)
    
    tokens: list[Instruction] = lexer.lex()
    interpret(tokens)

if __name__ == '__main__':
    main()
