
# 0: Clean Code

# 1: Tokeniser
    # 1: loop over chars in code
    # 2: read each identifier/symbol into a list
    # 3: return tokens, tokenMap

# 2: Preprocess
    # 1: check brackets match
    # 2: check for ;
    # 3: find variables (including lists) and functions
    # 4: check for undefined identifers
    # 5: convert +/-/&/*/auto * into something unambiguous
    # 6: convert (auto) and (auto*) into something unambiguous
    # 7: return variables, functions, tokens, tokenMap

# 3: Reverse Polish
    # 1: convert to reverse polish using shunting yard
    # 2: return tokens, tokenMap

# 4: Generate URCL
    # 1: traverse tokens left to right, converting to URCL
        # token
            # auto, auto*
                # variable
                    # 1: createVar(tokens[tokenNumber - 1], token)
                    # 2: tokens.pop(tokenNumber); tokenNumber = 0
                
                # %array
                    # createArray(tokens[tokenNumber - 1][1: ], token, tokens[tokenNumber - 2])
                        # if name.endswith("_" + functionScope): rawName = name[: len("_" + functionScope)]; else: rawName = name
                        # if not(name.endswith("_" + functionScope)): name += "_" + functionScope
                        # if name in definedArrays: raise Exception(FATAL - Defined duplicate array)
                        # definedArrays.append(name)
                        # start = findStartOfArray(length) # find optimal location in heap for array of given length
                        # arrays.append([name, type, length, start])
                        # if start == len(heap):
                            # for i in range(length):
                                # heap.append(rawName + "[" + str(i) + "]" + "_" + functionScope)
                        # else:
                            # for i in range(length):
                                # heap[start + i] = (rawName + "[" + str(i) + "]" + "_" + functionScope)
                                
                    # tokens.pop(tokenNumber); tokens[tokenNumber - 2] = 0; tokenNumber = 0
            
            # £function
                # 1: functionScope = function + "_" + functionScope
                # output.append("." + functionScope)
                # "INC SP SP"
                # 2: tokens[tokenNumber] = "functionVarStart"; tokenNumber = 0
            
            # $function
                # squigglyStack.append(functionScope)
                # listOfInputs = getListOfFunctionInputs()
                # numberOfInputs = len(listOfInputs)
                # functions.append([functionScope, tokens[tokenNumber + 1], numberOfInputs])
                # if functionScope in definedFunctions:
                    # raise Exception("FATAL - Tried to define an already defined function: " + functionScope)
                # definedFunctions.append(functionScope)
                # for i in listOfInputs:
                    # fetch1 = optimalFetch(i)
                    # "POP " + fetch1
                # "SUB SP SP " + str(numberOfInputs + 1)
                # tokens.pop(tokenNumber + 1); tokens.pop(tokenNumber); tokenNumber = 0
            
            # while
                # temp = fetchWhileConditionTokens()
                # squigglyStack.append(["while", uniqueNumber(), temp])
                # ".whileHead_" + squigglyStack[-1][1]
                # tokens.pop(tokenNumber); tokenNumber = 0
            
            # if
                # squigglyStack.append(["if", uniqueNumber()])
                # ".ifHead_" + squigglyStack[-1][1]
                # tokens.pop(tokenNumber); tokenNumber = 0

            # $while
                # number = lastWhile()
                # fetch1 = optimalFetch(tokens[tokenNumber - 1])
                # "BRZ .whileEnd_" + number + " " + fetch1
                # ".whileBody_" + number
                # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0

            # $if
                # number = lastIf()
                # fetch1 = optimalFetch(tokens[tokenNumber - 1])
                # "BRZ .elseStart_" + str(int(number) + 1) + " " + fetch1
                # ".ifBody_" + number
                # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
            
            # $elseif
                # number = lastElseIfOrIf()
                # fetch1 = optimalFetch(tokens[tokenNumber - 1])
                # "BRZ .elseStart_" + str(int(number) + 1) + " " + fetch1
                # ".ifBody_" + number
                # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
            
            # $return
                # INC SP SP
                # fetch1 = optimalFetch(tokens[tokenNumber - 1])
                # "STR SP " + fetch1
                # DEC SP SP
                # RET
                # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
            
            # {
                # nextToken = "69"
                # if tokenNumber + 1 < len(tokens):
                    # nextToken = tokens[tokenNumber + 1]
                
                # if squigglyStack[-1][0] == "while":
                    # temp = lastWhileConditions()
                    # temp.append("€while")
                    # tokens = tokens[: tokenNumber] + temp + tokens[tokenNumber + 1: ]; tokenNumber = 0
                
                # elif nextToken == "elseif":
                    # number = lastIf()
                    # "JMP .elseEnd_" + number
                    # number = str(int(lastElseIfOrIf()) + 1)
                    # squigglyStack.append(["elseif", number])
                    # ".elseStart_" + number
                    # ".ifHead_" + number
                    # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
                
                # elif nextToken == "else":
                    # number = lastIf()
                    # "JMP .elseEnd_" + number
                    # number = str(int(lastElseIfOrIf()) + 1)
                    # squigglyStack.append(["else", number])
                    # ".elseStart_" + number
                    # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
                
                # elif squigglyStack[-1][0] in ("if", "elseif", "else"):
                    # number = lastElseOrElseIfOrIf() + 1
                    # ".elseStart_" + number
                    # ".elseEnd_" + lastIf()
                    # popAllConditionsOffSquigglyStack()
                    # tokens.pop(tokenNumber); tokenNumber = 0
                
                # elif type(squigglyStack[-1]) == str: # end of function definition
                    # INC SP SP
                    # STR SP 0
                    # DEC SP SP
                    # RET
                    # locals = [i if i.endswith(functionScope) else "" for i in definedVariables]
                    # for i in locals:
                        # if i:
                            # delVar(i)
                    # squigglyStack.pop()
                    # functionScope = squigglyStack[-1][0]
                    # tokens.pop(tokenNumber); tokenNumber = 0
                    
                # else:
                    # raise Exception()
            
            # €while
                # number = lastWhile()
                # fetch1 = optimalFetch(tokens[tokenNumber - 1])
                # "BNZ .whileBody_" + number + " " + fetch1
                # ".whileEnd_" + number
                # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
            
            # elif listOfPotentialFunctions(): # function
                # temp = listOfPotentialFunctions()
                # if token + "_" + functionScope in temp:
                    # funcName = token + "_" + functionScope
                # elif token + "_" + previousFunctionScope in temp:
                    # funcName = token + "_" + previousFunctionScope
                # else:
                    # funcName = temp[0]
                # recursive = False
                # if token + "_" + previousFunctionScope() == functionScope: # recursive
                    # recursive = True
                # if recursive:
                    # locals = [i if i.endswith(functionScope) else "" for i in definedVariables]
                    # num = 0
                    # while num < len(locals):
                        # if locals[num] == "":
                            # locals.pop(num)
                            # num = 0
                        # else:
                            # num += 1
                    # for i in locals:
                        # fetch1 = optimalFetch(i)
                        # "PSH " + fetch1
                # numberOfInputs = functions[[i[0] for i in functions].index(token)][2]
                # if numberOfInputs == 0:
                    # "DEC SP SP"
                # else:
                    # for i in range(numberOfInputs):
                        # fetch1 = optimalFetch(tokens[tokenNumber - 1 - i])
                        # "PSH fetch1"
                        # if tokens[tokenNumber - 1 - i].startswith("TEMP"):
                            # delVar(tokens[tokenNumber - 1 - i])
                        # tokens.pop(tokenNumber - 1 - i)
                # tokenNumber -= numberOfInputs
                # "CAL ." + funcName
                # temp = createTEMP()
                # fetch1 = optimalFetch(temp)
                # "POP " + fetch1
                # tokens[tokenNumber] = temp
                # if recursive:
                    # for i in locals[-1]:
                        # fetch1 = optimalFetch(i)
                        # "POP " + fetch1
                # tokenNumber = 0
                
            # unary
                # sizeof
                    # length = 1
                    # if array:
                        # length = get length of array
                    # tokens[tokenNumber - 1] = str(length)
                    # tokens.pop(tokenNumber)
                    # tokenNumber = 0
                    
                # constant
                    # constant fold
                    
                # variable
                    # type = getType(tokens[tokenNumber - 1])
                    # if token == autoTypeCast: type = "auto"
                    # elif token == auto*TypeCast: type = "auto*"
                    # temp = createTEMP(type)
                    # tempLocation = fetch(temp)
                    # get fetch1
                        # --, ++, unary*, unary+, unary-, ~, !
                            # fetch1 = fetch(tokens[tokenNumber - 1])
                            # if tokens[tokenNumber - 1].startswith("TEMP"): delVar(tokens[tokenNumber - 1])
                        # autoTypeCast or auto*TypeCast
                            # fetch1 = optimalCopyFetch(tokens[tokenNumber - 1])
                    # gen URCL
                        # --
                            # DEC tempLocation fetch1
                        # ++
                            # DEC tempLocation fetch1
                        # autoTypeCast or auto*TypeCast
                            # MOV tempLocation fetch1
                        # unary&
                            # constant fold (might need to set a flag here)
                        # unary*
                            # LOD tempLocation fetch1
                        # unary+
                            # MOV tempLocation fetch1
                        # unary-
                            # NEG tempLocation fetch1
                        # ~
                            # NOT tempLocation fetch1
                        # !
                            # SETE tempLocation fetch1 0
                    # tokens.pop(tokenNumber); tokens[tokenNumber - 1] = temp; tokenNumber = 0
            
            # binary
                # type1 = getType(tokens[tokenNumber - 1])
                # type2 = getType(tokens[tokenNumber - 2])
                # if type1 != type2: raise Exception("FATAL - Cannot do " + token + " with types: " + type1 + " and " + type2)
                # fetch1 = fetch(tokens[tokenNumber - 1])
                # fetch2 = fetch(tokens[tokenNumber - 2])
                # if tokens[tokenNumber - 1].startswith("TEMP"): delVar(tokens[tokenNumber - 1])
                # if tokens[tokenNumber - 2].startswith("TEMP"): delVar(tokens[tokenNumber - 2])
                # temp = createTEMP(type1)
                # tempLocation = fetch(tempLocation)
                # ||
                    # OR tempLocation fetch1 fetch2
                    # SETNE tempLocation tempLocation 0
                # &&
                    # if tempLocation != fetch2:
                        # SETNE tempLocation fetch1 0
                        # AND tempLocation tempLocation fetch2
                        # SETNE tempLocation tempLocation 0
                    # elif tempLocation != fetch1:
                        # SETNE tempLocation fetch2 0
                        # AND tempLocation tempLocation fetch1
                        # SETNE tempLocation tempLocation 0
                    # elif tempLocation == fetch1 and tempLocation == fetch2:
                        # SETNE tempLocation fetch1 0
                    # else:
                        # raise Exception()
                # |
                    # OR tempLocation fetch1 fetch2
                # binary&
                    # AND tempLocation fetch1 fetch2
                # !=
                    # SETNE tempLocation fetch1 fetch2
                # ==
                    # SETE tempLocation fetch1 fetch2
                # >=
                    # SETGE tempLocation fetch1 fetch2
                # >
                    # SETG tempLocation fetch1 fetch2
                # <=
                    # SETLE tempLocation fetch1 fetch2
                # <
                    # SETL tempLocation fetch1 fetch2
                # >>
                    # BSR tempLocation fetch1 fetch2
                # << 
                    # BSL tempLocation fetch1 fetch2
                # binary-
                    # SUB tempLocation fetch1 fetch2
                # binary+
                    # ADD tempLocation fetch1 fetch2
                # %
                    # MOD tempLocation fetch1 fetch2
                # /
                    # DIV tempLocation fetch1 fetch2
                # binary*
                    # MLT tempLocation fetch1 fetch2
                # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens[tokenNumber - 2] = temp; tokenNumber = 0
            
            # assignment
                # =
                    # constant
                        # get target
                            # variable
                                # 1: target = fetch(variable)
                                # 2: IMM target constant
                                # 3: tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2); tokenNumber = 0
                            # %array
                                # arrayIndex = previous token
                                # arrayName = array name with %
                                # 1: target = find mem location with previous token (index) and array name
                                # 2: STR target constant
                                # 3: tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2); tokens.pop(tokenNumber - 3);
                                # 4: tokens.insert(tokenNumber - 3, str(int(arrayIndex) + 1)); tokens.insert(tokenNumber - 2, arrayName)
                                # 5: tokenNumber = 0
                            
                    # variable
                        # 1: get fetch
                            # fetch1 = fetch(variable)
                    
                        # 2: get target
                            # variable
                                # arrayFlag = False
                                # target = fetch(variable)
                            # %array
                                # arrayFlag = True
                                # arrayIndex = previous token
                                # arrayName = token
                                # 1: find mem location with previous token (index) and array name
                                # 2: target = memlocation
                                # 3: tokens.pop(tokenNumber - 2); tokenNumber -= 1
                        
                        # 3: genURCL
                            # target[0] == "R"
                                # MOV target fetch1
                            # target[0] == "M"
                                # STR target fetch1
                        
                        # 4: tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2)
                        
                        # 5: if arrayFlag:
                            # tokens.insert(tokenNumber - 2, str(int(arrayIndex) + 1)); tokens.insert(tokenNumber - 1, arrayName)
                        
                        # 6: tokenNumber = 0
                    
                # any other assignment
                    # constant
                        # 1: get target
                            # variable
                                # set array flag = False
                                # target = fetch(variable)
                            # %array
                                # set array flag = True
                                # targetOriginal = find mem location with previous token (index) and array name
                                # target = copyOptimisedFetch(targetOriginal)
                                # tokens.pop(tokenNumber - 2); tokenNumber -= 1
                                
                        # 2: genURCL
                            # >>=
                                # BSR target target constant
                            # <<=
                                # BSL target target constant
                            # ^=
                                # XOR target target constant
                            # |=
                                # OR target target constant
                            # &=
                                # AND target target constant
                            # %=
                                # MOD target target constant
                            # /=
                                # DIV target target constant
                            # *=
                                # MLT target target constant
                            # -=
                                # SUB target target constant
                            # +=
                                # ADD target target constant
                        
                        # 3: if arrayFlag:
                            # STR targetOriginal target
                            
                        # 4: tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2); tokenNumber = 0
                        
                    # variable
                        # 1: get fetch
                            # variable
                                # fetch1 = fetch(variable)
                            # %array
                                # 1: fetch1 = find mem location with previous token (index) and array name
                                # 2: create TEMP
                                # 3: temp = fetch(TEMP)
                                # 4: LOD temp fetch1
                                # 5: fetch1 = temp
                                # 5: # tokens.pop(tokenNumber - 1); tokenNumber -= 1
                    
                        # 2: get target
                            # variable
                                # set array flag = False
                                # target = fetch(variable)
                            # %array
                                # set array flag = True
                                # targetOriginal = find mem location with previous token (index) and array name
                                # target = copyOptimisedFetch(targetOriginal)
                                # tokens.pop(tokenNumber - 2); tokenNumber -= 1
                        
                        # 3: genURCL
                            # >>=
                                # BSR target target fetch1
                            # <<=
                                # BSL target target fetch1
                            # ^=
                                # XOR target target fetch1
                            # |=
                                # OR target target fetch1
                            # &=
                                # AND target target fetch1
                            # %=
                                # MOD target target fetch1
                            # /=
                                # DIV target target fetch1
                            # *=
                                # MLT target target fetch1
                            # -=
                                # SUB target target fetch1
                            # +=
                                # ADD target target fetch1
                        
                        # 4: if arrayFlag:
                            # STR targetOriginal target
                            
                        # 5: tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokens.pop(tokenNumber - 2); tokenNumber = 0
            
            # array
                # 1: create TEMP (same type as array type)
                # 2: temp = fetch(TEMP)
                # 3: memLocation = find mem location with previous token (index) and array name
                # 4: LOD temp memLocation
                # 5: # tokens.pop(tokenNumber); tokens[tokenNumber - 1] = tempVariableName; tokenNumber = 0
            
            # return
                # tokens.pop(tokenNumber)
                # tokenNumber = 0
            
            # $asm
                # number = uniqueNumber()
                # ".asmStart_" + number
                # while tokens[tokenNumber - 1] != "asm":
                    # temp = ""
                    # for i in tokens[tokenNumber - 1]:
                        # if i + "_" + functionScope in definedVariables:
                            # fetch1 = optimalFetch(i + "_" + functionScope)
                            # temp += fetch1 + " "
                        # else:
                            # temp += i + " "
                    # if temp:
                        # temp = temp[: -1]
                    # output.append(temp)
                    # tokens.pop(tokenNumber - 1)
                    # tokenNumber -= 1
                # ".asmEnd_" + number
                # tokens.pop(tokenNumber); tokens.pop(tokenNumber - 1); tokenNumber = 0
            
            # number, definedVar, %array, type == list, asm
                # tokenNumber += 1
    
            # else:
                # raise Exception("FATAL - Unrecognised token: " + token)

        # def listOfPotentialFunctions() -> list:
            # temp = [i if i.startswith(token) else "" for i in definedFunctions]
            # num = 0
            # while num < len(temp):
                # if temp[num] == "":
                    # temp.pop(num)
                    # num = 0
                # else:
                    # num += 1
            # return temp

    # 2: return URCL code as a list with markers for temporary variables

# 5: Compiler Optimisations
    # 1: optimise temporary variables
    # 2: return URCL code

# 6: General Optimisations


