


from bCompiler.constants import operators, precedence


def reversePolish(tokens: list, tokenMap: list, functions: list, variables: list, code: str) -> tuple:
    
    tokens = tokens[::-1]
    tokenMap = tokenMap[::-1]
    outputStack = []
    operatorStack = ["{"]
    mapOutStack = []
    mapOpStack = []
    while len(tokens) > 0:
        if len(operatorStack) == 0:
            topOp = ""
        else:
            topOp = operatorStack[-1]
        token = tokens.pop()
        map = tokenMap.pop()
        
        if (token[0].isnumeric()) or (token in variables):
            outputStack.append(token)
            mapOutStack.append(map)
            
        elif token in functions:
            operatorStack.append(token)
            mapOpStack.append(map)
            
        elif token[0] == "£":
            outputStack.append(token)
            mapOutStack.append(map)
            if topOp == "auto":
                operatorStack.pop()
                mapOpStack.pop()
            if token not in ("£else", "£asm"):
                operatorStack.append("$" + token[1:])
                mapOpStack.append(map)
            if token == "£asm":
                while tokens[-1] != "}":
                    if token[-1] != ";":
                        outputStack.append(tokens.pop())
                        mapOutStack.append(tokenMap.pop())
                    else:
                        tokens.pop()
                        tokenMap.pop()
                outputStack.append(tokens.pop())
                mapOutStack.append(tokenMap.pop())

        elif token == ",":
            while (topOp != "(") and (topOp != "return") and (topOp != "{"):
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
                if len(operatorStack) == 0:
                    topOp = ""
                else:
                    topOp = operatorStack[-1]

        elif token in operators():
            while ((topOp in operators()) and (precedence(topOp) > precedence(token)) and (token != "(")):
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
                if len(operatorStack) == 0:
                    topOp = ""
                else:
                    topOp = operatorStack[-1]
            operatorStack.append(token)
            mapOpStack.append(map)
            
        elif token in ["(", "{"]:
            if topOp == "auto":
                operatorStack.pop()
                mapOpStack.pop()
            operatorStack.append(token)
            mapOpStack.append(map)
            
        elif token == ")":
            while topOp != "(":
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
                if len(operatorStack) == 0:
                    topOp = ""
                else:
                    topOp = operatorStack[-1]
            if topOp == "(":
                operatorStack.pop()
                mapOpStack.pop()
                if len(operatorStack) == 0:
                    topOp = ""
                else:
                    topOp = operatorStack[-1]
            if topOp in functions:
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
            elif topOp[0] == "$":
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
                
        elif token == ";":
            while topOp != "{":
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
                if len(operatorStack) == 0:
                    topOp = ""
                else:
                    topOp = operatorStack[-1]
        
        elif token == "}":
            while topOp != "{":
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
                if len(operatorStack) == 0:
                    topOp = ""
                else:
                    topOp = operatorStack[-1]
            if topOp == "{":
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
                if len(operatorStack) == 0:
                    topOp = ""
                else:
                    topOp = operatorStack[-1]
            if topOp in functions:
                outputStack.append(operatorStack.pop())
                mapOutStack.append(mapOpStack.pop())
        
        else:
            return "FATAL - Unrecognised token: " + token + "\n" + code[map - 15: map + 15] + "\n               ^"
                
    while len(operatorStack) > 1:
        outputStack.append(operatorStack.pop())
        mapOutStack.append(mapOpStack.pop())
    return outputStack, mapOutStack