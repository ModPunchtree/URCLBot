
from bCompiler.constants import alpha, assignmentOperators, binaryOperators, numeric, operators, unaryOperators

def fetch(variable: str) -> str:
    global useNumber
    if ((variable not in (RegVariables + RAMVariables)) and ((functionScope + "_" + variable) not in (RegVariables + RAMVariables))) and not(variable[0].isnumeric()):
        raise Exception("FATAL - Tried to fetch an undefined variable: " + variable)
    if (variable[:len(functionScope) + 1] != (functionScope + "_")) and not(variable[0].isnumeric()):
        variable = functionScope + "_" + variable
    if variable in RegVariables:
        return "R" + str(RegVariables.index(variable) + 1)
    if variable in RAMVariables:
        reg = leastRecentlyUsed.index(min(leastRecentlyUsed)) + 1
        if "" in RAMVariables:
            mem = RAMVariables.index("")
        else:
            RAMVariables.append("")
            mem = RAMVariables.index("")
        output.append("STR M" + str(mem) + ", R" + str(reg))
        RAMVariables[mem] = RegVariables[reg - 1]
        output.append("LOD R" + str(reg) + ", M" + str(RAMVariables.index(variable)))
        RegVariables[reg - 1] = variable
        leastRecentlyUsed[reg - 1] = useNumber
        useNumber += 1
        RAMVariables[RAMVariables.index(variable)] = ""
        return "R" + str(reg)
    if variable[0].isnumeric():
        return str(int(variable, 0))
    return variable

def uniqueNum() -> int:
    global uniqueNumber
    uniqueNumber += 1
    return uniqueNumber - 1

def lastIf() -> int:
    for i in range(len(squigglyStack)):
        if squigglyStack[len(squigglyStack) - 1 - i][0] == "if":
            return int(squigglyStack[len(squigglyStack) - 1 - i][1])
    raise Exception("FATAL - Failed to find if statement")

def lastWhile() -> int:
    for i in range(len(squigglyStack)):
        if squigglyStack[len(squigglyStack) - 1 - i][0] == "while":
            return squigglyStack[len(squigglyStack) - 1 - i][1]
    raise Exception("FATAL - Failed to find while statement")

def lastCon() -> int:
    for i in range(len(squigglyStack)):
        if squigglyStack[len(squigglyStack) - 1 - i][0] in ["if", "elseif", "else"]:
            return int(squigglyStack[len(squigglyStack) - 1 - i][1])
    raise Exception("FATAL - Failed to find if/elseif/else statement")

def isValid(word: str) -> bool:
    for i in word:
        if i not in (alpha() + numeric()):
            return False
    return True

def createVariable(variable: str) -> str:
    global useNumber
    if variable[0].isnumeric():
        raise Exception("FATAL - Invalid variable name: " + variable)
    if not(isValid(variable)):
        raise Exception("FATAL - Invalid variable name: " + variable)
    if variable[:len(functionScope)] != functionScope:
        variable = functionScope + "_" + variable
    try:
        num = RegVariables.index("")
        RegVariables[num] = variable
        leastRecentlyUsed[num] = useNumber
        useNumber += 1
    except Exception:
        try:
            num = RAMVariables.index("")
            RAMVariables[num] = variable
        except Exception:
            RAMVariables.append(variable)
    definedVariables.append(variable)
    return ""

def createTEMP() -> str:
    temp = "TEMP" + str(uniqueNum())
    createVariable(temp)
    return functionScope + "_" + temp

def delVar(variable: str) -> str:
    if variable in RegVariables:
        num = RegVariables.index(variable)
        RegVariables[num] = ""
        leastRecentlyUsed[num] = 0
    elif variable in RAMVariables:
        num = RAMVariables.index(variable)
        RAMVariables[num] = ""
    else:
        raise Exception("FATAL - Tried to delete non-existant variable: " + variable)
    
    definedVariables.pop(definedVariables.index(variable))
    return ""

def correctValue(value: int) -> int:
    while value >= (2 ** wordLength):
        value -= 2 ** wordLength
    while value < 0:
        value += 2 ** wordLength
    return value

