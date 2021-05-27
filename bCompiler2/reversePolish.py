
# 1: convert to reverse polish using shunting yard
# 2: return tokens, tokenMap

from bCompiler2.constants import operators

def reversePolish(variables: list, lists: list, functions: list, tokens: list, tokenMap: list) -> tuple:

    # 1: convert to reverse polish using shunting yard
    output = []
    global operator
    operator = []
    tokenMapOutput = []
    tokenMapOperator = []
    while len(tokens) > 0:
        token = tokens.pop(0)
        location = tokenMap.pop(0)
        
        if token in [i[0] for i in variables] or token[0].isnumeric():
            output.append(token)
            tokenMapOutput.append(location)
        elif (token in [i[0] for i in functions + lists]) or (token[0] == "%"):
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
                    operator.pop()
                    tokenMapOperator.pop()
        elif token == "]":
            while topOp() != "[":
                output.append(operator.pop())
                tokenMapOutput.append(tokenMapOperator.pop())
            if topOp() == "[":
                operator.pop()
                tokenMapOperator.pop()
            if (topOp() in [i[0] for i in lists]) or (topOp().startswith("%")):
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
