
# 1: loop over chars in code
# 2: read each identifier/symbol into a list
# 3: return tokens, tokenMap

def tokenise(code: str) -> tuple:
    """
    Turn cleaned code into list of tokens and tokenMap.
    Returns: tokens: list, tokenMap: list
    """

    tokens = []
    tokenMap = []
    global symbols; symbols = "+-=*/<>,.!&~|^"
    singleSymbols = "({[]});"

    # 1: loop over chars in code
    num = 0
    while num < len(code):
        char = code[num]
        
        if char == " ":
            num += 1
            
        elif char in singleSymbols:
            tokens.append(char)
            tokenMap.append(num)
            num += 1
            
        elif char in symbols:
            #symbol
            tokenMap.append(num)
            symbol, num = readSymbol(code, num)
            tokens.append(symbol)
            
        elif char.isnumeric():
            #number
            tokenMap.append(num)
            number, num = readNum(code, num)
            tokens.append(number)
            
        elif char.isalpha() or char in ("_", "%"):
            # identifier
            tokenMap.append(num)
            identifier, num = readIdentifier(code, num)
            tokens.append(identifier)
    
    return tokens, tokenMap

def readNum(code: str, num: int) -> str:
    answer = ""
    while num < len(code):
        if code[num].isnumeric() or (code[num] == "x" and num == 1):
            answer += code[num]
            num += 1
        else:
            break
    answer = str(int(answer, 0))
    return answer, num

def readIdentifier(code: str, num: int) -> str:
    answer = ""
    while num < len(code):
        if code[num].isalpha() or code[num] in ("_", "%") or code[num].isnumeric():
            answer += code[num]
            num += 1
        else:
            break
    return answer, num

def readSymbol(code: str, num: int) -> str:
    answer = ""
    while num < len(code):
        if code[num] in symbols:
            answer += code[num]
            num += 1
        else:
            break
    return answer, num


