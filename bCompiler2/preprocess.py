
# 1: check brackets match
# 2: check for ;
# 3: find variables (including lists) and functions
# 4: check for undefined identifers
# 5: convert +/-/&/*/auto * into something unambiguous
# 6: convert (auto) and (auto*) into something unambiguous
# 7: return variables, functions, tokens, tokenMap

def preprocess(tokens: list, tokenMap: list, code: str, BITS: int) -> tuple:
    
    # 1: check brackets match
    if bracketsDontMatch(tokens, tokenMap):
        raise Exception("FATAL - Mismatched brackets:\n" + code[int(bracketsDontMatch(tokens, tokenMap)) - 15: int(bracketsDontMatch(tokens, tokenMap)) + 15] + "\n" + " "*15 + "^")
    
    # 2: check for ;
    if semicolonMissing(tokens, tokenMap):
        raise Exception("FATAL - Missing ; in code:\n" + code[int(semicolonMissing(tokens, tokenMap)) - 15: int(semicolonMissing(tokens, tokenMap)) + 15] + "\n" + " "*15 + "^")

    # 3: find variables (including lists) and functions
    global variables
    variables, lists, functions = findIdentifiers(tokens, tokenMap)
    
    # 4: check for undefined identifers
    if undefinedIdentifier(tokens, tokenMap, variables, lists, functions):
        raise Exception("FATAL - Unrecognised identifer:\n" + code[int(undefinedIdentifier(tokens, tokenMap, variables, lists, functions)) - 15: int(undefinedIdentifier(tokens, tokenMap, variables, lists, functions)) + 15] + "\n" + " "*15 + "^")

    # 5: convert +/-/&/*/auto * into something unambiguous
    # 6: convert (auto) and (auto*) into something unambiguous
    tokens, tokenMap = unambigify(tokens, tokenMap)

    # check numbers fit in BITS
    if numbersDontFitInBITS(tokens, tokenMap, BITS):
        raise Exception("FATAL - Invalid number in code:\n" + code[int(numbersDontFitInBITS(tokens, tokenMap, BITS)) - 15: int(numbersDontFitInBITS(tokens, tokenMap, BITS)) + 15] + "\n" + " "*15 + "^")

    # check for invalid symbols
    if invalidSymbol(tokens, tokenMap):
        raise Exception("FATAL - Invalid symbol:\n" + code[int(invalidSymbol(tokens, tokenMap)) - 15: int(invalidSymbol(tokens, tokenMap)) + 15] + "\n" + " "*15 + "^")

    # add call to main if needed
    if (not findMain(tokens)) and ("main" in [i[0] for i in functions]):
        tokens.append("main")
        tokens.append("(")
        tokens.append(")")
        tokens.append(";")
        for i in range(4):
            tokenMap.append("0")

    # 7: return variables, functions, tokens, tokenMap
    return variables, lists, functions, tokens, tokenMap

def bracketsDontMatch(tokens: list, tokenMap: list) -> str:
    stack = []
    for i, j in enumerate(tokens):
        if j in ("(", "{", "["):
            stack.append(j)
        elif j == ")":
            if stack.pop() != "(":
                return str(tokenMap[i])
        elif j == "}":
            if stack.pop() != "{":
                return str(tokenMap[i])
        elif j == "]":
            if stack.pop() != "[":
                return str(tokenMap[i])
    if len(stack) != 0:
        return str(tokenMap[-1])
    return ""

def semicolonMissing(tokens: list, tokenMap: list) -> str:
    assignment = False
    for i, j in enumerate(tokens):
        if False: #j == "}":
            for k in range(i):
                if tokens[i - 1 - k] == ";":
                    break
                elif tokens[i - 1 - k] != "}":
                    return str(tokenMap[i - 1 - k])
        elif False: #j in ("=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^="):
            if assignment == True:
                return str(tokenMap[i])
            assignment = True
        elif j == ";":
            assignment = False
    return ""

def findIdentifiers(tokens: list, tokenMap: list) -> tuple:
    variables = []
    lists = []
    functions = []
    for i, j in enumerate(tokens):
        if j[0].isalpha():
            if tokens[i - 1] == "auto":
                if tokens[i + 1] == "(":
                    functions.append([j, "auto"])
                    tokens[i] = "£" + j
                elif tokens[i + 1] == "[":
                    lists.append([j, "auto"])
                    tokens[i] = "%" + j
                else:
                    variables.append([j, "auto"])
                    
            elif tokens[i - 1] == "*":
                if tokens[i - 2] == "auto":
                    if tokens[i + 1] == "[":
                        lists.append([j, "auto*"])
                        tokens[i] = "%" + j
                    elif tokens[i + 1] == "(":
                        functions.append([j, "auto*"])
                        tokens[i] = "£" + j
                    else:
                        variables.append([j, "auto*"])
            
            if j in [i[0] for i in lists]:
                close = closeSquare(tokens, i + 1)
                if tokens[close] == "=":
                    tokens[i] = "%" + j
            
        if j == "=" and tokens[i + 1] == "{":
            close, tokens, tokenMap, num = closeSquiggly(tokens, i + 1, tokenMap)
            if tokens[close - 1] == "}":
                tokens[i + 1] = "["
                tokens[close - 1] = "]"
                if tokens[i - 2] == "[":
                    tokens.insert(i - 1, str(num + 1))
                    tokenMap.insert(i - 1, tokenMap[i - 1])
            
    return variables, lists, functions

