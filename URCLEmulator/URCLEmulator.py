
from URCLEmulator.constants import alpha, fetchThree
from URCLEmulator.constants import fetchNone, fetchOne, fetchOneTwo, fetchOneTwoThree, fetchTwo, fetchTwoThree, numberOfOps, urcl, validOpTypes

def emulate(raw: str, connection: bool = False, outputs: bool = True) -> str:
    global offline
    offline = connection
    # pre-process
    # 1 remove spaces
    # 2 remove line comments
    
    # headers
    # 1 find word length header, else assume 8 bits
    # 2 find MINREG, else calculate it #########################################################
    # 3 find MINHEAP, MINSTACK delete it
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
    if raw.startswith("$URCL"):
        code = raw[5:]
    else:
        code = raw
    code = code.replace(" ", "")
    code = code.replace("$", "R")
    code = code.replace("#", "M")
    code = code.split("\n")
    
    # 2 remove line comments
    code = [code[i][: code[i].find("//")] if code[i].find("//") != -1 else code[i] for i in range(len(code))]
    code = list(filter(None, code))
    if code[-1] != "HLT":
        code.append("HLT")
    
    # headers
    # 1 find word length header, else assume 8 bits
    global BITS; BITS = findBITSHeader()
    #if BITS > 16:
    #    raise Exception("FATAL - BITS cannot be more than 16")

    # 2 find MINREG, else calculate it
    MINREG = findMINREGHeader()
    if MINREG > 2 ** BITS:
        raise Exception("FATAL - MINREG cannot be more than " + str(2 ** BITS))
    elif MINREG > 65536:
        raise Exception("FATAL - MINREG cannot be more than 65536")
    
    # 3 find MINHEAP, MINSTACK delete it
    MINHEAP = findMINHEAPHeader()
    if MINHEAP > 2 ** BITS:
        raise Exception("FATAL - MINHEAP cannot be more than " + str(2 ** BITS))
    MINSTACK = findMINSTACKHeader()
    if MINSTACK > 2 ** BITS:
        raise Exception("FATAL - MINSTACK cannot be more than " + str(2 ** BITS))
    
    # 4 find IMPORT, RUN RAM, return error
    findIMPORTRUNHeader()
    
    ################################################
    
    # setup
    
    ################################################
    
    # 1 resolve define macros
    resolveDefineMacros()
    
    # 2 replace labels with literals
    resolveLabels()
    
    # 3 make global list for registers + ram + SP
    global registers
    registers = [2 ** BITS - 1 for i in range(MINREG + 1)]
    global uninitialisedReg
    uninitialisedReg = [True for i in registers]
    registers[0] = 0
    uninitialisedReg[0] = False
    global memory
    memory = [2 ** BITS - 1 for i in range(min(MINHEAP + MINSTACK + len(code), 2 ** BITS))]
    global SP; SP = len(memory)
    
    # 4 replace relatives with literals
    resolveRelatives()
    
    # 5 put code in ram, then set M0 offset
    global M0; M0 = len(code)
    putCodeInRAM()
    global uninitialisedMem
    uninitialisedMem = [True if i < len(code) else False for i in range(len(memory))]
    
    # 6 put DW values into memory
    for i, j in enumerate(code):
        if j.startswith("DW"):
            if j[2: ].startswith("M"):
                memory[i] = M0 + int(j[3: ], 0)
            else:
                memory[i] = int(j[2:], 0)
    
    # 7 PC = 0, R0 = 0, branch = False, ect.
    global PC; PC = 0
    global branch; branch = False
    cycleLimit = 1000
    global totalCycles; totalCycles = 0
    global warnings; warnings = ()
    global outputList; outputList = []
    
    ################################################
    
    # main
    
    ################################################
    
    global instruction
    while totalCycles < cycleLimit:
        instruction = memory[PC]
        if type(instruction) != str:
            raise Exception("FATAL - Tried to execute non-instruction: " + str(instruction))
        
        # 1 find instruction
        op = fetchInstruction(instruction)

        # check for stack underflow
        if ((op in ("RET", "POP")) and (correctValue(SP) == 0)) or (SP > len(memory)):
            raise Exception("FATAL - Stack underflow")

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
        if uninitialisedFetch(op, ops, opTypes, uninitialisedReg, uninitialisedMem):
            warnings += ("This instruction: " + instruction + "\nFetches an uninitialised register or memory location",)
        
        # 6 check if write location is not valid -> return error or append warning
        if writingToR0(ops):
            warnings += ("This instruction: " + instruction + "\nHas R0 as the first operand, it is generally bad practice to have R0 here", )

        if op == "HLT":
            break

        # 7 fetch values from reg/ram
        fetchList = fetchOps(op, ops)
        
        # 8 do operation
        result = doOperation(op, fetchList)
        
        # 9 truncate result
        result = correctValue(result)
        
        # 10 write result
        writeResult(op, result, ops, fetchList)
        
        # 11 R0 = 0
        registers[0] = 0
        
        # 12 if not branch -> PC += 1
        if not branch:
            PC += 1
        else:
            branch = False
        
        totalCycles += 1
    
        if outputs:
            print("\n".join(["WARNING - " + i for i in warnings]) + 
                  "\n\nInstruction just completed = " + str(instruction) +
                  "\nPC = " + str(PC) +
                  "\nTotal number of cycles: " + str(totalCycles) + 
                  "\nStack Pointer = " + str(correctValue(SP)) +
                  "\nTotal memory size = " + str(len(memory)) +
                  "\n\nRegisters:\n" + 
                  "\n".join(["R" + str(i) + ": " + str(j) for i, j in enumerate(registers)][1:]) +
                  "\n\nMemory:    (M0 = " + str(M0) + ")\n" +
                  "\n".join(filter(None, ["M" + str(i - M0) + ": " + str(j) if uninitialisedMem[i] and type(j) != str and i >= M0 else "" for i, j in enumerate(memory)])) +
                  "\n\nRaw Output:\n" +
                  ", ".join(["0x" + hex(i)[2:].upper() for i in outputList]) +
                  "\n\nAscii Output:\n" +
                  "".join([chr(i % 65536) for i in outputList]))
    
    # return warnings + all registers/initialised memory + outputList
    return ("\n".join(["WARNING - " + i for i in warnings]) + 
            "\n\nPC = " + str(PC) +
            "\nTotal number of cycles: " + str(totalCycles) + 
            "\nStack Pointer = " + str(correctValue(SP)) +
            "\nTotal memory size = " + str(len(memory)) +
            "\n\nRegisters:\n" + 
            "\n".join(["R" + str(i) + ": " + str(j) for i, j in enumerate(registers)][1:]) +
            "\n\nMemory:    (M0 = " + str(M0) + ")\n" +
            "\n".join(filter(None, ["M" + str(i - M0) + ": " + str(j) if uninitialisedMem[i] and type(j) != str and i >= M0 else "" for i, j in enumerate(memory)])) +
            "\n\nOutput:\n" +
            ", ".join(["0x" + hex(i)[2:].upper() for i in outputList]) +
            "\n\nAscii Output:\n" +
            "".join([chr(i % 65536) for i in outputList]))