def unaryToURCL() -> str:
    global index
    if token not in ["auto", "return"]:
        location1 = fetch(tokens[index - 1])
        if tokens[index - 1][(len(functionScope) + 1):(len(functionScope) + 5)] == "TEMP":
            delVar(tokens[index - 1])
        temp = createTEMP()
        location2 = fetch(temp)
    if token == "!":
        output.append("SETGE " + location2 + ", " + location1 + ", 1")
    elif token == "~":
        output.append("NOT " + location2 + ", " + location1)
    elif token == "-":
        output.append("NEG " + location2 + ", " + location1)
    elif token == "+":
        pass
    elif token == "*":
        raise Exception("FATAL - This compiler does not support variable pointers")
    elif token == "&":
        raise Exception("FATAL - This compiler does not support variable pointers")
    elif token == "++":
        output.append("INC " + location2 + ", " + location1)
    elif token == "--":
        output.append("DEC " + location2 + ", " + location1)
    elif token == "auto":
        y = createVariable(tokens[index - 1])
        if y:
            return y
        tokens.pop(index)
        tokenMap.pop(index)
    elif token == "return":
        output.append("INC SP, SP")
        temp2 = fetch(tokens[index - 1])
        output.append("STR SP, " + temp2)
        if temp2[len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
            delVar(temp2)
        output.append("DEC SP, SP")
        output.append("RET")
        tokens.pop(index)
        tokenMap.pop(index)
        tokens.pop(index - 1)
        tokenMap.pop(index - 1)
        
    if token not in ["auto", "return"]:
        tokens[index] = temp
        tokens.pop(index - 1)
        tokenMap.pop(index - 1)
    index = 0
    if token != "auto":
        output.append("//TEMP")
    return ""

def unaryConstant() -> str:
    global index
    num = int(tokens[index - 1], 0)
    if token == "!":
        if num == 0:
            tokens[index - 1] = "1"
        else:
            tokens[index - 1] = "0"
    elif token == "~":
        tokens[index - 1] = str((2 ** wordLength) - num - 1)
    elif token == "-":
        tokens[index - 1] = str((2 ** wordLength) - num)
    elif token == "+":
        pass
    elif token == "*":
        raise Exception("FATAL - Pointers are not supported on this compiler")
    elif token == "&":
        raise Exception("FATAL - Pointers are not supported on this compiler")
    elif token == "++":
        tokens[index - 1] = str(num + 1)
    elif token == "--":
        tokens[index - 1] = str(num - 1)
    elif token == "auto":
        return createVariable(num)
    elif token == "return":
        output.append("INC SP, SP")
        temp2 = fetch(tokens[index - 1])
        output.append("STR SP, " + temp2)
        output.append("DEC SP, SP")
        output.append("RET")
        tokens.pop(index)
        tokenMap.pop(index)
        tokens.pop(index - 1)
        tokenMap.pop(index - 1)
    
    if token != "return":
        tokens.pop(index)
        tokenMap.pop(index)
    index = 0
    return ""

def binaryToURCL() -> str:
    global index
    op1 = fetch(tokens[index - 2])
    op2 = fetch(tokens[index - 1])
    if tokens[index - 2][len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
        delVar(tokens[index - 2])
    if tokens[index - 1][len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
        delVar(tokens[index - 1])
    tempName = createTEMP()
    temp = fetch(tempName)
    if token == "||":
        if op1 != op2:
            output.append("OR " + temp + ", " + op1 + ", " + op2)
            output.append("SETGE " + temp + ", " + temp + ", 1")
        elif op1 == op2:
            output.append("SETGE " + temp + ", " + op1 + ", 1")
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "&&":
        if op1 == op2:
            output.append("IMM " + temp + ", 1")
        elif temp != op1:
            output.append("PSH " + op1)
            output.append("SETGE " + op1 + ", " + op1 + ", 1")
            output.append("SETGE " + temp + ", " + op2 + ", 1")
            output.append("AND " + temp + ", " + temp + ", " + op1)
            output.append("POP " + op1)
        elif temp != op2:
            output.append("PSH " + op2)
            output.append("SETGE " + op2 + ", " + op2 + ", 1")
            output.append("SETGE " + temp + ", " + op1 + ", 1")
            output.append("AND " + temp + ", " + temp + ", " + op2)
            output.append("POP " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "|":
        output.append("OR " + temp + ", " + op1 + ", " + op2)
    elif token == "^":
        output.append("XOR " + temp + ", " + op1 + ", " + op2)
    elif token == "&":
        output.append("AND " + temp + ", " + op1 + ", " + op2)
    elif token == "!=":
        if op1 == op2:
            output.append("IMM " + temp + ", 0")
        elif op1 != op2:
            output.append("SETNE " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "==":
        if op1 == op2:
            output.append("IMM " + temp + ", 1")
        elif op1 != op2:
            output.append("SETE " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == ">=":
        if op1 == op2:
            output.append("IMM " + temp + ", 1")
        elif op1 != op2:
            output.append("SETGE " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == ">":
        if op1 == op2:
            output.append("IMM " + temp + ", 0")
        elif op1 != op2:
            output.append("SETG " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "<=":
        if op1 == op2:
            output.append("IMM " + temp + ", 1")
        elif op1 != op2:
            output.append("SETLE " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "<":
        if op1 == op2:
            output.append("IMM " + temp + ", 0")
        elif op1 != op2:
            output.append("SETL " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == ">>":
        if op2 == "1":
            output.append("RSH " + temp + ", " + op1)
        elif op2 != "1":
            output.append("BSR " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "<<":
        if op2 == "1":
            output.append("LSH " + temp + ", " + op1)
        elif op2 != "1":
            output.append("BSL " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "-":
        if op1 == op2:
            output.append("IMM " + temp + ", 0")
        elif op1 != op2:
            output.append("SUB " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "+":
        output.append("ADD " + temp + ", " + op1 + ", " + op2)
    elif token == "%":
        if op2 == "0":
            raise Exception("FATAL - Division by zero error")
        elif op1 == op2:
            output.append("IMM " + temp + ", 0")
        elif op1 == "0":
            output.append("IMM " + temp + ", 0")
        elif op1 != op2:
            output.append("MOD " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "/":
        if op2 == "0":
            raise Exception("FATAL - Division by zero error")
        elif op1 == op2:
            output.append("IMM " + temp + ", 1")
        elif op1 == "0":
            output.append("IMM " + temp + ", 0")
        elif op2 == "1":
            output.append("MOV " + temp + ", " + op1)
        elif op2 == "2":
            output.append("RSH " + temp + ", " + op1)
        elif op1 != op2:
            output.append("DIV " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    elif token == "*":
        if (op1 == "0") or (op2 == "0"):
            output.append("IMM " + temp + ", 0")
        elif op1 == "1":
            output.append("MOV " + temp + ", " + op2)
        elif op2 == "1":
            output.append("MOV " + temp + ", " + op1)
        elif op1 == "2":
            output.append("LSH " + temp + ", " + op2)
        elif op2 == "2":
            output.append("LSH " + temp + ", " + op1)
        elif (op1 != "0") and (op2 != "0"):
            output.append("MLT " + temp + ", " + op1 + ", " + op2)
        else:
            raise Exception("FATAL - Unhandled operand combination for: " + token)
    tokens[index - 2] = tempName
    tokens.pop(index)
    tokenMap.pop(index)
    tokens.pop(index - 1)
    tokenMap.pop(index - 1)
    index = 0
    output.append("//TEMP")
    return ""

def binaryConstant() -> str:
    global index
    num1 = int(tokens[index - 2], 0)
    num2 = int(tokens[index - 1], 0)
    if token == "||":
        if (num1 + num2) == 0:
            tokens[index - 2] = 0
        else:
            tokens[index - 2] = 1
    elif token == "&&":
        if (num1 > 0) and (num2 > 0):
            tokens[index - 2] = 1
        else:
            tokens[index - 2] = 0
    elif token == "|":
        tokens[index - 2] = num1 | num2
    elif token == "^":
        tokens[index - 2] = num1 ^ num2
    elif token == "&":
        tokens[index - 2] = num1 & num2
    elif token == "!=":
        if num1 != num2:
            tokens[index - 2] = 1
        else:
            tokens[index - 2] = 0
    elif token == "==":
        if num1 == num2:
            tokens[index - 2] = 1
        else:
            tokens[index - 2] = 0
    elif token == ">=":
        if num1 >= num2:
            tokens[index - 2] = 1
        else:
            tokens[index - 2] = 0
    elif token == ">":
        if num1 > num2:
            tokens[index - 2] = 1
        else:
            tokens[index - 2] = 0
    elif token == "<=":
        if num1 <= num2:
            tokens[index - 2] = 1
        else:
            tokens[index - 2] = 0
    elif token == "<":
        if num1 < num2:
            tokens[index - 2] = 1
        else:
            tokens[index - 2] = 0
    elif token == ">>":
        tokens[index - 2] = num1 >> num2
    elif token == "<<":
        tokens[index - 2] = num1 << num2
    elif token == "-":
        tokens[index - 2] = num1 - num2
    elif token == "+":
        tokens[index - 2] = num1 + num2
    elif token == "%":
        tokens[index - 2] = num1 % num2
    elif token == "/":
        tokens[index - 2] = num1 // num2
    elif token == "*":
        tokens[index - 2] = num1 * num2
    else:
        raise Exception("FATAL - Undefined binary operator: " + token)
    tokens[index - 2] = str(correctValue(tokens[index - 2]))
    tokens.pop(index)
    tokenMap.pop(index)
    tokens.pop(index - 1)
    tokenMap.pop(index - 1)
    index = 0
    return ""

def assignmentToURCL() -> str:
    global index
    op1 = fetch(tokens[index - 2])
    op2 = fetch(tokens[index - 1])
    if token == "=":
        output.append("MOV " + op1 + ", " + op2)
    elif token == "+=":
        output.append("ADD " + op1 + ", " + op1 + ", " + op2)
    elif token == "-=":
        output.append("SUB " + op1 + ", " + op1 + ", " + op2)
    elif token == "*=":
        output.append("MLT " + op1 + ", " + op1 + ", " + op2)
    elif token == "/=":
        output.append("DIV " + op1 + ", " + op1 + ", " + op2)
    elif token == "%=":
        output.append("MOD " + op1 + ", " + op1 + ", " + op2)
    elif token == "&=":
        output.append("AND " + op1 + ", " + op1 + ", " + op2)
    elif token == "|=":
        output.append("OR " + op1 + ", " + op1 + ", " + op2)
    elif token == "^=":
        output.append("XOR " + op1 + ", " + op1 + ", " + op2)
    elif token == "<<=":
        if op2 == "1":
            output.append("LSH " + op1 + ", " + op1)
        else:
            output.append("BSL " + op1 + ", " + op1 + ", " + op2)
    elif token == ">>=":
        if op2 == "1":
            output.append("RSH " + op1 + ", " + op1)
        else:
            output.append("BSR " + op1 + ", " + op1 + ", " + op2)
    else:
        raise Exception("FATAL - Undefined assignment operator: " + token)
    if tokens[index - 1][len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
        delVar(tokens[index - 1])
    tokens.pop(index)
    tokenMap.pop(index)
    tokens.pop(index - 1)
    tokenMap.pop(index - 1)
    tokens.pop(index - 2)
    tokenMap.pop(index - 2)
    index = 0
    return ""

def generateURCL(tokens_: list, tokenMap_: list, functions: list, variables_: list, length: int, reg: int, code: str) -> str:
    
    global functionScope; functionScope = "global"
    global squigglyStack; squigglyStack = [["global", -1]] # name, uniqueNumber
    global RAMVariables; RAMVariables = [] # name
    global RegVariables; RegVariables = [""] * reg # name
    global leastRecentlyUsed; leastRecentlyUsed = [0] * reg
    global useNumber; useNumber = 1
    global uniqueNumber; uniqueNumber = 0
    global output; output = []
    global index; index = 0
    global tokens; tokens = tokens_
    global tokenMap; tokenMap = tokenMap_
    global token; tokens[index]
    global wordLength; wordLength = length
    global variables; variables = variables_
    global functionInputs; functionInputs = [["global", 0]] # name, inputs
    global definedVariables; definedVariables = []
    
    while index < len(tokens):
        token = tokens[index]
        if token[0] == "£":
            if token[1:] in functions:
                num = str(uniqueNum())
                output.append("JMP ." + token[1:] + "_END" + num)
                output.append("." + token[1:])
                functionScope = token[1:]
                squigglyStack.append([token[1:], num])

                output.append("INC SP, SP")
                temp2 = 1
                while tokens[index + 1][0] != "$":
                    y = createVariable(tokens[index + 1]) # defines input vars left to right
                    if y:
                        return y
                    var = fetch(tokens[index + 1])
                    output.append("POP " + var)
                    tokens.pop(index + 2)
                    tokenMap.pop(index + 2)
                    tokens.pop(index + 1)
                    tokenMap.pop(index + 1)
                    temp2 += 1
                if temp2 == 1:
                    output.pop()
                else:
                    output.append("SUB SP, SP, " + str(temp2))
                functionInputs.append([functionScope, temp2 - 1])
                
            elif token[1:] in ["if", "elseif", "else", "while"]:
                if token[1:] == "if":
                    num = str(uniqueNum())
                    output.append(".ifHead" + num)
                    squigglyStack.append(["if", num])
                elif token[1:] == "elseif":
                    output.append("JMP .elseEnd" + str(lastIf()))
                    num = str(int(lastCon()) + 1)
                    output.append(".elseStart" + num)
                    output.append(".ifHead" + num)
                    squigglyStack.append(["elseif", num])
                elif token[1:] == "else":
                    output.append("JMP .elseEnd" + str(lastIf()))
                    num = str(int(lastCon()) + 1)
                    output.append(".elseStart" + num)
                    squigglyStack.append(["else", num])
                elif token[1:] == "while":
                    num = str(uniqueNum())
                    output.append(".whileHead" + num)
                    squigglyStack.append(["while", num])
            elif token[1:] == "asm":
                tokens.pop(index + 1)
                tokenMap.pop(index + 1)
                temp = ""
                while tokens[index + 1] != "}":
                    if tokens[index + 1] == ",":
                        temp = temp[:-1] + tokens[index + 1] + " "
                    elif functionScope + "_" + tokens[index + 1] in definedVariables:
                        op = fetch(tokens[index + 1])
                        temp += op + " "
                    elif tokens[index + 1] in ("%", "#", "$"):
                        temp += tokens[index + 1]
                    else:
                        temp += tokens[index + 1] + " "
                    tokens.pop(index + 1)
                    tokenMap.pop(index + 1)
                    if tokens[index + 1] == ";":
                        tokens.pop(index + 1)
                        tokenMap.pop(index + 1)
                        output.append(temp)
                        temp = ""
                tokens.pop(index + 1)
                tokenMap.pop(index + 1)
            
            tokens.pop(index)
            tokenMap.pop(index)
            index = 0
                    
        elif token[0] == "$":
            if token[1:] in functions:
                tokens.pop(index)
                tokenMap.pop(index)
                index = 0
            elif token[1:] in ["if", "elseif", "while", "else"]:
                location = fetch(tokens[index - 1])
                if (location[0] != "R") and not(location[0].isnumeric()):
                    return location
                
                if token[1:] == "if":
                    output.append("BRZ .elseStart" + str(lastIf() + 1) + ", " + location)
                    output.append(".ifBody" + str(lastCon()))
                    tokens.pop(index)
                    tokenMap.pop(index)
                    if tokens[index - 1][len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
                        delVar(tokens[index - 1])
                    tokens.pop(index - 1)
                    tokenMap.pop(index - 1)
                elif token[1:] == "elseif":
                    output.append("BRZ .elseStart" + str(lastCon() + 1) + ", " + location)
                    output.append(".ifBody" + str(lastCon()))
                    tokens.pop(index)
                    tokenMap.pop(index)
                    if tokens[index - 1][len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
                        delVar(tokens[index - 1])
                    tokens.pop(index - 1)
                    tokenMap.pop(index - 1)
                elif token[1:] == "while":
                    output.append("BRZ .whileEnd" + str(lastWhile()) + ", " + location)
                    output.append(".whileBody" + str(lastWhile()))
                    tokens.pop(index)
                    tokenMap.pop(index)
                    if tokens[index - 1][len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
                        delVar(tokens[index - 1])
                    tokens.pop(index - 1)
                    tokenMap.pop(index - 1)
                else:
                    tokens.pop(index)
                    tokenMap.pop(index)
                index = 0
            else:
                raise Exception("FATAL - Undefined token: " + token)
                
        elif (token[0].isnumeric()) or (token in variables) or (token in RegVariables) or (token in RAMVariables):
            index += 1

        elif token in operators():
            if token in binaryOperators():
                if tokens[index - 1][0].isnumeric() and tokens[index - 2][0].isnumeric():
                    y = binaryConstant()
                else:
                    y = binaryToURCL()
                if y:
                    return y
            elif token in unaryOperators():
                if tokens[index - 1][0].isnumeric():
                    y = unaryConstant()
                else:
                    y = unaryToURCL()
                if y:
                    return y
            elif token in assignmentOperators():
                y = assignmentToURCL()
                if y:
                    return y
            else:
                raise Exception("FATAL - Unrecognised operand: " + token)

        elif token in functions:
            inputs = []
            for i in functionInputs: # fetch number of inputs
                if i[0] == token:
                    inputs = i[1]
            if inputs == []:
                raise Exception("FATAL - Undefined function: " + token)

            if functionScope == token: # save variables if recursive
                temp2 = []
                for i in range(inputs):
                    temp2.append(tokens[index + i - inputs])
                for i in definedVariables:
                    if i[:len(functionScope) + 1] == (functionScope + "_"):
                        temp = True
                        if i[len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
                            for j in range(inputs):
                                if temp2[inputs - 1 - j] == i:
                                    temp = False
                        if temp:
                            output.append("PSH " + fetch(i))
            
            for i in range(inputs):
                temp = fetch(tokens[index - 1])
                output.append("PSH " + temp)
                if tokens[index - 1][len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
                    delVar(tokens[index - 1])
                tokens.pop(index - 1)
                tokenMap.pop(index - 1)
                index -= 1
            if inputs == 0:
                output.append("DEC SP, SP")
            
            output.append("CAL ." + token)
            
            temp2 = createTEMP()
            output.append("POP " + fetch(temp2))
            
            if inputs > 1:
                output.append("ADD SP, SP, " + str(inputs - 1))
            
            if functionScope == token: # restore variables
                for i in definedVariables[::-1][1:]:
                    if i[:len(functionScope) + 1] == (functionScope + "_"):
                        temp = True
                        if i[len(functionScope) + 1: len(functionScope) + 5] == "TEMP":
                            for j in range(inputs):
                                if temp2[inputs - 1 - j] == i:
                                    temp = False
                        if temp:
                            output.append("POP " + fetch(i))
            
            tokens[index] = temp2
            index = 0
        
        elif token == "{":
            if squigglyStack[-1][0] in functions:
                output.append("INC SP, SP")
                output.append("STR SP, 0")
                output.append("DEC SP, SP")
                output.append("RET")
                output.append("." + functionScope + "_END" + squigglyStack[-1][1])
                for i in RegVariables:
                    if i[:len(functionScope) + 1] == (functionScope + "_"):
                        delVar(i)
                for i in RAMVariables:
                    if i[:len(functionScope) + 1] == (functionScope + "_"):
                        delVar(i)
                squigglyStack.pop()
                functionScope = squigglyStack[-1][0]
            elif squigglyStack[-1][0] in ["if", "elseif", "else"]:
                skip = False
                if len(tokens) != index + 1:
                    if tokens[index + 1] in ["£elseif", "£else"]:
                        skip = True
                if skip == False:
                    num = str(lastCon() + 1)
                    output.append(".elseStart" + num)
                    num = str(lastIf())
                    output.append(".elseEnd" + num)
                    temp = len(squigglyStack)
                    for i in range(temp):
                        if squigglyStack[temp - 1 - i][0] in ["if", "elseif", "else"]:
                            squigglyStack.pop()
                        else:
                            break
            elif squigglyStack[-1][0] == "while":
                output.append("JMP .whileHead" + str(squigglyStack[-1][1]))
                output.append(".whileEnd" + str(lastWhile()))
                squigglyStack.pop()
            tokens = tokens[index + 1:]
            tokenMap = tokenMap[index + 1:]
            index = 0
        
        elif token == "asm":
            pass #asm
        else:
            raise Exception("FATAL - Unrecognised token: " + token + "\n" + code[tokenMap[index] - 15: tokenMap[index] + 15] + "\n               ^")
    
    if output[-1] != "HLT":
        output.append("HLT")
    return output