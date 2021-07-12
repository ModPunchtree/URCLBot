from bCompilerOLD.constants import alpha, operators, split

def tokenize(code: str) -> tuple:
    
    def read(code: str, target: list, start: int = 0) -> tuple:
        temp = []
        if code[start] in target:
            temp.append(-1)
        start += 1
        for i in target:
            if code[start:].find(i) != -1:
                temp.append(code[start:].find(i))
        if len(temp) != 0:
            end = min(temp) + start
        else:
            end = len(code)
        text = code[start - 1: end]
        return text, end
    
    functions = []
    variables = [] 
    tokens = []
    tokenMap = []
    index = 0
    while (index < len(code) and (index != -1)):
        char = code[index]
        if char == " ":
            index += 1
            
        elif char.isnumeric():
            number, index = read(code, (operators() + (" ", ";", "(", ")", "{", "}")), index)
            tokens.append(number)
            tokenMap.append(index)
            
        elif char in alpha():
            tokenMap.append(index)
            text, index = read(code, (operators() + (" ", ";", "(", ")", "{", "}")), index)
            tokens.append(text)
            temp2 = read(code, (operators() + (";", "(", ")", "{", "}") + tuple(split(alpha()))), index)
            if text in ("if", "else", "while", "asm", "return", "auto"):
                pass
            elif temp2[1] < len(code):
                if code[temp2[1]] == "(":
                    if tokens[-2] == "auto":
                        tokens[-1] = "£" + tokens[-1]
                    functions.append(text)
                else:
                    variables.append(text)
                
        elif char in operators():
            tokenMap.append(index)
            if code[index: index + 3] in operators():
                length = 3
            elif code[index: index + 2] in operators():
                length = 2
            else:
                length = 1
            tokens.append(code[index: index + length])
            index += length
            
        elif char in (";", "(", ")", "{", "}"):
            tokenMap.append(index)
            tokens.append(char)
            index += 1
            
        else:
            return "FATAL - Unrecognised token: " + char + "\n" + code[index - 15: index + 15] + "\n               ^"
    
    for i in range(len(tokens) - 1):
        if tokens[i] == "else":
            if tokens[i + 1] == "if":
                tokens[i] = "elseif"
                tokens.pop(i + 1)
                tokenMap.pop(i + 1)
                i = 0
    for i in range(len(tokens)):
        if tokens[i] in ("if", "elseif", "else", "while", "asm"):
            tokens[i] = "£" + tokens[i]
    
    return tokens, tokenMap, functions, variables