################################################

# Functions

################################################

def findBITSHeader() -> int:
    for i in range(len(code)):
        if code[i].startswith("BITS"):
            temp = code[i]
            code.pop(i)
            if temp.find("=") != -1:
                return int(temp[len(temp) - temp[::-1].find("="):], 0)
            else:
                return int(temp[4:], 0)
    return 8

def findMINREGHeader() -> int:
    for i in range(len(code)):
        if code[i].startswith("MINREG"):
            temp = int(code[i][6:], 0)
            code.pop(i)
            return temp
    return 8

def findMINHEAPHeader() -> int:
    if BITS > 16:
        MINHEAP = 2 ** 16
    else:
        MINHEAP = 2 ** BITS
    for i in range(len(code)):
        if code[i].startswith("MINHEAP"):
            MINHEAP = int(code[i][6:], 0)
            code.pop(i)
            return MINHEAP
    return MINHEAP

def findMINSTACKHeader() -> int:
    MINSTACK = 8
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
    global code
    for i in range(len(code)):
        if code[i].startswith("@define"):
            macro = code[i][: code[i].index(",")]
            definition = code[i][code[i].index(",") + 1: ]
            code.pop(i)
            code = [j.replace("@" + macro, definition) for j in code]
            return resolveDefineMacros()

def resolveLabels() -> None:
    global code
    for i in range(len(code)):
        if code[i].startswith("."):
            x = code[i]
            for j, k in enumerate(code):
                if k.find(x) != -1 and k[k.find(x) + len(x): k.find(x) + len(x) + 1] not in tuple(alpha() + "0123456789"):
                    code[j] = k.replace(x, str(i))
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
        while code[i].find("M") != -1:
            if code[i][code[i].find("M") + 1].isnumeric():
                num = readNum(code[i][code[i].find("M") + 1: ])
                code[i] = code[i].replace("M" + str(num), str(num + M0), 1)
            else:
                code[i] = code[i].replace("M", "#", 1)
        memory[i] = code[i].replace("#", "M")

