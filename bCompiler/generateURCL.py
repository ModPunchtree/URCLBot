
def generateURCL(tokens_: list, tokenMap: list, allVariables: list, allFunctions: list, allArrays: list, MINREG: int, BITS: int) -> list:
    global tokens; tokens = [i for i in tokens_]
    global uniqueNum; uniqueNum = 0
    global functionScope; functionScope = "global"
    global definedVariables; definedVariables = [] # just names
    global variables; variables = [] # name + _scope, type
    global definedFunctions; definedFunctions = [] # just names
    global functions; functions = [] # name + _scope, type, number of inputs
    global definedArrays; definedArrays = [] # just names
    global arrays; arrays = [] # name + _scope, type, length, origin
    global registers; registers = ["" for i in range(MINREG)]
    global leastRecentlyUsedRegister; leastRecentlyUsedRegister = [0 for i in range(MINREG)] # smaller number means less used
    global heap; heap = []
    global output; output = []
    global token
    global squigglyStack; squigglyStack = ["global"]
    
    global tokenNumber; tokenNumber = 0
    while tokenNumber < len(tokens):
        token = tokens[tokenNumber]

        if type(token) == list:
            tokenNumber += 1
        
        elif token in ("auto", "auto*"):
            if not tokens[tokenNumber - 1].startswith("%"):
                temp = createVariable(tokens[tokenNumber - 1], token)
                tokens.pop(tokenNumber); tokenNumber = 0
            else: # %array
                createArray(tokens[tokenNumber - 1][1: ], token, tokens[tokenNumber - 2])
                tokens.pop(tokenNumber); tokens[tokenNumber - 2] = "0"; tokenNumber = 0
        
        elif token.startswith("£") and (token[1: ] in [i[0] for i in allFunctions]):
            functionScope = token[1: ] + "_" + functionScope
            output.append("JMP .End_" + functionScope)
            output.append("." + functionScope)
            output.append("INC SP SP")
            tokens[tokenNumber] = "functionVarStart"; tokenNumber = 0
        
        elif token.startswith("$") and (token[1: ] in [i[0] for i in allFunctions]):
            squigglyStack.append(functionScope)
            listOfInputs = getListOfFunctionInputs()
            numberOfInputs = len(listOfInputs)
            functions.append([functionScope, tokens[tokenNumber + 1], numberOfInputs])
            if functionScope in definedFunctions:
                raise Exception("FATAL - Tried to define an already defined function: " + functionScope)
            definedFunctions.append(functionScope)
            for i in listOfInputs:
                fetch1 = optimisedFetch(i)
                output.append("POP " + fetch1)
            output.append("SUB SP SP " + str(numberOfInputs + 1))
            tokens.pop(tokenNumber + 1); tokens.pop(tokenNumber); tokenNumber = 0
        
        elif token == "while":
            temp = fetchWhileConditionTokens()
            squigglyStack.append(["while", uniqueNumber(), temp])
            output.append(".whileHead_" + squigglyStack[-1][1])
            tokens.pop(tokenNumber); tokenNumber = 0
        
        elif token == "if":
            squigglyStack.append(["if", uniqueNumber()])
            output.append(".ifHead_" + squigglyStack[-1][1])
            tokens.pop(tokenNumber); tokenNumber = 0
        
        elif token == "$while":
            number = lastWhile()
            fetch1 = optimisedFetch(tokens[tokenNumber - 1])
            if tokens[tokenNumber - 1].startswith("TEMP"):
                delVar(tokens[tokenNumber - 1])
            output.append("BRZ .whileEnd_" + number + " " + fetch1)
            output.append(".whileBody_" + number)
            tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
        
        elif token == "$if":
            number = lastIf()
            fetch1 = optimisedFetch(tokens[tokenNumber - 1])
            if tokens[tokenNumber - 1].startswith("TEMP"):
                delVar(tokens[tokenNumber - 1])
            output.append("BRZ .elseStart_" + str(int(number) + 1) + " " + fetch1)
            output.append(".ifBody_" + number)
            tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
        
        elif token == "$elseif":
            number = lastElseIfOrIf()
            fetch1 = optimisedFetch(tokens[tokenNumber - 1])
            if tokens[tokenNumber - 1].startswith("TEMP"):
                delVar(tokens[tokenNumber - 1])
            output.append("BRZ .elseStart_" + str(int(number) + 1) + " " + fetch1)
            output.append(".ifBody_" + number)
            tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
        
        elif token == "$return":
            output.append("INC SP SP")
            fetch1 = optimisedFetch(tokens[tokenNumber - 1])
            if tokens[tokenNumber - 1].startswith("TEMP"):
                delVar(tokens[tokenNumber - 1])
            output.append("STR SP " + fetch1)
            output.append("DEC SP SP")
            output.append("RET")
            tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
        
        elif token == "{":
            nextToken = 69
            if tokenNumber + 1 < len(tokens):
                nextToken = tokens[tokenNumber + 1]
            if squigglyStack[-1][0] == "while":
                temp = lastWhileConditions()
                temp.append("€while")
                tokens = tokens[: tokenNumber] + temp + tokens[tokenNumber + 1: ]
                tokenNumber = 0
            elif nextToken == "elseif":
                number = lastIf()
                output.append("JMP .elseEnd_" + number)
                number = str(int(lastElseIfOrIf()) + 1)
                squigglyStack.append(["elseif", number])
                output.append(".elseStart_" + number)
                output.append(".ifHead_" + number)
                tokens.pop(tokenNumber + 1); tokens.pop(tokenNumber); tokenNumber = 0
            elif nextToken == "else":
                number = lastIf()
                output.append("JMP .elseEnd_" + number)
                number = str(int(lastElseIfOrIf()) + 1)
                squigglyStack.append(["else", number])
                output.append(".elseStart_" + number)
                tokens.pop(tokenNumber + 1); tokens.pop(tokenNumber); tokenNumber = 0
            elif squigglyStack[-1][0] in ("if", "elseif", "else"):
                number = str(int(lastElseOrElseIfOrIf()) + 1)
                output.append(".elseStart_" + number)
                output.append(".elseEnd_" + lastIf())
                popAllConditionsOffSquigglyStack()
                tokens.pop(tokenNumber + 1); tokens.pop(tokenNumber); tokenNumber = 0
            elif type(squigglyStack[-1]) == str: # end of function definition
                output.append("INC SP SP")
                output.append("STR SP 0")
                output.append("DEC SP SP")
                output.append("RET")
                output.append(".End_" + functionScope)
                locals = [i if i.endswith(functionScope) else "" for i in definedVariables]
                for i in locals:
                    if i:
                        delVar(i)
                squigglyStack.pop()
                functionScope = squigglyStack[-1]
                tokens.pop(tokenNumber); tokenNumber = 0
            else:
                raise Exception()
                
        elif token == "€while":
            number = lastWhile()
            fetch1 = optimisedFetch(tokens[tokenNumber - 1])
            if tokens[tokenNumber - 1].startswith("TEMP"):
                delVar(tokens[tokenNumber - 1])
            output.append("BNZ .whileBody_" + number + " " + fetch1)
            output.append(".whileEnd_" + number)
            tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
        
        elif listOfPotentialFunctions(token):
            temp = listOfPotentialFunctions(token)
            temp69 = str(token)
            if token + "_" + functionScope in temp:
                funcName = token + "_" + functionScope
            elif token + "_" + previousFunctionScope() in temp:
                funcName = token + "_" + previousFunctionScope()
            else:
                funcName = temp[-1]
            functionType = getFunctionType(funcName)
            recursive = False
            if (token + "_" + previousFunctionScope() == functionScope) and (funcName != (token + "_" + functionScope)): # recursive
                recursive = True
            if recursive:
                locals = [i if i.endswith(functionScope) else "" for i in definedVariables]
                num = 0
                while num < len(locals):
                    if locals[num] == "":
                        locals.pop(num)
                        num = 0
                    else:
                        num += 1
                for i in locals:
                    fetch1 = optimisedFetch(i)
                    output.append("PSH " + fetch1)
            try:
                numberOfInputs = functions[[i[0] for i in functions].index(temp69)][2]
            except:
                try:
                    numberOfInputs = functions[[i[0] for i in functions].index(temp69 + "_" + functionScope)][2]
                except:
                    numberOfInputs = functions[[i[0] for i in functions].index(temp69 + "_" + previousFunctionScope())][2]
            if numberOfInputs == 0:
                output.append("DEC SP SP")
            deleted = []
            for i in range(numberOfInputs):
                fetch1 = optimisedFetch(tokens[tokenNumber - 1 - i])
                output.append("PSH " + fetch1)
                if tokens[tokenNumber - 1 - i].startswith("TEMP"):
                    delVar(tokens[tokenNumber - 1 - i])
                    deleted.append(tokens[tokenNumber - 1 - i])
                tokens.pop(tokenNumber - 1 - i)
            tokenNumber -= numberOfInputs
            output.append("CAL ." + funcName)
            temp = createTEMP(functionType)
            fetch1 = optimisedFetch(temp)
            output.append("POP " + fetch1)
            tokens[tokenNumber] = temp
            if (numberOfInputs == 0) or (numberOfInputs == 1):
                pass
            else:
                output.append("ADD SP SP " + str(numberOfInputs - 1))
            if recursive:
                for i in deleted:
                    if i in locals:
                        locals.pop(locals.index(i))
                for i in locals[:: -1]:
                    fetch1 = optimisedFetch(i)
                    output.append("POP " + fetch1)
            tokenNumber = 0
            
        elif token in ("--", "++", "autoTypeCast", "auto*TypeCast", "sizeof", "unary&", "unary*", "unary+", "unary-", "~", "!"):
            if token == "sizeof":
                length = 1
                if tokens[tokenNumber - 1] in definedArrays:
                    length = getArrayLength(tokens[tokenNumber - 1])
                tokens[tokenNumber - 1] = str(length)
                tokens.pop(tokenNumber)
                tokenNumber = 0
            elif token == "unary&":
                if tokens[tokenNumber - 1] in definedArrays:
                    temp = createTEMP(type1)
                    tempLocation = optimisedFetch(temp)
                    output.append("ADD " + tempLocation + " " + str(getArrayOrigin(tokens[tokenNumber - 1])) + " M0")
                    tokens[tokenNumber - 1] = temp
                    tokens.pop(tokenNumber)
                    tokenNumber = 0
                else:
                    raise Exception()
            else:
                if tokens[tokenNumber - 1][0].isnumeric():
                    type1 = "auto"
                else:
                    type1 = getVariableType(tokens[tokenNumber - 1])
                if token == "autoTypeCast":
                    type1 = "auto"
                elif token == "auto*TypeCast":
                    type1 = "auto*"
                fetch1 = optimisedFetch(tokens[tokenNumber - 1])
                if tokens[tokenNumber - 1].startswith("TEMP"):
                    delVar(tokens[tokenNumber - 1])
                temp = createTEMP(type1)
                tempLocation = optimisedFetch(temp)
                if token == "--":
                    output.append("DEC " + tempLocation + " " + fetch1)
                elif token == "++":
                    output.append("INC " + tempLocation + " " + fetch1)
                elif token in ("autoTypeCast", "auto*TypeCast"):
                    output.append("MOV " + tempLocation + " " + fetch1)
                elif token == "unary*":
                    output.append("LOD " + tempLocation + " " + fetch1)
                elif token == "unary+":
                    output.append("MOV " + tempLocation + " " + fetch1)
                elif token == "unary-":
                    output.append("NEG " + tempLocation + " " + fetch1)
                elif token == "~":
                    output.append("NOT " + tempLocation + " " + fetch1)
                elif token == "!":
                    output.append("SETE " + tempLocation + " " + fetch1 + " 0")
                else:
                    raise Exception()
                tokens.pop(tokenNumber); tokens[tokenNumber - 1] = temp; tokenNumber = 0

        elif token in ("||", "&&", "|", "binary&", "!=", "==", ">=", ">", "<=", "<", ">>", "<<", "binary-", "binary+", "%", "/", "binary*"):
            type1 = "constant"
            type2 = "constant"
            if not tokens[tokenNumber - 2][0].isnumeric():
                type1 = getVariableType(tokens[tokenNumber - 2])
            if not tokens[tokenNumber - 1][0].isnumeric():
                type2 = getVariableType(tokens[tokenNumber - 1])
            
            if (type1 != type2) and (type1 != "constant") and (type2 != "constant"):
                raise Exception("FATAL - Cannot do " + token + " with types: " + type1 + " and " + type2)
            fetch1 = optimisedFetch(tokens[tokenNumber - 2])
            fetch2 = optimisedFetch(tokens[tokenNumber - 1])
            if tokens[tokenNumber - 1].startswith("TEMP"):
                delVar(tokens[tokenNumber - 1])
            if tokens[tokenNumber - 2].startswith("TEMP"):
                delVar(tokens[tokenNumber - 2])
            temp = createTEMP(type1)
            tempLocation = optimisedFetch(temp)
            if token == "||":
                output.append("OR " + tempLocation + " " + fetch1 + " " + fetch2)
                output.append("SETNE " + tempLocation + " " + tempLocation + " 0")
            elif token == "&&":
                if tempLocation != fetch2:
                    output.append("SETNE " + tempLocation + " " + fetch1 + " 0")
                    output.append("AND " + tempLocation + " " + tempLocation + " " + fetch2)
                    output.append("SETNE " + tempLocation + " " + tempLocation + " 0")
                elif tempLocation != fetch1:
                    output.append("SETNE " + tempLocation + " " + fetch2 + " 0")
                    output.append("AND " + tempLocation + " " + tempLocation + " " + fetch1)
                    output.append("SETNE " + tempLocation + " " + tempLocation + " 0")
                elif (tempLocation == fetch1) and (tempLocation == fetch2):
                    output.append("SETNE " + tempLocation + " " + fetch1 + " 0")
                else:
                    raise Exception()
            elif token == "|":
                output.append("OR " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "binary&":
                output.append("AND " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "!=":
                output.append("SETNE " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "==":
                output.append("SETE " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == ">=":
                output.append("SETGE " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == ">":
                output.append("SETG " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "<=":
                output.append("SETLE " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "<":
                output.append("SETL " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == ">>":
                output.append("BSR " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "<<":
                output.append("BSL " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "binary-":
                output.append("SUB " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "binary+":
                output.append("ADD " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "%":
                output.append("MOD " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "/":
                output.append("DIV " + tempLocation + " " + fetch1 + " " + fetch2)
            elif token == "binary*":
                output.append("MLT " + tempLocation + " " + fetch1 + " " + fetch2)
            else:
                raise Exception()
            tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens[tokenNumber - 2] = temp; tokenNumber = 0

        elif token in (">>=", "<<=", "^=", "|=", "&=", "%=", "/=", "*=", "-=", "+=", "="):
            if token == "=":
                if tokens[tokenNumber - 1][0].isnumeric():
                    if not tokens[tokenNumber - 2].startswith("%"):
                        target = optimisedFetch(tokens[tokenNumber - 2])
                        output.append("IMM " + target + " " + tokens[tokenNumber - 1])
                        tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2); tokenNumber = 0
                    else: # %array
                        oldIndex = tokens[tokenNumber - 3]
                        arrayIndex = optimisedFetch(tokens[tokenNumber - 3])
                        if tokens[tokenNumber - 3].startswith("TEMP"):
                            delVar(tokens[tokenNumber - 3])
                        arrayName = tokens[tokenNumber - 2]
                        output.append("ADD " + arrayIndex + " " + arrayIndex + " " + str(getArrayOrigin(arrayName[1: ])))
                        output.append("STR " + arrayIndex + " " + tokens[tokenNumber - 1])
                        tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2); tokens.pop(tokenNumber - 3)
                        if oldIndex[0].isnumeric():
                            tokens.insert(tokenNumber - 3, str(int(oldIndex) + 1)); tokens.insert(tokenNumber - 2, arrayName)
                        tokenNumber = 0
                else:
                    fetch1 = optimisedFetch(tokens[tokenNumber - 1])
                    if not tokens[tokenNumber - 2].startswith("%"):
                        arrayFlag = False
                        target = optimisedFetch(tokens[tokenNumber - 2])
                        if tokens[tokenNumber - 1].startswith("TEMP"):
                            delVar(tokens[tokenNumber - 1])
                        output.append("MOV " + target + " " + fetch1)
                    else:
                        arrayFlag = True
                        oldIndex = tokens[tokenNumber - 3]
                        arrayIndex = optimisedFetch(tokens[tokenNumber - 3])
                        if tokens[tokenNumber - 1].startswith("TEMP"):
                            delVar(tokens[tokenNumber - 1])
                        if tokens[tokenNumber - 3].startswith("TEMP"):
                            delVar(tokens[tokenNumber - 3])
                        arrayName = tokens[tokenNumber - 2]
                        output.append("ADD " + arrayIndex + " " + arrayIndex + " " + str(getArrayOrigin(arrayName[1: ])))
                        output.append("STR " + arrayIndex + " " + fetch1)
                        tokens.pop(tokenNumber - 2); tokenNumber -= 1
                    tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2)
                    if arrayFlag and oldIndex[0].isnumeric():
                        tokens.insert(tokenNumber - 2, str(int(oldIndex) + 1)); tokens.insert(tokenNumber - 1, arrayName)
                    tokenNumber = 0
            else:
                if tokens[tokenNumber - 1][0].isnumeric():
                    if not tokens[tokenNumber - 2].startswith("%"):
                        arrayFlag = False
                        target = optimisedFetch(tokens[tokenNumber - 2])
                    else: # %array
                        arrayFlag = True
                        arrayName = tokens[tokenNumber - 2]
                        arrayType = getArrayType(arrayName[1: ])
                        fetch1 = optimisedFetch(tokens[tokenNumber - 3])
                        if tokens[tokenNumber - 3].startswith("TEMP"):
                            delVar(tokens[tokenNumber - 3])
                        tempName = createTEMP(arrayType)
                        temp = optimisedFetch(tempName)
                        tempName2 = createTEMP(arrayType)
                        temp2 = optimisedFetch(tempName2)
                        output.append("MOV " + temp + " " + fetch1)
                        output.append("ADD " + temp + " " + temp + " " + str(getArrayOrigin(arrayName[1: ])))
                        output.append("LOD " + temp2 + " " + temp)
                        target = temp2
                        tokens.pop(tokenNumber - 2); tokenNumber -= 1
                    if token == ">>=":
                        output.append("BSR " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "<<=":
                        output.append("BSL " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "^=":
                        output.append("XOR " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "|=":
                        output.append("OR " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "&=":
                        output.append("AND " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "%=":
                        output.append("MOD " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "/=":
                        output.append("DIV " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "*=":
                        output.append("MLT " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "-=":
                        output.append("SUB " + target + " " + target + " " + tokens[tokenNumber - 1])
                    elif token == "+=":
                        output.append("ADD " + target + " " + target + " " + tokens[tokenNumber - 1])
                    else:
                        raise Exception()
                    if arrayFlag:
                        output.append("STR " + temp + " " + target)
                    tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2); tokenNumber = 0
                else:
                    fetch1 = optimisedFetch(tokens[tokenNumber - 1])
                    if not tokens[tokenNumber - 2].startswith("%"):
                        arrayFlag = False
                        target = optimisedFetch(tokens[tokenNumber - 2])
                        if tokens[tokenNumber - 1].startswith("TEMP"):
                            delVar(tokens[tokenNumber - 1])
                    else: # %array
                        arrayFlag = True
                        arrayName = tokens[tokenNumber - 2]
                        arrayType = getArrayType(arrayName[1: ])
                        fetch1 = optimisedFetch(tokens[tokenNumber - 3])
                        if tokens[tokenNumber - 3].startswith("TEMP"):
                            delVar(tokens[tokenNumber - 3])
                        if tokens[tokenNumber - 1].startswith("TEMP"):
                            delVar(tokens[tokenNumber - 1])
                        tempName = createTEMP(arrayType)
                        temp = optimisedFetch(tempName)
                        tempName2 = createTEMP(arrayType)
                        temp2 = optimisedFetch(tempName2)
                        output.append("MOV " + temp + " " + fetch1)
                        output.append("ADD " + temp + " " + temp + " " + str(getArrayOrigin(arrayName[1: ])))
                        output.append("LOD " + temp2 + " " + temp)
                        target = temp2
                        tokens.pop(tokenNumber - 2); tokenNumber -= 1
                    if token == ">>=":
                        output.append("BSR " + target + " " + target + " " + fetch1)
                    elif token == "<<=":
                        output.append("BSL " + target + " " + target + " " + fetch1)
                    elif token == "^=":
                        output.append("XOR " + target + " " + target + " " + fetch1)
                    elif token == "|=":
                        output.append("OR " + target + " " + target + " " + fetch1)
                    elif token == "&=":
                        output.append("AND " + target + " " + target + " " + fetch1)
                    elif token == "%=":
                        output.append("MOD " + target + " " + target + " " + fetch1)
                    elif token == "/=":
                        output.append("DIV " + target + " " + target + " " + fetch1)
                    elif token == "*=":
                        output.append("MLT " + target + " " + target + " " + fetch1)
                    elif token == "-=":
                        output.append("SUB " + target + " " + target + " " + fetch1)
                    elif token == "+=":
                        output.append("ADD " + target + " " + target + " " + fetch1)
                    else:
                        raise Exception()
                    if arrayFlag:
                        output.append("STR " + temp + " " + target)
                    tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2); tokenNumber = 0
        
        elif (token + "_" + functionScope) in definedArrays:
            type1 = getArrayType(token)
            tempName = createTEMP(type1)
            temp = optimisedFetch(tempName)
            if tokens[tokenNumber - 1][0].isnumeric():
                location = "M" + str(getArrayOrigin(token) + int(tokens[tokenNumber - 1], 0))
            else:
                fetch1 = optimisedFetch(tokens[tokenNumber - 1])
                if tokens[tokenNumber - 1].startswith("TEMP"):
                    delVar(tokens[tokenNumber - 1])
                output.append("MOV " + temp + " " + fetch1)
                output.append("ADD " + temp + " " + temp + " " + str(getArrayOrigin(token)))
                location = temp
            output.append("LOD " + temp + " " + location)
            tokens.pop(tokenNumber); tokens[tokenNumber - 1] = tempName; tokenNumber = 0
        
        elif token == "return":
            tokens.pop(tokenNumber)
            tokenNumber = 0
        
        elif token == "$asm":
            number = uniqueNumber()
            output.append(".asmStart_" + number)
            while tokens[tokenNumber - 1] != "asm":
                temp = ""
                for i in tokens[tokenNumber - 1]:
                    if i + "_" + functionScope in definedVariables:
                        fetch1 = optimisedFetch(i + "_" + functionScope)
                        temp += fetch1 + " "
                    else:
                        temp += i + " "
                if temp:
                    temp = temp[: -1]
                output.append(temp)
                tokens.pop(tokenNumber - 1)
                tokenNumber -= 1
            output.append(".asmEnd_" + number)
            tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
        
        elif (token[0].isnumeric()) or (token in [i[0] for i in allVariables]) or (token.startswith("%")) or (token == "asm") or (token == "functionVarStart") or (token in definedVariables):
            tokenNumber += 1
        
        else:
            raise Exception("FATAL - Unrecognised token: " + token)

    return output

def listOfPotentialFunctions(name: str) -> list:
    temp = [i if i.startswith(name) else "" for i in definedFunctions]
    for i, j in enumerate(temp):
        if len(j) >= (len(name) + 1):
            if j[len(name)] != "_":
                temp[i] = ""
        else:
            temp[i] = ""
    num = 0
    while num < len(temp):
        if temp[num] == "":
            temp.pop(num)
            num = 0
        else:
            num += 1
    return temp

def uniqueNumber() -> str:
    global uniqueNum
    uniqueNum += 1
    return str(uniqueNum)

def optimisedFetch(name: str) -> str:
    
    if name[0].isnumeric():
        targetLocation = "R" + str(leastRecentlyUsedRegister.index(min(leastRecentlyUsedRegister)) + 1)
    
        preserveName = registers[int(targetLocation[1:]) - 1]
        if preserveName != "":
            if "" in registers:
                output.append("MOV R" + str(registers.index("") + 1) + " " + targetLocation)
                registers[registers.index("")] = preserveName
                leastRecentlyUsedRegister[registers.index(preserveName)] = max(leastRecentlyUsedRegister) + 1
            elif "" in heap:
                output.append("STR M" + str(heap.index("")) + " " + targetLocation)
                heap[heap.index("")] = preserveName
            else:
                output.append("STR M" + str(len(heap)) + " " + targetLocation)
                heap.append(preserveName)
            registers[int(targetLocation[1:]) - 1] = ""
        
        output.append("IMM " + targetLocation + " " + name)
        leastRecentlyUsedRegister[int(targetLocation[1:]) - 1] = max(leastRecentlyUsedRegister) + 1
        return targetLocation
    
    if name not in definedVariables:
        name += "_" + functionScope

    if name in definedVariables:
        if name in registers:
            targetLocation = "R" + str(registers.index(name) + 1)
        else:
            targetLocation = "R" + str(leastRecentlyUsedRegister.index(min(leastRecentlyUsedRegister)) + 1)
    
            preserveName = registers[int(targetLocation[1:]) - 1]
            if preserveName != "":
                if "" in registers:
                    output.append("MOV R" + str(registers.index("") + 1) + " " + targetLocation)
                    registers[registers.index("")] = preserveName
                    leastRecentlyUsedRegister[registers.index(preserveName)] = max(leastRecentlyUsedRegister) + 1
                elif "" in heap:
                    output.append("STR M" + str(heap.index("")) + " " + targetLocation)
                    heap[heap.index("")] = preserveName
                else:
                    output.append("STR M" + str(len(heap)) + " " + targetLocation)
                    heap.append(preserveName)
                registers[int(targetLocation[1:]) - 1] = ""

            location = "M" + str(heap.index(name))
            output.append("LOD " + targetLocation + " " + location)
    else:
        raise Exception("FATAL - Tried to fetch variable that doesn't exist: " + name)
    
    leastRecentlyUsedRegister[registers.index(name)] = max(leastRecentlyUsedRegister) + 1
    
    return targetLocation

def createVariable(name: str, type: str) -> str:
    if not(name.endswith("_" + functionScope)):
        name += "_" + functionScope
    for i in name:
        if ((not(i.isnumeric)) and (not(i.isalpha)) and (i != "_")):
            raise Exception("FATAL - Invalid variable name: " + name)
    if (name in registers) or (name in heap):
        raise Exception("FATAL - Tried to define already existing variable: " + name)
    
    if "" in registers:
        leastRecentlyUsedRegister[registers.index("")] = max(leastRecentlyUsedRegister) + 1
        registers[registers.index("")] = name
    elif "" in heap:
        heap[heap.index("")] = name
    else:
        heap.append(name)

    variables.append([name, type])
    definedVariables.append(name)
    return name

def createTEMP(type: str) -> str:
    name = "TEMP_" + uniqueNumber()
    return createVariable(name, type)

def getArrayType(name: str) -> str:
    try:
        return arrays[[i[0] for i in arrays].index(name)][1]
    except:
        return arrays[[i[0] for i in arrays].index(name + "_" + functionScope)][1]

def getArrayOrigin(name: str) -> int:
    try:
        return arrays[[i[0] for i in arrays].index(name)][3]
    except:
        return arrays[[i[0] for i in arrays].index(name + "_" + functionScope)][3]

def delVar(name: str) -> None:
    if name not in definedVariables:
        name += "_" + functionScope
    if name in definedVariables:
        if name in registers:
            leastRecentlyUsedRegister[registers.index(name)] = 0
            registers[registers.index(name)] = ""
        else:
            heap[heap.index(name)] = ""
        definedVariables.pop(definedVariables.index(name))
    else:
        raise Exception("FATAL - Tried to delete variable which does not exist: " + name)

def getVariableType(name: str) -> str:
    try:
        return variables[[i[0] for i in variables].index(name)][1]
    except:
        return variables[[i[0] for i in variables].index(name + "_" + functionScope)][1]

def getArrayLength(name: str) -> str:
    try:
        return arrays[[i[0] for i in arrays].index(name)][2]
    except:
        return arrays[[i[0] for i in arrays].index(name + "_" + functionScope)][2]

def previousFunctionScope() -> str:
    num = len(squigglyStack) - 2
    while num > -1:
        if type(squigglyStack[num]) == str:
            return squigglyStack[num]
        num -= 1
    return "global"

def getFunctionType(name: str) -> str:
    try:
        return functions[[i[0] for i in functions].index(name)][1]
    except:
        return functions[[i[0] for i in functions].index(name + "_" + functionScope)][1]

def lastWhile() -> str:
    num = len(squigglyStack) - 1
    while num > -1:
        if squigglyStack[num][0] == "while":
            return squigglyStack[num][1]
        num -= 1
    raise Exception("FATAL - Failed to find previous while statement")

def lastWhileConditions() -> list:
    num = len(squigglyStack) - 1
    while num > -1:
        if squigglyStack[num][0] == "while":
            return squigglyStack[num][2]
        num -= 1
    raise Exception("FATAL - Failed to find previous while statement")

def lastIf() -> str:
    num = len(squigglyStack) - 1
    while num > -1:
        if squigglyStack[num][0] == "if":
            return squigglyStack[num][1]
        num -= 1
    raise Exception("FATAL - Failed to find previous if statement")

def lastElseIfOrIf() -> str:
    num = len(squigglyStack) - 1
    while num > -1:
        if squigglyStack[num][0] in ("if", "elseif"):
            return squigglyStack[num][1]
        num -= 1
    raise Exception("FATAL - Failed to find previous 'if' or 'else if' statement")

def lastElseOrElseIfOrIf() -> str:
    num = len(squigglyStack) - 1
    while num > -1:
        if squigglyStack[num][0] in ("if", "elseif", "else"):
            return squigglyStack[num][1]
        num -= 1
    raise Exception("FATAL - Failed to find previous 'if', 'else if' or 'else' statement")

def popAllConditionsOffSquigglyStack() -> None:
    num = len(squigglyStack) - 1
    while num > -1:
        if squigglyStack[num][0] == "if":
            squigglyStack.pop(num)
            return
        elif squigglyStack[num][0] in ("elseif", "else"):
            squigglyStack.pop(num)
        else:
            raise Exception("FATAL - Found non-condition statement on the squigglyStack")
        num -= 1
    raise Exception("FATAL - Failed to find previous if statement")

def fetchWhileConditionTokens() -> list:
    num = 0
    answer = []
    for i in tokens[tokenNumber + 1: ]:
        if i == "$while":
            if num == 0:
                return answer
            else:
                num -= 1
        elif i == "while":
            num += 1
        answer.append(i)
    raise Exception("FATAL - Failed to find $while")

def getListOfFunctionInputs() -> list:
    global tokenNumber
    answer = []
    temp = [i for i in tokens[: tokenNumber]]
    num = len(temp) - 1
    num2 = 0
    while num > -1:
        i = temp[num]
        if i == "functionVarStart":
            if num2 == 0:
                tokens.pop(num)
                tokenNumber -= 1
                return answer[:: -1]
            else:
                num2 -= 1
        elif i.startswith("$"):
            num2 += 1
        answer.append(i)
        tokens.pop(num)
        tokenNumber -= 1
        num -= 1
            
def createArray(name: str, type: str, length: str) -> None:
    if name.endswith("_" + functionScope):
        rawName = name[: len("_" + functionScope)]
    else:
        rawName = name
    if not(name.endswith("_" + functionScope)):
        name += "_" + functionScope
    if name in definedArrays:
        raise Exception("FATAL - Attempted to define already defined array: " + name)
    definedArrays.append(name)
    start = findStartOfArray(int(length)) # find optimal location in heap for array of given length
    arrays.append([name, type, length, start])
    if start == len(heap):
        for i in range(int(length)):
            heap.append(rawName + "[" + str(i) + "]" + "_" + functionScope)
    else:
        for i in range(int(length)):
            heap[start + i] = (rawName + "[" + str(i) + "]" + "_" + functionScope)
    return
    
def findStartOfArray(length: int) -> int:
    num = 0
    num2 = 0
    while num < len(heap):
        if heap[num] == "":
            num2 += 1
        else:
            num2 = 0
        num += 1
        if num2 == length:
            return num - num2
    return num





