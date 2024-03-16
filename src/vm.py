# SLIT -- a Stack Language Intended for Training
# SLIT virtual machine
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

from lexer import Token, Instruction, CONDITIONAL_TOKENS

import math
import re

class VirtualMachine:
    def __init__(self: VirtualMachine, program: list[Instruction]) -> None:
        self.__program = program
    
    def __throw(self: VirtualMachine, error: str) -> None:
        print(error)
        exit(-1)

    def __loop_until_endif(
            self: VirtualMachine,
            tokens: list[Instruction],
            idx: int
    ) -> int:
        idx += 1

        token: Token = None
        skipped_ifs: int = 0

        while idx < len(tokens):
            token = tokens[idx].token
            
            if token == Token.ENDIF:
                skipped_ifs -= 1
                
                if skipped_ifs <= 0:
                    break

            elif token in CONDITIONAL_TOKENS:
                skipped_ifs += 1

            idx += 1

        return idx

    def __loop_until_condend(
            self: VirtualMachine,
            tokens: list[Instruction],
            idx: int
    ) -> int:
        idx += 1

        token: Token = None
        skipped_ifs: int = 0

        while idx < len(tokens):
            token = tokens[idx].token
            
            if token == Token.ENDIF:
                skipped_ifs -= 1
                
                if skipped_ifs == 0:
                    idx += 1
                    break

            if token == Token.ELSE:
                if not skipped_ifs:
                    break
                elif tokens[idx + 1].token in CONDITIONAL_TOKENS:
                    idx += 1

            elif token in CONDITIONAL_TOKENS:
                skipped_ifs += 1

            idx += 1

        return idx
    
    def __get_variable(self: VirtualMachine, variables: dict, name):
        if isinstance(name, str):
            if name not in variables:
                self.__throw(f'Undeclared variable {name}!')
            
            return variables[name]
        
        return name
    
    def __get_string_or_var(self: VirtualMachine, variables: dict, value):
        result = self.__str_match.match(value)

        if not result:
            return self.__get_variable(variables, value)
        else:
            return result.group(1)

    def interpret(self: VirtualMachine) -> int:
        stack: list = []

        variables: dict = {}
        consts: dict = {}

        if_stack: int = 0
        t_idx: int = 0
        
        step: bool = False

        self.__var_match = re.compile('(^[a-zA-Z_][a-zA-Z_0-9]?$)')
        self.__str_match = re.compile('"(.+)"')
        
        while t_idx < len(self.__program):
            token: Token = self.__program[t_idx].token
            value = self.__program[t_idx].value

            if step:
                print(f'{t_idx:02}: {stack}')

            if token == Token.STEP:
                step = not step

            elif token == Token.QUIT:
                return value if value else 0

            elif token == Token.PUSHN:
                value = self.__get_variable(variables, value)
                stack.append(value)

            elif token == Token.PUSHS:
                stack.append(
                    self.__get_string_or_var(variables, value)
                )

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
                value = self.__get_variable(variables, value)

                if math.isclose(stack[-1], value):
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFNEQ:
                value = self.__get_variable(variables, value)

                if not math.isclose(stack[-1], value):
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFLT:
                value = self.__get_variable(variables, value)

                if stack[-1] < value:
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFLET:
                value = self.__get_variable(variables, value)

                if math.isclose(stack[-1], value) or stack[-1] < value:
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFGT:
                value = self.__get_variable(variables, value)

                if stack[-1] > value:
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)

            elif token == Token.IFGET:
                value = self.__get_variable(variables, value)

                if math.isclose(stack[-1], value) or stack[-1] > value:
                    t_idx += 1
                    if_stack += 1
                    continue
                
                t_idx = self.__loop_until_condend(self.__program, t_idx)
            
            elif token == Token.STRCMP:
                stack.append(
                    int(self.__get_string_or_var(variables, value) == stack.pop())
                )

            elif token == Token.ELSE:
                t_idx = self.__loop_until_endif(self.__program, t_idx)

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

            elif token == Token.DECL:
                var = self.__program[t_idx].var
                result = self.__str_match.match(value)

                if not result:
                    variables[var] = value
                else:
                    variables[var] = result.group(1)

            t_idx += 1
        
        return 0

