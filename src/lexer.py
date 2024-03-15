# SLIT -- A Stack Language Intended for Training
# SLIT Lexer
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from enum import Enum, auto
import re

class Token(Enum):
    """All possible token values"""
    
    # Debug directives
    STEP  = auto() # Prints line number + stack at every instruction

    # Stack manipulation
    PUSHN = auto() # Push a number onto the stack
    PUSHS = auto() # Push a string onto the stack

    POP   = auto() # Pop off of the stack
    CLEAR = auto() # Clears the stack

    # Arithmetic
    ADD   = auto() # Add the top 2 numbers on the stack
    SUB   = auto() # Subtract the top 2 numbers on the stack
    MUL   = auto() # Multiply the top 2 numbers on the stack
    DIV   = auto() # Divide the top 2 numbers on the stack

    SQRT  = auto() # Square root of top 2 numbers
    POW   = auto() # Last number on the stack to the power of the second to last number

    # Conditionals
    IFEQ  = auto() # If equal to
    IFNEQ = auto() # If not equal to
    IFLT  = auto() # If less than
    IFLET = auto() # If less than or equal to
    IFGT  = auto() # If greater than
    IFGET = auto() # If greater than or equal to

    ELSE  = auto() # Else
    ENDIF = auto() # Ends a conditional expression
    
    # IO
    PUT   = auto() # Put on the screen
    DUMP  = auto() # Dumps the stack state to the screen

CONDITIONAL_TOKENS: tuple[Token] = (
    Token.IFEQ, Token.IFNEQ,
    Token.IFLT, Token.IFLET,
    Token.IFGT, Token.IFGET
)

class Instruction:
    def __init__(self: Instruction, token: Token) -> None:
        self.token = token
        self.value = None
    
    def __str__(self: Instruction) -> str:
        return f'TK: {self.token:15} | VL: {self.value}'

    def __repr__(self: Instruction) -> str:
        return self.__str__()

class InstructionNumber(Instruction):
    def __init__(self: InstructionNumber, token: Token, value: float) -> None:
        super().__init__(token)
        self.value = value

class InstructionString(Instruction):
    def __init__(self: InstructionString, token: Token, value: str) -> None:
        super().__init__(token)
        self.value = value

class Lexer:
    def __init__(self: Lexer, program: list[str]) -> None:
        self.__program = program
        self.__rules = []
    
    def add_rule(self: Lexer, rule: str, token: Token) -> None:
        self.__rules.append((rule, token))

    def __lex_line(self: Lexer, line: str) -> Instruction:
        for rule, tk in self.__rules:
            result = re.compile(rule).match(line)
            if not result:
                continue

            try:
                value = result.group(1)

                if value.isdigit():
                    return InstructionNumber(tk, float(value))

                return InstructionString(tk, value)
            except:
                return Instruction(tk)

    def lex(self: Lexer) -> list[Instruction]:
        self.__tokenized = []

        for line in self.__program:
            line = line.strip()

            if line[0] == '#':
                continue

            self.__tokenized.append(
                self.__lex_line(line)
            )

        return self.__tokenized
