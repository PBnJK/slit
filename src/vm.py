# SLIT -- a Stack Language Intended for Training
# SLIT virtual machine
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from lexer import Token, Instruction, CONDITIONAL_TOKENS
import math

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
    
    def __loop_until_condend(self: VirtualMachine, tokens: list[Instruction], idx: int) -> int:
        idx += 1

        token: Token = None
        skipped_ifs: int = 0

        while idx < len(tokens):
            token = tokens[idx].token
            
            if token in (Token.ENDIF, Token.ELSE):
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

        if_stack: int = 0
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

            elif token == Token.SWAP:
                a = stack.pop()
                b = stack.pop()

                stack.append(a)
                stack.append(b)

            elif token == Token.DUP:
                duped = stack[-1]
                stack.append(duped)

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
                stack.append(
                    math.sqrt(stack.pop())
                )

            elif token == Token.POW:
                b: float = stack.pop()
                a: float = stack.pop()

                stack.append(a ** b)
            
            elif token == Token.MOD:
                b: float = stack.pop()
                a: float = stack.pop()

                stack.append(a % b)

            elif token == Token.SIND:
                stack.append(
                    math.sin(math.radians(stack.pop()))
                )
            
            elif token == Token.SINR:
                stack.append(
                    math.sin(stack.pop())
                )
            
            elif token == Token.COSD:
                stack.append(
                    math.cos(math.radians(stack.pop()))
                )
            
            elif token == Token.COSR:
                stack.append(
                    math.cos(stack.pop())
                )
            
            elif token == Token.TAND:
                stack.append(
                    math.tan(math.radians(stack.pop()))
                )
            
            elif token == Token.TANR:
                stack.append(
                    math.tan(stack.pop())
                )
            
            elif token == Token.IFEQ:
                if math.isclose(stack[-1], value):
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFNEQ:
                if not math.isclose(stack[-1], value):
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFLT:
                if stack[-1] < value:
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFLET:
                if math.isclose(stack[-1], value) or stack[-1] < value:
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFGT:
                if stack[-1] > value:
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFGET:
                if math.isclose(stack[-1], value) or stack[-1] > value:
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.ELSE:
                if if_stack:
                    if_stack -= 1
                    t_idx = self.__loop_until_token(self.__program, t_idx, Token.ENDIF)

            elif token == Token.ENDIF:
                if_stack -= 1

            elif token == Token.PUT:
                print(stack[-1] if stack else "Empty stack")

            elif token == Token.PUTRAW:
                print(stack[-1] if stack else "Empty stack", end='')

            elif token == Token.DUMP:
                print(stack if stack else "Empty stack")

            elif token == Token.PRINT:
                print(value, end='')

            elif token == Token.READ:
                val: str = input('> ')

                try:
                    stack.append(float(val))
                except:
                    stack.append(val)
                
            elif token == Token.ANYKEY:
                input()

            t_idx += 1