def undefinedIdentifier(tokens: list, tokenMap: list, variables: list, lists: list, functions: list) -> str:
    for i, j in enumerate(tokens):
        if j[0].isalpha():
            if j not in [i[0] for i in variables + lists + functions] + ["auto", "delete", "return", "asm", "if", "else", "while"]:
                return str(tokenMap[i])
    return ""

def unambigify(tokens: list, tokenMap: list) -> tuple:
    for i, j in enumerate(tokens):
        if j == "auto":
            if tokens[i + 1] == "*":
                tokens[i] = "auto*"
                tokens.pop(i + 1)
                tokenMap.pop(i + 1)
                return unambigify(tokens, tokenMap)
            elif tokens[i + 1] == ")" and tokens[i - 1] == "(":
                tokens[i] = "autoTypeCast"
                tokens.pop(i + 1)
                tokenMap.pop(i + 1)
                tokens.pop(i - 1)
                tokenMap.pop(i - 1)
                return unambigify(tokens, tokenMap)
        elif j == "auto*":
            if tokens[i + 1] == ")" and tokens[i - 1] == "(":
                tokens[i] = "auto*TypeCast"
                tokens.pop(i + 1)
                tokenMap.pop(i + 1)
                tokens.pop(i - 1)
                tokenMap.pop(i - 1)
                return unambigify(tokens, tokenMap)
        elif j == "else":
            if tokens[i + 1] == "if":
                tokens[i] = "elseif"
                tokens.pop(i + 1)
                tokenMap.pop(i + 1)
                return unambigify(tokens, tokenMap)
        elif j == "-":
            if tokens[i - 1] in [i[0] for i in variables] + [")", "]", "}"] or tokens[i - 1][0].isnumeric():
                tokens[i] = "binary-"
            else:
                tokens[i] = "unary-"
        elif j == "+":
            if tokens[i - 1] in [i[0] for i in variables] + [")", "]", "}"] or tokens[i - 1][0].isnumeric():
                tokens[i] = "binary+"
            else:
                tokens[i] = "unary+"
        elif j == "&":
            if tokens[i - 1] in [i[0] for i in variables] + [")", "]", "}"] or tokens[i - 1][0].isnumeric():
                tokens[i] = "binary&"
            else:
                tokens[i] = "unary&"
        elif j == "*":
            if tokens[i - 1] in [i[0] for i in variables] + [")", "]", "}"] or tokens[i - 1][0].isnumeric():
                tokens[i] = "binary*"
            else:
                tokens[i] = "unary*"
    return tokens, tokenMap

def numbersDontFitInBITS(tokens: list, tokenMap: list, BITS: int) -> str:
    for i, j in enumerate(tokens):
        if j[0].isnumeric():
            if int(j, 0) >= 2 ** BITS:
                return str(tokenMap[i])
    return ""

def invalidSymbol(tokens: list, tokenMap: list) -> str:
    for i, j in enumerate(tokens):
        if (not(j[0].isalpha())) and (j[0] != "_") and (j[0] not in ("£", "%")) and (j[0] not in "({[]});") and (not(j[0].isnumeric())):
            if j not in ("!", "~", "unary-", "unary+", "unary*", "sizeof", "binary*", "/", "%", "binary+", "binary-", "<<", ">>", "<", "<=", ">", ">=", "==", "!=", "&", "^", "|", "&&", "||", "=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", ","):
                return str(tokenMap[i])
    return ""

def findMain(tokens: list) -> bool:
    for i in tokens:
        if i == "main":
            return True
    return False

def closeSquare(tokens: list, i: int) -> int:
    count = 0
    if tokens[i] == "[":
        count += 1
    i += 1
    while (count > 0) and (i < len(tokens)):
        if tokens[i] == "[":
            count += 1
        elif tokens[i] == "]":
            count -= 1
        i += 1
    return i

def closeSquiggly(tokens: list, i: int, tokenMap: list) -> int:
    count = 0
    num = 0
    if tokens[i] == "{":
        count += 1
    i += 1
    while (count > 0) and (i < len(tokens)):
        if tokens[i] == "{":
            count += 1
        elif tokens[i] == "}":
            count -= 1
        elif tokens[i] == ",":
            num += 1
            tokens.insert(i, "=")
            tokenMap.insert(i, tokenMap[i])
            i += 1
        i += 1
    return i, tokens, tokenMap, num




