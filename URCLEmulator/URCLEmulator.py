
from URCLEmulator.constants import numberOfOps, urcl, validOpTypes

def emulate(raw: str) -> str:
    
    # pre-process
    # 1 remove spaces
    # 2 remove line comments
    
    # headers
    # 1 find word length header, else assume 8 bits
    # 2 find MINREG, else calculate it #########################################################
    # 3 find MINRAM, MINSTACK delete it
    # 4 find IMPORT, return error
    
    # setup
    # 1 make global list for registers + ram + SP
    # 2 resolve define macros
    # 3 replace labels with literals
    # 4 replace relatives with literals
    # 5 put code in ram, then set M0 offset
    # 6 put DW values into memory
    # 7 PC = 0, R0 = 0, branch = False, ect.
    
    # main
    # 1 find instruction
    # 2 list of ops
    # 3 get op types
    # 4 check types are valid and check number of ops
    # 5 check if fetched operands are uninitialised -> append warning
    # 6 check if write location is not valid -> return error or append warning
    # 7 fetch values from reg/ram
    # 8 do operation
    # 9 truncate result
    # 10 write result
    # 11 R0 = 0
    # 12 if not branch -> PC += 1
    
    ################################################
    
    # pre-process
    
    ################################################
    
    # 1 remove spaces
    global code
    code = raw[5:]
    code = code.replace(" ", "")
    code = code.replace("$", "R")
    code = code.replace("#", "M")
    code = code.split("\n")
    
    # 2 remove line comments
    code = [code[i][: code[i].find("//")] if code[i].find("//") != -1 else code[i] for i in range(len(code))]
    
    # headers
    # 1 find word length header, else assume 8 bits
    BITS = findBITSHeader()

    # 2 find MINREG, else calculate it
    MINREG = findMINREGHeader()
    
    # 3 find MINRAM, MINSTACK delete it
    MINRAM = findMINRAMHeader()
    MINSTACK = findMINSTACKHeader()
    
    # 4 find IMPORT, RUN RAM, return error
    findIMPORTRUNHeader()
    
    ################################################
    
    # setup
    
    ################################################
    
    # 1 make global list for registers + ram + SP
    registers = [2 ** BITS - 1 for i in range(MINREG + 1)]
    uninitialisedReg = [True for i in registers]
    registers[0] = 0
    uninitialisedReg[0] = False
    memory = [2 ** BITS - 1 for i in range(MINRAM)]
    
    global SP; SP = 2 ** BITS
    
    # 2 resolve define macros
    resolveDefineMacros()
    
    # 3 replace labels with literals
    resolveLabels()
    
    # 4 replace relatives with literals
    resolveRelatives()
    
    # 5 put code in ram, then set M0 offset
    putCodeInRAM()
    M0 = len(code)
    uninitialisedMem = [True if i < len(code) else False for i in memory]
    
    # 6 put DW values into memory
    for i, j in enumerate(code):
        if j.startswith("DW"):
            memory[i] = int(j[2:], 0)
    
    # 7 PC = 0, R0 = 0, branch = False, ect.
    PC = 0
    branch = False
    cycleLimit = 1000
    totalCycles = 0
    warnings = ()
    
    ################################################
    
    # main
    
    ################################################
    
    while totalCycles < cycleLimit:
        instruction = memory[PC]
        
        # 1 find instruction
        op = fetchInstruction(instruction)

        # 2 get list of ops
        ops = getOps(instruction[len(op): ])
        
        # 3 get op types
        opTypes = getOpsType(ops)
        
        # 4 check types are valid and check number of ops
        if invalidNumberOfOps(op, ops):
            raise Exception("FATAL - Invalid number of operands in instruction: " + instruction)
        if invalidOpTypes(op, opTypes):
            raise Exception("FATAL - Invalid operand types in instruction: " + instruction)
        
        # 5 check if fetched operands are uninitialised -> append warning
        if uninitialisedFetch():
            warnings.append("This instruction: " + instruction + "\nFetches an uninitialised register or memory location")
        
        # 6 check if write location is not valid -> return error or append warning
        if writingToR0(ops):
            warnings.append("This instruction: " + instruction + "\nHas R0 as the first operand, it is generally bad practice to have R0 here")

        # 7 fetch values from reg/ram
        # 8 do operation
        # 9 truncate result
        # 10 write result
        doWork(op, ops, opTypes)
        
        totalCycles += 1
    
    return "\n".join(code)

################################################

# Functions

################################################

def findBITSHeader() -> int:
    for i in range(len(code)):
        if code[i].startswith("BITS"):
            code.pop(i)
            if code[i].find("=") != -1:
                return int(code[i][code[i].find("=") + 1:], 0)
            else:
                return int(code[i][4:], 0)
    return 8

def findMINREGHeader() -> int:
    for i in range(len(code)):
        if code[i].startswith("MINREG"):
            code.pop(i)
            return int(code[i][6:], 0)
    return 8

def findMINRAMHeader() -> int:
    MINRAM = 2 ** BITS
    for i in range(len(code)):
        if code[i].startswith("MINRAM"):
            MINRAM = int(code[i][6:], 0)
            code.pop(i)
            return MINRAM
    return MINRAM

