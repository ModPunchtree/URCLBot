
# 4: Generate URCL
    # 1: traverse tokens left to right, converting to URCL
    # 2: return URCL code as a list with markers for temporary variables

def generateURCL(tokens: list, tokenMap: list, allVariables: list, allFunctions: list, allArrays: list, MINREG: int, BITS: int) -> list:
    global uniqueNum; uniqueNum = 0
    global functionScope; functionScope = "global"
    global definedVariables; definedVariables = [] # just names
    global variables; variables = [] # name + _scope, type
    global definedFunctions; definedFunctions = [] # just names
    global functions; functions = [] # name + _scope, type
    global definedArrays; definedArrays = [] # just names
    global arrays; arrays = [] # name + _scope, type, length
    global registers; registers = ["" for i in range(MINREG)]
    global heap; heap = []
    global output; output = []

    tokenNumber = 0
    while tokenNumber < len(tokens):
        token = tokens[tokenNumber]

        if token in ("auto", "auto*"):
            # auto or auto*

            if tokens[tokenNumber - 1] in allVariables:
                # variable
                createVariable(tokens[tokenNumber - 1], token)
                tokens.pop(tokenNumber)
                tokenNumber = 0
                
            elif tokens[tokenNumber - 1] in allFunctions:
                # function
                pass

            elif tokens[tokenNumber - 1] in allArrays:
                # array
                pass

        # while
        # if elseif else
        # asm
        # $return

        elif token in ("--", "++", "autoTypeCast", "auto*TypeCast", "sizeof", "unary&", "unary*", "unary+", "unary-", "~", "!", "auto", "auto*"):
            # unary symbol
            pass
        elif token in ("||", "&&", "|", "binary&", "!=", "==", ">=", ">", "<=", "<", ">>", "<<", "binary-", "binary+", "%", "/", "binary*"):
            # binary symbol
            pass
        elif token in (">>=", "<<=", "^=", "|=", "&=", "%=", "/=", "*=", "-=", "+=", "="):
            # assignment symbol
            pass

        elif (token[0].isnumeric()) or (token in definedVariables) or (token.startswith("%")) or (token == "return"):
            # number or variable or %array or return
            tokenNumber += 1

        else:
            raise Exception("FATAL - Unrecognised token: " + token)

    return output

def uniqueNumber() -> str:
    global uniqueNum
    uniqueNum += 1
    return str(uniqueNum)

def createVariable(name: str, type: str) -> str:
    if not(name.endswith("_" + functionScope)):
        name += "_" + functionScope
    for i in name:
        if ((not(i.isnumeric)) and (not(i.isalpha)) and (i != "_")):
            raise Exception("FATAL - Invalid variable name: " + name)
    if (name in registers) or (name in heap):
        raise Exception("FATAL - Tried to define already existing variable: " + name)
    
    if "" in registers:
        #location = "R" + str(registers.index("") + 1)
        registers[registers.index("")] = name
    elif "" in heap:
        #location = "M" + str(heap.index(""))
        heap[heap.index("")] = name
    else:
        #location = "M" + str(len(heap))
        heap.append(name)

    variables.append([name, type])
    definedVariables.append(name)
    return name

def createTEMP() -> str:
    name = "TEMP_" + uniqueNumber()
    return createVariable(name, "auto")

def fetch(name: str, targetLocation: str):
    preserveName = registers[int(targetLocation[1:]) - 1]
    if preserveName != "":
        if "" in registers:
            output.append("MOV R" + str(registers.index("") + 1) + ", " + targetLocation)
            registers[registers.index("")] = preserveName
        elif "" in heap:
            output.append("STR M" + str(heap.index("")) + ", " + targetLocation)
            heap[heap.index("")] = preserveName
        else:
            output.append("STR M" + str(len(heap)) + ", " + targetLocation)
            heap.append(preserveName)
        registers[int(targetLocation[1:]) - 1] = ""

    if name[0].isnumeric():
        output.append("IMM " + targetLocation + ", " + name)
        return

    if name not in definedVariables:
        name += "_" + functionScope

    if name in definedVariables:
        if name in registers:
            location = "R" + str(registers.index(name) + 1)
            output.append("MOV " + targetLocation + ", " + location)
        else:
            location = "M" + str(heap.index(name))
            output.append("LOD " + targetLocation + ", " + location)
    else:
        raise Exception("FATAL - Tried to fetch variable that doesn't exist: " + name)

def copyFetch(name: str, targetLocation: str):
    preserveName = registers[int(targetLocation[1:]) - 1]
    if preserveName != "":
        if "" in registers:
            output.append("MOV R" + str(registers.index("") + 1) + ", " + targetLocation)
            registers[registers.index("")] = preserveName
        elif "" in heap:
            output.append("STR M" + str(heap.index("")) + ", " + targetLocation)
            heap[heap.index("")] = preserveName
        else:
            output.append("STR M" + str(len(heap)) + ", " + targetLocation)
            heap.append(preserveName)
        registers[int(targetLocation[1:]) - 1] = ""

    if name[0].isnumeric():
        output.append("IMM " + targetLocation + ", " + name)
        return

    if name not in definedVariables:
        name += "_" + functionScope

    if name in definedVariables:
        if name in registers:
            location = "R" + str(registers.index(name) + 1)
            output.append("MOV " + targetLocation + ", " + location)
        else:
            location = "M" + str(heap.index(name))
            output.append("LOD " + targetLocation + ", " + location)
    else:
        raise Exception("FATAL - Tried to fetch variable that doesn't exist: " + name)
