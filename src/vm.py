# SLIT -- a Stack Language Intended for Training
# SLIT virtual machine
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from lexer import Token, Instruction, CONDITIONAL_TOKENS
from math  import sqrt, isclose

class VirtualMachine:
    def __init__(self: VirtualMachine, program: list[Instruction]) -> None:
        self.__program = program
    
    def __loop_until_token(
            self: VirtualMachine,
            tokens: list[Instruction],
            idx: int, target: Token
    ) -> int:
        idx += 1

        token: Token = None
        skipped_ifs: int = 0

        while idx < len(tokens):
            token = tokens[idx].token
            
            if token == target:
                if skipped_ifs:
                    skipped_ifs -= 1
                else:
                    break
            elif token in CONDITIONAL_TOKENS:
                skipped_ifs += 1

            idx += 1

        return idx
    
    def interpret(self: VirtualMachine) -> None:
        stack: list = []
        if_stack: list = []

        t_idx: int = 0
        step: bool = False

        while t_idx < len(self.__program):
            token: Token = self.__program[t_idx].token
            value = self.__program[t_idx].value

            if step:
                print(f'{t_idx:02}: {stack}')

            if token == Token.STEP:
                step = not step

            elif token in (Token.PUSHN, Token.PUSHS):
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
                
                t_idx = self.__loop_until_token(self.__program, t_idx, Token.ELSE)

            elif token == Token.IFNEQ:
                if not isclose(stack[-1], value):
                    t_idx += 1
                    if_stack.append(True)
                    continue
                
                t_idx = self.__loop_until_token(self.__program, t_idx, Token.ELSE)

            elif token == Token.IFLT:
                if stack[-1] < value:
                    t_idx += 1
                    if_stack.append(True)
                    continue
                
                t_idx = self.__loop_until_token(self.__program, t_idx, Token.ELSE)

            elif token == Token.IFLET:
                if isclose(stack[-1], value) or stack[-1] < value:
                    t_idx += 1
                    if_stack.append(True)
                    continue
                
                t_idx = self.__loop_until_token(self.__program, t_idx, Token.ELSE)

            elif token == Token.IFGT:
                if stack[-1] > value:
                    t_idx += 1
                    if_stack.append(True)
                    continue
                
                t_idx = self.__loop_until_token(self.__program, t_idx, Token.ELSE)

            elif token == Token.IFGET:
                if isclose(stack[-1], value) or stack[-1] > value:
                    t_idx += 1
                    if_stack.append(True)
                    continue
                
                t_idx = self.__loop_until_token(self.__program, t_idx, Token.ELSE)

            elif token == Token.ELSE:
                if if_stack:
                    if_stack.pop() 
                    t_idx = self.__loop_until_token(self.__program, t_idx, Token.ENDIF)

            elif token == Token.ENDIF:
                pass

            elif token == Token.PUT:
                print(stack[-1] if stack else "Empty stack")

            elif token == Token.DUMP:
                print(stack if stack else "Empty stack")

            t_idx += 1