def readNum(text: str) -> int:
    answer = ""
    for i in text:
        if i.isnumeric() or i == "x":
            answer += i
        else:
            return int(answer, 0)
    return int(answer, 0)

def fetchInstruction(instruction: str) -> None:
    if instruction[: 5] in urcl():
        temp = 5
    elif instruction[: 4] in urcl():
        temp = 4
    elif instruction[: 3] in urcl():
        temp = 3
    elif instruction[: 2] in urcl():
        temp = 2
    else:
        raise Exception("FATAL - Unrecognised instruction: " + instruction)

    return instruction[: temp]

def getOps(text: str) -> tuple:
    answer = ()
    char = 0
    temp = ""
    while char < len(text):
        if text[char] == ",":
            answer += (temp,)
            temp = ""    
        else:
            temp += text[char]
        char += 1
    if temp:
        answer += (temp,)
    return answer

def getOpsType(ops: tuple) -> tuple:
    answer = ()
    for i in ops:
        if i.startswith("R") or i == "SP":
            answer += ("REG",)
        elif i.startswith("M"):
            answer += ("MEM",)
        elif i[0].isnumeric():
            answer += ("IMM",)
        elif i.startswith("%"):
            answer += ("PORT",)
        else:
            answer += (i,)
    return answer

def invalidNumberOfOps(op: str, ops: tuple) -> bool:
    if len(ops) == numberOfOps()[urcl().index(op)]:
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
        if ops[0][0].isnumeric():
            num = int(ops[0], 0)
        elif ops[0] == "SP":
            num = 0
        else:
            num = int(ops[0][1:])
        if opTypes[0] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[0] == "MEM":
            temp = not uninitialisedMemory[num]

    elif op in ("BOD", "BEV", "BRZ", "BZR", "BNZ", "BZN", "BRN", "BRP"):
        if ops[0][0].isnumeric():
            num = int(ops[0], 0)
        elif ops[0] == "SP":
            num = 0
        else:
            num = int(ops[0][1:])
        if opTypes[0] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[0] == "MEM":
            temp = not uninitialisedMemory[num]
        if ops[1][0].isnumeric():
            num = int(ops[1], 0)
        elif ops[1] == "SP":
            num = 0
        else:
            num = int(ops[1][1:])
        if opTypes[1] == "REG":
            temp = uninitialisedReg[num] or temp
        elif opTypes[1] == "MEM":
            temp = not uninitialisedMemory[num] or temp

    elif (len(ops) == 2) and (op != "IN"):
        if ops[1].isnumeric():
            num = int(ops[1])
        elif ops[1] == "SP":
            num = 0
        elif ops[1][0].isnumeric():
            num = int(ops[1], 0)
        else:
            num = int(ops[1][1:], 0)
        if opTypes[1] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[1] == "MEM":
            temp = not uninitialisedMemory[num + M0]
    
    elif op in ("BGR", "BRL", "BRG", "BRE", "BNE", "BLE"):
        if ops[0][0].isnumeric():
            num = int(ops[0], 0)
        elif ops[0] == "SP":
            num = 0
        else:
            num = int(ops[0][1:])
        if opTypes[0] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[0] == "MEM":
            temp = not uninitialisedMemory[num]
        if ops[1][0].isnumeric():
            num = int(ops[1], 0)
        elif ops[1] == "SP":
            num = 0
        else:
            num = int(ops[1][1:])
        if opTypes[1] == "REG":
            temp = uninitialisedReg[num] or temp
        elif opTypes[1] == "MEM":
            temp = not uninitialisedMemory[num] or temp
        if ops[2][0].isnumeric():
            num = int(ops[2], 0)
        elif ops[2] == "SP":
            num = 0
        else:
            num = int(ops[2][1:])
        if opTypes[2] == "REG":
            temp = uninitialisedReg[num] or temp
        elif opTypes[2] == "MEM":
            temp = not uninitialisedMemory[num] or temp
    
    elif len(ops) == 3:
        if ops[1][0].isnumeric():
            num = int(ops[1], 0)
        elif ops[1] == "SP":
            num = 0
        else:
            num = int(ops[1][1:])
        if opTypes[1] == "REG":
            temp = uninitialisedReg[num]
        elif opTypes[1] == "MEM":
            temp = not uninitialisedMemory[num]
        if ops[2][0].isnumeric():
            num = int(ops[2], 0)
        elif ops[2] == "SP":
            num = 0
        else:
            num = int(ops[2][1:])
        if opTypes[2] == "REG":
            temp = uninitialisedReg[num] or temp
        elif opTypes[2] == "MEM":
            temp = not uninitialisedMemory[num] or temp
            
    return temp

