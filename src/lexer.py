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
    QUIT  = auto() # Exits the program with error code

    # Stack manipulation
    PUSHN = auto() # Push a number onto the stack
    PUSHS = auto() # Push a string onto the stack

    POP   = auto() # Pop off of the stack
    CLEAR = auto() # Clears the stack

    SWAP  = auto() # Swaps the top two items
    DUP   = auto() # Duplicates the top item

    # Arithmetic
    ADD   = auto() # Add the top two items on the stack
    SUB   = auto() # Subtract the top two items on the stack
    MUL   = auto() # Multiply the top two items on the stack
    DIV   = auto() # Divide the top two items on the stack

    MOD   = auto() # Modulo the top two items

    SQRT  = auto() # Square root of top two items
    POW   = auto() # Power of top two items
    
    SIND  = auto() # Sine of the top value (in degrees)
    SINR  = auto() # Sine of the top value (in radians)

    COSD  = auto() # Cosine of the top value (in degrees)
    COSR  = auto() # Cosine of the top value (in radians)

    TAND  = auto() # Tangent of the top value (in degrees)
    TANR  = auto() # Tangent of the top value (in radians)

    # Conditionals
    IFEQ  = auto() # If equal to
    IFNEQ = auto() # If not equal to
    IFLT  = auto() # If less than
    IFLET = auto() # If less than or equal to
    IFGT  = auto() # If greater than
    IFGET = auto() # If greater than or equal to

    STRCMP= auto() # Compare strings

    ELSE  = auto() # Else
    ENDIF = auto() # Ends a conditional expression

    # Loops
    LOOP    = auto() # Begin loop
    ENDLOOP = auto() # End loop

    BREAK = auto() # Breaks out of the loop
    RERUN = auto() # Runs the loop back from the beginning (same as continue)
    
    # IO
    PUT    = auto() # Put on the screen
    PUTRAW = auto() # Put on the screen (no newline)

    DUMP   = auto() # Dumps the stack state to the screen

    PRINT  = auto() # Prints a given string to the screen

    READ   = auto() # Reads user input and puts on the stack
    ANYKEY = auto() # Waits for any user key (doesn't push to stack)

    # Variables
    DECL   = auto() # Variable declaration

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

class InstructionVar(Instruction):
    def __init__(self: InstructionString, token: Token, var: str, value: int) -> None:
        super().__init__(token)
        self.var   = var
        self.value = value

class Lexer:
    def __init__(self: Lexer, program: list[str]) -> None:
        self.__program = program
        self.__rules = []
    
    def add_rule(self: Lexer, rule: str, token: Token) -> None:
        self.__rules.append((rule, token))
    
    def __lex_line(self: Lexer, line: str) -> Instruction:
        line = line.strip()

        if (not line) or (line[0] == '#'):
            return None

        for rule, tk in self.__rules:
            result = re.compile(rule).match(line)
            if not result:
                continue

            try:
                value = result.group(1)
                
                try:
                    var = value
                    value = result.group(2)

                    return InstructionVar(tk, var, value)
                except:

                    if value.isdigit():
                        return InstructionNumber(tk, float(value))
               
                    # Avoids newlines/backslashes getting escaped
                    value = value.encode('raw_unicode_escape').decode('unicode_escape')
                    return InstructionString(tk, value)
            except:
                return Instruction(tk)

    def lex(self: Lexer) -> list[Instruction]:
        self.__tokenized = []

        for line in self.__program:
            sub_lines: list[str] = line.split(';')

            if sub_lines:
                for l in sub_lines:
                    instr: Instruction = self.__lex_line(l)

                    if instr:
                        self.__tokenized.append(instr)
            else:
                instr: Instruction = self.__lex_line(line)

                if instr:
                    self.__tokenized.append(instr)

        return self.__tokenized
