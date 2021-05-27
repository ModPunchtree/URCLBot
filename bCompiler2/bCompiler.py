
# 0: Clean Code
# 1: Tokeniser
# 2: Preprocess
# 3: Reverse Polish
# 4: Generate URCL
# 5: Compiler Optimisations
# 6: General Optimisations

from bCompiler2.reversePolish import reversePolish
from bCompiler2.preprocess import preprocess
from bCompiler2.tokeniser import tokenise

def bCompiler2(raw: str) -> str:
    """
    Converts raw text into B code or an error.
    Returns a string.
    """
    
    # 0: Clean Code
    global BITS
    global MINREG
    global code
    code, BITS, MINREG = cleanCode(raw)
    
    # 1: Tokeniser
    tokens, tokenMap = tokenise(code)

    # 2: Preprocess
    variables, lists, functions, tokens, tokenMap = preprocess(tokens, tokenMap, code, BITS)

    # 3: Reverse Polish
    tokens, tokenMap = reversePolish(variables, lists, functions, tokens, tokenMap)

    return tokens

def cleanCode(raw: str) -> tuple:
    """
    Works out BITS and MINREG from the raw text input.
    Removes new lines and multiple spaces from code.
    Returns: code: str, BITS: int, MINREG: int
    """
    
    firstLine = raw[: raw.index("\n")]
    firstLine = "".join([i if i != " " else "" for i in firstLine])
    
    if firstLine.startswith("$B"):
        if firstLine.find(",") != -1:
            BITS = int(firstLine[2: firstLine.index(",")], 0)
            MINREG = int(firstLine[firstLine.index(",") + 1: ], 0)
        else:
            BITS = int(firstLine[2: ], 0)
            MINREG = 8
    else:
        BITS = 8
        MINREG = 8
        
    if BITS > 16:
        raise Exception("FATAL - Word length cannot be more than 16 bits")
    if MINREG > 2 ** BITS:
        raise Exception("FATAL - Cannot have more than " + str(2 ** BITS) + " registers")
    
    code = raw[raw.index("\n"): ].replace("\n", " ")
    code = code.replace("  ", " ")
    code = code.replace("  ", " ")
    code = " "*15 + code + " "*15
    
    return code, BITS, MINREG

