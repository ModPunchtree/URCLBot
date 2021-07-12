from bCompilerOLD.generateURCL import generateURCL
from bCompilerOLD.reversePolish import reversePolish
from bCompilerOLD.cleanCode import cleanCode
from bCompilerOLD.tokenizer import tokenize
from bCompilerOLD.optimiser import optimise
from bCompilerOLD.headers import headers

def compile(raw: str, length: int, reg: int) -> str:
    
    code = raw.split("\n")
    code = cleanCode(code)
    
    temp = tokenize(code)
    if type(temp) == str:
        return temp
    tokens, tokenMap, functions, variables = temp
    
    temp = reversePolish(tokens, tokenMap, functions, variables, code)
    if type(temp) == str:
        return temp
    tokens, tokenMap = temp

    try:
        tokens.index("£main")
        try:
            tokens.index("main")
        except:
            tokens.append("main")
            tokenMap.append(-1)
    except:
        pass
    
    output = generateURCL(tokens, tokenMap, functions, variables, length, reg, code)
    if type(output) == str:
        return output
    
    output = optimise(output)

    output = headers(output, length)

    output = "\n".join(output)
    return output