def writingToR0(ops: tuple) -> bool:
    if len(ops) > 0:
        if ops[0] == "R0":
            return True
    return False

def fetchOps(op: str, ops: tuple) -> tuple:
    if op == "LLOD":
        return ("", fetch(str(fetch(ops[1], op) + fetch(ops[2], op)), op, True))
    elif fetchThree(op):
        return ("", "", fetch(ops[2], op))
    elif fetchTwoThree(op):
        return ("", fetch(ops[1], op), fetch(ops[2], op))
    elif fetchOneTwoThree(op):
        return (fetch(ops[0], op), fetch(ops[1], op), fetch(ops[2], op))
    elif op == "LOD":
        return ("", fetch(ops[1], op, True))
    elif fetchTwo(op):
        return ("", fetch(ops[1], op))
    elif fetchOneTwo(op):
        return (fetch(ops[0], op), fetch(ops[1], op))
    elif fetchOne(op):
        return (fetch(ops[0], op),)
    elif fetchNone(op):
        return ()
    else:
        raise Exception("FATAL - Failed to fetch operands for: " + instruction)

def fetch(operand: str, op: str, absMem: bool = False) -> int:
    global SP
    global warnings
    if op in ("POP", "RET"):
        temp = fetch(str(SP), "LOD", True)
        SP += 1
        return temp
    elif (operand == "SP") and (op == "LOD"):
        return memory[SP]
    elif operand == "PC":
        return PC
    elif operand == "SP":
        return SP
    elif op == "LOD" and operand.startswith("R"):
        num = int(operand[1:])
        num = registers[num]
        return memory[num]
    elif op == "IMM" and operand[0] == "M":
        return int(operand[1: ], 0) + M0
    elif operand.startswith("R"):
        num = int(operand[1:])
        return registers[num]
    elif operand.startswith("M"):
        num = int(operand[1:], 0)
        return memory[num + M0]
    elif operand.startswith("%"):
        if offline:
            while True:
                print("\n".join(["WARNING - " + i for i in warnings]) + 
                      "\n\nInstruction just completed = " + str(instruction) +
                      "\nPC = " + str(PC) +
                      "\nTotal number of cycles: " + str(totalCycles) + 
                      "\nStack Pointer = " + str(correctValue(SP)) +
                      "\nTotal memory size = " + str(len(memory)) +
                      "\n\nRegisters:\n" + 
                      "\n".join(["R" + str(i) + ": " + str(j) for i, j in enumerate(registers)][1:]) +
                      "\n\nMemory:    (M0 = " + str(M0) + ")\n" +
                      "\n".join(filter(None, ["M" + str(i - M0) + ": " + str(j) if uninitialisedMem[i] and type(j) != str and i >= M0 else "" for i, j in enumerate(memory)])) +
                      "\n\nRaw Output:\n" +
                      ", ".join(["0x" + hex(i)[2:].upper() for i in outputList]) +
                      "\n\nAscii Output:\n" +
                      "".join([chr(i % 65536) for i in outputList]))
                num = input("Type value for port " + operand + ": ")
                if num.isnumeric() or (num.startswith("'") and num.endswith("'")) or num.startswith("0x") or num.startswith("0b") or len(num) == 1:
                    if num.isnumeric() or num.startswith("0x") or num.startswith("0b"):
                        num2 = int(num, 0)
                        break
                    elif num.startswith("'") and num.endswith("'"):
                        try:
                            num2 = ord(num[1])
                            break
                        except:
                            pass
                    else:
                        try:
                            num2 = ord(num)
                            break
                        except:
                            pass
                else:
                    print("Invalid input try again")
            return num2
        else:
            warnings += ("IN instruction tried to fetch value from port: " + operand + "\nThis emulator does not support ports so it returned 0 instead.",)
            return 0
    elif operand[0].isnumeric() and absMem:
        num = int(operand, 0)
        return memory[num]
    elif operand[0].isnumeric():
        return int(operand, 0)
    else:
        raise Exception("FATAL - Invalid fetch location: " + operand)