def findMINSTACKHeader() -> int:
    MINSTACK = 0
    for i in range(len(code)):
        if code[i].startswith("MINSTACK"):
            MINSTACK = int(code[i][8:], 0)
            code.pop(i)
            return MINSTACK
    return MINSTACK

def findIMPORTRUNHeader() -> None:
    for i in code:
        if i.startswith("IMPORT"):
            raise Exception("FATAL - Libraries are not supported on this emulator")
        elif i == "RUNROM":
            raise Exception("FATAL - RUN ROM is not supported on this emulator")

def resolveDefineMacros() -> None:
    for i in range(len(code)):
        if code[i].startswith("@define"):
            macro = code[i][: code[i].index(",")]
            definition = code[i][code[i].index(",") + 1: ]
            code.pop(i)
            code = [j.replace("@" + macro, definition) for j in code]
            return resolveDefineMacros()

def resolveLabels() -> None:
    for i in range(len(code)):
        if code[i].startswith("."):
            code = [j.replace(code[i], str(i)) for j in code]
            code.pop(i)
            return resolveLabels()

def resolveRelatives() -> None:
    for i in range(len(code)):
        if code[i].find("+") != -1:
            num = code[i][code[i].find("+") + 1: ]
            if num.find(",") != -1:
                num = num[: num.find(",")]
            num = int(num, 0)
            num = str(i + num)
            code[i] = code[i][: code[i].find("+")] + num + code[i][code[i].find("+") + len(num) + 1: ]

def putCodeInRAM() -> None:
    for i in range(len(code)):
        memory[i] = code[i]

def fetchInstruction(instruction: str) -> None:
    if instruction[5: ] in urcl():
        temp = 5
    elif instruction[4: ] in urcl():
        temp = 4
    elif instruction[3: ] in urcl():
        temp = 3
    elif instruction[2: ] in urcl():
        temp = 2
    else:
        raise Exception("FATAL - Unrecognised instruction: " + instruction)

    return instruction[temp: ]

def getOps(text: str) -> tuple:
    answer = ()
    char = 0
    temp = ""
    while char < len(text):
        if text[char] == ",":
            answer += (temp)
            temp = ""    
        else:
            temp += text[char]
        char += 1
    if temp:
        answer += (temp)
    return answer

def getOpsType(ops: tuple) -> tuple:
    answer = ()
    for i in ops:
        if i.startswith("R"):
            answer += ("REG")
        elif i.startswith("M"):
            answer += ("MEM")
        elif i[0].isnumeric():
            answer += ("IMM")
        elif i.startswith("%"):
            answer += ("PORT")
        else:
            answer += (i)

def invalidNumberOfOps(op: str, ops: tuple) -> bool:
    if len(ops) == numberOfOps()[numberOfOps().index(op)]:
        return False
    return True

def invalidOpTypes(op: str, opTypes: tuple) -> bool:
    index = urcl().index(op)
    if opTypes in validOpTypes()[index]:
        return False
    return True

def uninitialisedFetch(op: str, ops: tuple, opTypes: tuple, uninitialisedReg: list, uninitialisedMemory: list) -> bool:
    temp = False
    if (len(ops) == 1) and (op != "POP"):
        num = int(ops[0][1:])
        if opTypes[0] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[0] == "MEM":
            temp = uninitialisedMemory[num]

    elif op in ("BOD", "BEV", "BRZ", "BZR", "BNZ", "BZN", "BRN", "BRP"):
        num = int(ops[0][1:])
        if opTypes[0] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[0] == "MEM":
            temp = uninitialisedMemory[num]
        num = int(ops[1][1:])
        if opTypes[1] == "REG":
            temp = uninitialisedReg[num] or temp
        elif opTypes[1] == "MEM":
            temp = uninitialisedMemory[num] or temp

    elif (len(ops) == 2) and (op != "IN"):
        num = int(ops[1][1:])
        if opTypes[1] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[1] == "MEM":
            temp = uninitialisedMemory[num]
    
    elif op in ("BGR", "BRL", "BRG", "BRE", "BNE", "BLE"):
        num = int(ops[0][1:])
        if opTypes[0] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[0] == "MEM":
            temp = uninitialisedMemory[num]
        num = int(ops[1][1:])
        if opTypes[1] == "REG":
            temp = uninitialisedReg[num] or temp
        elif opTypes[1] == "MEM":
            temp = uninitialisedMemory[num] or temp
        num = int(ops[2][1:])
        if opTypes[2] == "REG":
            temp = uninitialisedReg[num] or temp
        elif opTypes[2] == "MEM":
            temp = uninitialisedMemory[num] or temp
    
    elif len(ops) == 3:
        num = int(ops[1][1:])
        if opTypes[1] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[1] == "MEM":
            temp = uninitialisedMemory[num]
        num = int(ops[2][1:])
        if opTypes[2] == "REG":
            temp = uninitialisedReg[num] or temp
        elif opTypes[2] == "MEM":
            temp = uninitialisedMemory[num] or temp
            
    return temp

def writingToR0(ops: tuple) -> bool:
    if len(ops) > 0:
        if ops[0] == "R0":
            return True
    return False

def doWork(op: str, ops: tuple, opTypes: tuple):
    
    # 7 fetch values from reg/ram
    pass
    
    # 8 do operation
    # 9 truncate result
    # 10 write result


