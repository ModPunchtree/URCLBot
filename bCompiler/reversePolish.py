
# 1: convert to reverse polish using shunting yard
# 2: return tokens, tokenMap

from bCompiler.constants import operators

def reversePolish(variables: list, arrays: list, functions: list, tokens: list, tokenMap: list) -> tuple:

    # 1: convert to reverse polish using shunting yard
    output = []
    global operator
    operator = []
    tokenMapOutput = []
    tokenMapOperator = []
    while len(tokens) > 0:
        token = tokens.pop(0)
        location = tokenMap.pop(0)
        if type(token) == list:
            for i in token[: : -1]:
                output.append(i)
            tokenMapOutput.append(location)            
        elif token in [i[0] for i in variables] or token[0].isnumeric():
            output.append(token)
            tokenMapOutput.append(location)
        elif (token in [i[0] for i in functions + arrays]) or (token[0] == "%"):
            operator.append(token)
            tokenMapOperator.append(location)
        elif token in operators() and token != ",":
            while (topOp() in operators()) and (precedence(topOp()) > precedence(token)) and (topOp() != "("):
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
            operator.append(token)
            tokenMapOperator.append(location)
        elif token in ("(", "[", "{"):
            operator.append(token)
            tokenMapOperator.append(location)
        elif token == ")":
            while topOp() != "(":
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
            if topOp() == "(":
                operator.pop()
                tokenMapOperator.pop()
            if topOp() in [i[0] for i in functions]:
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
            if topOp().startswith("$"):
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
                if topOp() in ("auto", "auto*"):
                    output.append(operator.pop())
                    tokenMapOutput.append(tokenMapOperator.pop())
        elif token == "]":
            while topOp() != "[":
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
            if topOp() == "[":
                operator.pop()
                tokenMapOperator.pop()
            if (topOp() in [i[0] for i in arrays]) or (topOp().startswith("%")):
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
        elif token == ";":
            while topOp() != "{" and topOp() != "":
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
        elif token == ",":
            while topOp() not in ("", "(", "["):
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
        elif token == "}":
            while topOp() != "{":
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
            if topOp() == "{":
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOutput.pop())
        elif token[0] == "£":
            output.append(token)
            tokenMapOutput.append(location)
            operator.append("$" + token[1: ])
            tokenMapOperator.append(location)
        elif token in ("while", "if", "elseif", "else", "asm", "return", "delete"):
            output.append(token)
            tokenMapOutput.append(location)
            operator.append("$" + token)
            tokenMapOperator.append(location)
        else:
            print("WARNING - Unrecognised Token in for Polish: " + token)

    while len(operator) > 0:
        output.append(operator.pop())
        tokenMapOutput.append(tokenMapOperator.pop())
    
    return output, tokenMapOutput

def topOp() -> str:
    if len(operator) == 0:
        return ""
    return operator[-1]

def precedence(x) -> int:
    try:
        return operators().index(x)
    except:
        return -1