def doOperation(op: str, fetchList: tuple) -> int:
    global SP
    if op == "ADD":
        return fetchList[1] + fetchList[2]
    elif op == "RSH":
        return fetchList[1] // 2
    elif op == "LOD":
        return fetchList[1]
    elif op == "STR":
        return fetchList[1]
    elif op == "JMP":
        return fetchList[0]
    elif op == "BGE":
        if fetchList[1] >= fetchList[2]:
            return 1
        return 0
    elif op == "NOR":
        return (2 ** BITS - 1) - (fetchList[1] | fetchList[2])
    elif op == "SUB":
        return fetchList[1] - fetchList[2]
    elif op == "MOV":
        return fetchList[1]
    elif op == "NOP":
        return 0
    elif op == "IMM":
        return fetchList[1]
    elif op == "LSH":
        return fetchList[1] * 2
    elif op == "INC":
        return fetchList[1] + 1
    elif op == "DEC":
        return fetchList[1] - 1
    elif op == "NEG":
        return -fetchList[1]
    elif op == "AND":
        return fetchList[1] & fetchList[2]
    elif op == "OR":
        return fetchList[1] | fetchList[2]
    elif op == "NOT":
        return (2 ** BITS - 1) - fetchList[1]
    elif op == "XNOR":
        return (2 ** BITS - 1) - (fetchList[1] ^ fetchList[2])
    elif op == "XOR":
        return fetchList[1] ^ fetchList[2]
    elif op == "NAND":
        return (2 ** BITS - 1) - (fetchList[1] & fetchList[2])
    elif op == "BRL":
        if fetchList[1] < fetchList[2]:
            return 1
        return 0
    elif op == "BRG":
        if fetchList[1] > fetchList[2]:
            return 1
        return 0
    elif op == "BRE":
        if fetchList[1] == fetchList[2]:
            return 1
        return 0
    elif op == "BNE":
        if fetchList[1] != fetchList[2]:
            return 1
        return 0
    elif op == "BOD":
        if (fetchList[1] % 2) == 1:
            return 1
        return 0
    elif op == "BEV":
        if (fetchList[1] % 2) == 0:
            return 1
        return 0
    elif op == "BLE":
        if fetchList[1] <= fetchList[2]:
            return 1
        return 0
    elif op in ("BRZ", "BZR"):
        if fetchList[1] == 0:
            return 1
        return 0
    elif op in ("BNZ", "BZN"):
        if fetchList[1] != 0:
            return 1
        return 0
    elif op == "BRN":
        if fetchList[1] >= 2 ** (BITS - 1):
            return 1
        return 0
    elif op == "BRP":
        if fetchList[1] < 2 ** (BITS - 1):
            return 1
        return 0
    elif op == "IN":
        return fetchList[1]
    elif op == "OUT":
        return fetchList[1]
    elif op == "PSH":
        return fetchList[0]
    elif op == "POP":
        num = memory[SP]
        SP += 1
        return num
    elif op == "CAL":
        return fetchList[0]
    elif op == "RET":
        num = memory[SP]
        SP += 1
        return num
    elif op == "HLT":
        return 0
    elif op == "MLT":
        return fetchList[1] * fetchList[2]
    elif op == "DIV":
        return fetchList[1] // fetchList[2]
    elif op == "MOD":
        return fetchList[1] % fetchList[2]
    elif op == "BSR":
        return fetchList[1] // 2 ** fetchList[2]
    elif op == "BSL":
        return fetchList[1] * 2 ** fetchList[2]
    elif op == "SRS":
        if fetchList[1] >= 2 ** (BITS - 1):
            return (fetchList[1] // 2) + 2 ** (BITS - 1)
        return fetchList[1] // 2
    elif op == "BSS":
        temp = fetchList[1]
        for i in range(fetchList[2]):
            if temp >= 2 ** (BITS - 1):
                temp = (temp // 2) + 2 ** (BITS - 1)
            temp //= 2
        return temp
    elif op == "SETE":
        if fetchList[1] == fetchList[2]:
            return 1
        return 0
    elif op == "SETNE":
        if fetchList[1] != fetchList[2]:
            return 1
        return 0
    elif op == "SETG":
        if fetchList[1] > fetchList[2]:
            return 1
        return 0
    elif op == "SETL":
        if fetchList[1] < fetchList[2]:
            return 1
        return 0
    elif op == "SETGE":
        if fetchList[1] >= fetchList[2]:
            return 1
        return 0
    elif op == "SETLE":
        if fetchList[1] <= fetchList[2]:
            return 1
        return 0
    elif op == "LLOD":
        return fetchList[1]
    elif op == "LSTR":
        return fetchList[2]
    else:
        raise Exception("FATAL - Invalid operation: " + op)

def correctValue(value: int) -> int:
    while value >= 2 ** BITS:
        value -= 2 ** BITS
    while value < 0:
        value += 2 ** BITS
    return value

def writeResult(op: str, result: int, ops: tuple, fetchList: tuple) -> None:
    global SP
    if op == "ADD":
        write(ops[0], result)
    elif op == "RSH":
        write(ops[0], result)
    elif op == "LOD":
        write(ops[0], result)
    elif op == "STR":
        if ops[0] == "SP":
            write(str(SP), result)
        elif ops[0].startswith("R"):
            write(str(fetch(ops[0], op, True)), result)
        else:
            write(ops[0], result)
    elif op == "JMP":
        write("PC", result)
    elif op == "BGE":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "NOR":
        write(ops[0], result)
    elif op == "SUB":
        write(ops[0], result)
    elif op == "MOV":
        write(ops[0], result)
    elif op == "NOP":
        pass
    elif op == "IMM":
        write(ops[0], result)
    elif op == "LSH":
        write(ops[0], result)
    elif op == "INC":
        write(ops[0], result)
    elif op == "DEC":
        write(ops[0], result)
    elif op == "NEG":
        write(ops[0], result)
    elif op == "AND":
        write(ops[0], result)
    elif op == "OR":
        write(ops[0], result)
    elif op == "NOT":
        write(ops[0], result)
    elif op == "XNOR":
        write(ops[0], result)
    elif op == "XOR":
        write(ops[0], result)
    elif op == "NAND":
        write(ops[0], result)
    elif op == "BRL":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "BRG":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "BRE":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "BNE":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "BOD":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "BEV":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "BLE":
        if result == 1:
            write("PC", fetchList[0])
    elif op in ("BRZ", "BZR"):
        if result == 1:
            write("PC", fetchList[0])
    elif op in ("BNZ", "BZN"):
        if result == 1:
            write("PC", fetchList[0])
    elif op == "BRN":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "BRP":
        if result == 1:
            write("PC", fetchList[0])
    elif op == "IN":
        write(ops[0], result)
    elif op == "OUT":
        outputList.append(result)
    elif op == "PSH":
        SP -= 1
        write(str(SP), result)
    elif op == "POP":
        write(ops[0], result)
    elif op == "CAL":
        SP -= 1
        write(str(SP), PC + 1)
        write("PC", result)
    elif op == "RET":
        write("PC", result)
    elif op == "HLT":
        pass
    elif op == "MLT":
        write(ops[0], result)
    elif op == "DIV":
        write(ops[0], result)
    elif op == "MOD":
        write(ops[0], result)
    elif op == "BSR":
        write(ops[0], result)
    elif op == "BSL":
        write(ops[0], result)
    elif op == "SRS":
        write(ops[0], result)
    elif op == "BSS":
        write(ops[0], result)
    elif op == "SETE":
        write(ops[0], result)
    elif op == "SETNE":
        write(ops[0], result)
    elif op == "SETG":
        write(ops[0], result)
    elif op == "SETL":
        write(ops[0], result)
    elif op == "SETGE":
        write(ops[0], result)
    elif op == "SETLE":
        write(ops[0], result)
    elif op == "LLOD":
        write(ops[0], result)
    elif op == "LSTR":
        if ops[0][0].isnumeric():
            base = int(ops[0], 0)
        elif ops[0][0] == "R":
            base = fetch(ops[0], op)
        else:
            base = int(ops[0][1:], 0)
        if ops[1][0].isnumeric():
            offset = int(ops[1], 0)
        elif ops[1][0] == "R":
            offset = fetch(ops[1], op)
        else:
            offset = int(ops[1][1:], 0)
        write(str(base + offset), result)
    else:
        raise Exception("FATAL - Invalid operation: " + op)

def write(location: str, value: int) -> None:
    global PC
    global branch
    global SP
    if location.startswith("R"):
        num = int(location[1:])
        registers[num] = value
        uninitialisedReg[num] = False
    elif location.startswith("M"):
        num = int(location[1:], 0)
        memory[num + M0] = value
        uninitialisedMem[num] = True
    elif location[0].isnumeric():
        num = int(location, 0)
        memory[num] = value
        uninitialisedMem[num] = True
    elif location == "PC":
        num = int(value)
        PC = num
        branch = True
    elif location == "SP":
        num = int(value)
        SP = num
    else:
        raise Exception("FATAL - Invalid write location: " + location)


