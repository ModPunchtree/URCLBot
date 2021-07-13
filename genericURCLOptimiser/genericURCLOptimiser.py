
from genericURCLOptimiser.constants import alpha

##################################################################################

# clean code
    # 1 cut off $optimise
    # 2 delete line comments
    # 3 delete empty lines
    # 4 relatives to labels
    # 5 convert BZR/BZN to BRZ/BNZ

# label/branching optimisations
    # 1 delete duplicate labels
    # 2 shortcut branches
    # 3 delete useless branches

# constant folding

# single instruction optimisations
    # 1  ADD   -> LSH, MOV, INC, DEC, NOP
    # 2  RSH   -> MOV, NOP
    # 3  LOD   -> NOP
    # 4  STR   -> 
    # 5  JMP   -> 
    # 6  BGE   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 7  NOR   -> NOT, MOV, NOP
    # 8  SUB   -> MOV, NEG, DEC, INC, NOP
    # 9  MOV   -> IMM, NOP
    # 10 LSH   -> NOP
    # 11 DEC   -> NOP
    # 12 NEG   -> NOP
    # 13 AND   -> MOV, NOP
    # 14 OR    -> MOV, NOP
    # 15 NOT   -> MOV
    # 16 XNOR  -> XOR, NOT, MOV, NOP
    # 17 XOR   -> MOV, NOT, NOP
    # 18 NAND  -> NOT, MOV, NOP
    # 19 BRL   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 20 BRG   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 21 BRE   -> JMP, BRZ, NOP
    # 22 BNE   -> JMP, BNZ, NOP
    # 23 BOD   -> JMP, NOP
    # 24 BEV   -> JMP, NOP
    # 25 BLE   -> JMP, BRZ, BNZ, NOP
    # 26 BRZ   -> JMP, NOP
    # 27 BNZ   -> JMP, NOP
    # 28 BRN   -> JMP, NOP
    # 29 BRP   -> JMP, NOP
    # 30 PSH   -> 
    # 31 POP   -> INC
    # 32 CAL   -> 
    # 33 RET   -> 
    # 34 HLT   -> 
    # 35 MLT   -> LSH, BSL, MOV, NOP
    # 36 DIV   -> RSH, BSR, MOV, NOP
    # 37 MOD   -> AND, MOV, NOP
    # 38 BSR   -> RSH, MOV, NOP
    # 39 BSL   -> LSH, MOV, NOP
    # 40 SRS   -> MOV, NOP
    # 41 BSS   -> SRS, BSR, MOV, NOP
    # 42 SETE  -> MOV, NOP
    # 43 SETNE -> MOV, NOP
    # 44 SETG  -> MOV, NOP
    # 45 SETL  -> MOV, NOP
    # 46 SETGE -> MOV, NOP
    # 47 SETLE -> MOV, NOP
    # 48 INC   -> MOV, NOP
    # 49 NOP   -> 
    # 50 IMM   -> NOP

# miscellaneous optimisations
    # SETBNZ
    # LODSTR
    # STRLOD
    # PSHPOP
    # POPPSH

# pre-execution optimisation
# list of lists?

##################################################################################

def genericURCLoptimiser(raw: str, BITS: int) -> list:
    
    # clean code
    # 1 cut off $optimise
    if type(raw) == str:
        if raw.startswith("$optimise") or raw.startswith("$optimize"):
            code = raw[raw.index("\n"): ]
        else:
            code = raw
        code = code.split("\n")
    elif raw[0] == "$optimise":
        code = raw[1: ]
    else:
        code = raw
    
    # 2 delete line comments
    code = [i[: i.index("//")] if i.find("//") != -1 else i for i in code]
    
    # 3 delete empty lines
    code = list(filter(None, code))
    
    # delete headers
    code = deleteHeaders(code)
    
    # 4 relatives to labels
    global uniqueNum; uniqueNum = 0
    code = relativesToLabels(code)
    
    # 5 convert BZR/BZN to BRZ/BNZ
    code = ["BRZ" + i[3:] if i.startswith("BZR")
            else "BNZ" + i[3: ] if i.startswith("BZN")
            else i for i in code]

    # optimisation loop
    while True:
        oldCode = [i for i in code]
        returnedCode = optimise(code, BITS)
        if oldCode == returnedCode:
            return code
        code = returnedCode

def optimise(code: list, BITS: int) -> list:
    # label/branching optimisations
    # 1 delete duplicate labels
    code = deleteDuplicateLabels(code)
    
    # 2 shortcut branches
    oldCode = [i for i in code]
    returnedCode = shortcutBranches(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
        
    # 3 delete useless branches
    oldCode = [i for i in code]
    returnedCode = deleteUselessBranches(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # 4 delete useless labels
    oldCode = [i for i in code]
    returnedCode = deleteUselessLabels(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # constant folding
    oldCode = [i for i in code]
    returnedCode = constantFolding(code, BITS)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # single instruction optimisations
    oldCode = [i for i in code]
    returnedCode = singleInstructionOptimisations(code, BITS)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
        
    # miscellaneous optimisations
    oldCode = [i for i in code]
    returnedCode = miscellaneousOptimisations(code, BITS)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # unreachable code optimisation
    oldCode = [i for i in code]
    returnedCode = unreachableCode(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # optimise write before read
    oldCode = [i for i in code]
    returnedCode = optimiseWriteBeforeRead(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # optimise imm then read
    oldCode = [i for i in code]
    returnedCode = optimiseIMM(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # optimise PSHIMM then POP
    oldCode = [i for i in code]
    returnedCode = PSHIMMthenPOP(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # optimise unique jumps
    oldCode = [i for i in code]
    returnedCode = optimiseUniqueJMP(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode

    # optimise unique calls
    oldCode = [i for i in code]
    returnedCode = optimiseUniqueCAL(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode

    # optimise JMP to conditional branch
    oldCode = [i for i in code]
    returnedCode = optimiseJMPBranch(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode

    # SETBranch
    oldCode = [i for i in code]
    returnedCode = SETBRZOrBNZ(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode

    return code

def optimiseJMPBranch(code: list) -> list:
    for i, j in enumerate(code[: -1]):
        if j.startswith("JMP"):
            label = j[4:]
            found = False
            for k, l in enumerate(code):
                if l == label:
                    found = True
                elif found:
                    label2 = l[l.find(" ") + 1: ][: l[l.find(" ") + 1: ].find(",")]
                    if label2 == code[i + 1]:
                        opCode = l[: l.find(" ")]
                        newOpCode = opposite(opCode)
                        newLabel = ".shortcut" + uniqueNumber()
                        code[i] = newOpCode + " " + newLabel + l[l.find(","): ]
                        code.insert(k + 1, newLabel)
                        return code
                    break
    return code

def opposite(opCode):
    if opCode == "BGE":
        return "BRL"
    elif opCode == "BLE":
        return "BRG"
    elif opCode == "BRG":
        return "BLE"
    elif opCode == "BRL":
        return "BGE"
    elif opCode == "BRE":
        return "BNE"
    elif opCode == "BNE":
        return "BRE"
    elif opCode == "BOD":
        return "BEV"
    elif opCode == "BEV":
        return "BOD"
    elif opCode == "BRP":
        return "BRN"
    elif opCode == "BRN":
        return "BRP"
    elif opCode == "BRC":
        return "BNC"
    elif opCode == "BNC":
        return "BRC"
    else:
        raise Exception("FATAL - Unrecognised branch: " + opCode)

def optimiseUniqueCAL(code: list) -> list:
    for i, j in enumerate(code):
        if j.startswith("CAL"):
            label = j[4:]
            count = 0
            for k in code:
                if k.find(label) != -1:
                    if k.startswith("."):
                        pass
                    elif not(k[k.find(label) + len(label): k.find(label) + len(label) + 1]):
                        count += 1
                    elif k[k.find(label) + len(label)] not in alpha:
                        count += 1
            if count < 2:
                uniqueLabel = ".return" + uniqueNumber()
                code.insert(i + 1, uniqueLabel)
                address = code.index(label)
                endAddress = len(code) - 1
                for k, l in enumerate(code[address: ]):
                    if l.startswith(("JMP", "RET", "HLT")):
                        endAddress = address + k
                        break
                if not((i >= address) and (i <= endAddress)):
                    temp = [k for k in code[address: endAddress + 1]]
                    del code[address: endAddress + 1]
                    for k, l in enumerate(temp):
                        if l == "RET":
                            temp[k] = "JMP " + uniqueLabel
                    code = code[: i] + ["DEC SP, SP"] + temp + [code[i + 1]] + ["INC SP, SP"] + code[i + 2: ]
                    return optimiseUniqueCAL(code)
    return code

def optimiseUniqueJMP(code: list) -> list:
    for i, j in enumerate(code):
        if j.startswith("JMP"):
            label = j[4:]
            count = 0
            for k in code:
                if k.find(label) != -1:
                    if k.startswith("."):
                        pass
                    elif not(k[k.find(label) + len(label): k.find(label) + len(label) + 1]):
                        count += 1
                    elif k[k.find(label) + len(label)] not in alpha():
                        count += 1
            if count < 2:
                address = code.index(label)
                endAddress = len(code) - 1
                for k, l in enumerate(code[address: ]):
                    if l.startswith(("JMP", "RET", "HLT")):
                        endAddress = address + k
                        break
                if not((i >= address) and (i <= endAddress)):
                    temp = [k for k in code[address: endAddress + 1]]
                    del code[address: endAddress + 1]
                    code = code[: i] + temp + code[i + 1:]
                    return optimiseUniqueJMP(code)
    return code

def relativesToLabels(code: list) -> list:
    for i, j in enumerate(code):
        if j.find("+") != -1:
            num = readNum(j[j.find("+") + 1: ])
            label = ".relativeLabel" + uniqueNumber()
            code[i] = code[i].replace("+" + str(num), label)
            temp = i
            while num > 0:
                if not code[temp].startswith("."):
                    num -= 1
                temp += 1
            code.insert(temp, label)
            return relativesToLabels(code)
        elif j.find("-") != -1:
            num = readNum(j[j.find("-") + 1: ])
            label = ".relativeLabel" + uniqueNumber()
            code[i] = code[i].replace("-" + str(num), label)
            temp = i
            while num > 0:
                if not code[temp].startswith("."):
                    num -= 1
                temp -= 1
            code.insert(temp, label)
            return relativesToLabels(code)
    return code

def readNum(text: str) -> int:
    temp = ""
    for i in text:
        if (i.isnumeric()) or (i == "x"):
            temp += i
        else:
            return int(temp, 0)
    return int(temp, 0)
    
def uniqueNumber() -> str:
    global uniqueNum
    uniqueNum += 1
    return str(uniqueNum)

def deleteDuplicateLabels(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            return code
        if j.startswith(".") and code[i + 1].startswith("."):
            code.pop(i)
            for k, l in enumerate(code):
                if not l.startswith("."):
                    while findInStr(l, j) != -1:
                        l = l[: findInStr(l, j)] + code[i] + l[findInStr(l, j) + len(j): ]
                code[k] = l
            return deleteDuplicateLabels(code)

def findInStr(string: str, subString: str) -> int:
    if string.find(subString) != -1:
        index = string.find(subString)
        nextIndex = index + len(subString)
        if nextIndex >= len(string):
            return index
        elif string[nextIndex] == ",":
            return index
        else:
            temp = findInStr(string.replace(subString, "^"*len(subString), 1), subString)
            return temp
    return -1

def shortcutBranches(code: list) -> list:
    for i, j in enumerate(code):
        if j.startswith(("JMP", "BGE", "BLE", "BRG", "BRL", "BRZ", "BNZ", "BOD", "BEV", "BRP", "BRN")):
            if j.startswith("JMP"):
                label = j[4: ]
                rest = ""
            else:
                label = j[4: j.find(",")]
                rest = j[j.find(","): ]
            location = code[code.index(label) + 1]
            if location.startswith("JMP"):
                label2 = location[4: ]
                code[i] = j[:4] + label2 + rest
                return shortcutBranches(code)
    return code

def deleteUselessBranches(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            return code
        if j.startswith(("JMP", "BGE", "BLE", "BRG", "BRL", "BRZ", "BNZ", "BOD", "BEV", "BRP", "BRN")):
            label = ""
            if j.startswith("JMP"):
                label = j[4: ]
            if label:
                if code[i + 1] == label:
                    code.pop(i)
                    return deleteUselessBranches(code)

def deleteUselessLabels(code: list) -> list:
    for i, j in enumerate(code):
        if j.startswith("."):
            useful = False
            for k in code:
                if k.find(j) != -1 and not k.startswith("."):
                    useful = True
            if not useful:
                code.pop(i)
                return deleteUselessLabels(code)
    return code

def singleInstructionOptimisations(code: list, BITS: int) -> list:
    for i, j in enumerate(code):
        op = readOperation(j)
        ops = readOps(j[len(op) + 1: ])
        
        # 1  ADD   -> LSH, MOV, INC, DEC, NOP
        if op == "ADD":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "DEC " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "DEC " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "INC " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == "1":
                code[i] = "INC " + ops[0] + ", " + ops[2]
                return code
            elif (ops[2] == "0") or (ops[2] == "R0"):
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif (ops[1] == "0") or (ops[1] == "R0"):
                code[i] = "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[1] == ops[2]:
                code[i] = "LSH " + ops[0] + ", " + ops[1]
                return code
            
        # 2  RSH   -> MOV, NOP
        elif op == "RSH":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif (ops[1] == "R0") or (ops[1] == "0") or (ops[1] == "1"):
                code[i] = "MOV " + ops[0] + ", 0"
                return code
        
        # 3  LOD   -> NOP
        elif op == "LOD":
            if ops[0] == "R0":
                code.pop(i)
                return code
        
        # 4  STR   -> 
        elif op == "STR":
            pass
        
        # 5  JMP   -> 
        elif op == "JMP":
            pass
        
        # 6  BGE   -> JMP, BRZ, BNZ, BRN, BRP, NOP
        elif op == "BGE":
            if ops[1] == ops[2]:
                code[i] = "JMP " + ops[0]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "JMP " + ops[0]
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BRZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "BNZ " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** (BITS - 1)):
                code[i] = "BRN " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** (BITS - 1)):
                code[i] = "BRP " + ops[0] + ", " + ops[2]
                return code
        
        # 7  NOR   -> NOT, MOV, NOP
        elif op == "NOR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif (ops[2] == "0") or (ops[2] == "R0"):
                code[i] = "NOT " + ops[0] + ", " + ops[1]
                return code
            elif (ops[1] == "0") or (ops[1] == "R0"):
                code[i] = "NOT " + ops[0] + ", " + ops[2]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 0"
                return code

        # 8  SUB   -> MOV, NEG, DEC, INC, NOP
        elif op == "SUB":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[2] == "1":
                code[i] = "DEC " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "INC " + ops[0] + ", " + ops[1]
                return code
            elif (ops[1] == "0") or (ops[1] == "R0"):
                code[i] = "NEG " + ops[0] + ", " + ops[1]
                return code
            elif (ops[2] == "0") or (ops[2] == "R0"):
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code

        # 9  MOV   -> IMM, NOP
        elif op == "MOV":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1][0].isnumeric():
                code[i] = "IMM " + ops[0] + ", " + ops[1]
                return code
            elif ops[0] == ops[1]:
                code.pop(i)
                return code

        # 10 LSH   -> NOP
        elif op == "LSH":
            if ops[0] == "R0":
                code.pop(i)
                return code

        # 11 DEC   -> NOP
        elif op == "DEC":
            if ops[0] == "R0":
                code.pop(i)
                return code
            
        # 12 NEG   -> NOP
        elif op == "NEG":
            if ops[0] == "R0":
                code.pop(i)
                return code
        
        # 13 AND   -> MOV, NOP
        elif op == "AND":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif (ops[1] == "0") or (ops[1] == "R0") or (ops[2] == "0") or (ops[2] == "R0"):
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif (ops[1] == str(2 ** BITS - 1)) or (ops[1] == ops[2]):
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "MOV " + ops[0] + ", " + ops[2]
                return code
            
        # 14 OR    -> MOV, NOP
        elif op == "OR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", " + ops[2]
                return code
    
        # 15 NOT   -> MOV
        elif op == "NOT":
            if ops[0] == "R0":
                code.pop(i)
                return code      
            
        # 16 XNOR  -> XOR, NOT, MOV, NOP
        elif op == "XNOR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] == "NOT " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] == "NOT " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] == "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            
        # 17 XOR   -> MOV, NOT, NOP
        elif op == "XOR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] == "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] == "NOT " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] == "NOT " + ops[0] + ", " + ops[1]
                return code
            
        # 18 NAND  -> NOT, MOV, NOP
        elif op == "NAND":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0" or ops[2] == "0" or ops[2] == "R0":
                code[i] = "IMM " + ops[0] + ", " + str(2 ** BITS - 1)
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "NOT " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "NOT " + ops[0] + ", " + ops[2]
                return code
        
        # 19 BRL   -> JMP, BRZ, BNZ, BRN, BRP, NOP
        elif op == "BRL":
            if ops[1] == ops[2]:
                code.pop(i)
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BNZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "BRZ " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == str(2 ** (BITS - 1)):
                code[i] = "BRP " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** (BITS - 1) - 1):
                code[i] = "BRN " + ops[0] + ", " + ops[2]
                return code
        
        # 20 BRG   -> JMP, BRZ, BNZ, BRN, BRP, NOP
        elif op == "BRG":
            if ops[1] == ops[2]:
                code.pop(i)
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "BNZ " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "1":
                code[i] = "BRZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** (BITS - 1) - 1):
                code[i] = "BRN " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == str(2 ** (BITS - 1)):
                code[i] = "BRP " + ops[0] + ", " + ops[2]
                return code
        
        # 21 BRE   -> JMP, BRZ, NOP
        elif op == "BRE":
            if ops[1] == ops[2]:
                code[i] = "JMP " + ops[0]
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BRZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "BRZ " + ops[0] + ", " + ops[1]
                return code
        
        # 22 BNE   -> JMP, BNZ, NOP
        elif op == "BNE":
            if ops[1] == ops[2]:
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "BNZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "BNZ " + ops[0] + ", " + ops[1]
                return code
        
        # 23 BOD   -> JMP, NOP
        elif op == "BOD":
            if ops[0] == "R0":
                code.pop(i)
                return code
        
        # 24 BEV   -> JMP, NOP
        elif op == "BEV":
            if ops[0] == "R0":
                code[i] = "JMP " + ops[0]
                return code
        
        # 25 BLE   -> JMP, BRZ, BNZ, NOP
        elif op == "BLE":
            if ops[1] == ops[2]:
                code[i] = "JMP " + ops[0]
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "JMP " + ops[0]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "BRZ " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == "1":
                code[i] = "BNZ " + ops[0] + ", " + ops[2]
                return code
            elif ops[1] == str(2 ** (BITS - 1)):
                code[i] = "BRN " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** (BITS - 1) - 1):
                code[i] = "BRP " + ops[0] + ", " + ops[1]
                return code
        
        # 26 BRZ   -> JMP, NOP
        elif op == "BRZ":
            if ops[0] == "R0":
                code[i] = "JMP " + ops[0]
                return code
        
        # 27 BNZ   -> JMP, NOP
        elif op == "BNZ":
            if ops[0] == "R0":
                code.pop(i)
                return code
        
        # 28 BRN   -> JMP, NOP
        elif op == "BRN":
            if ops[0] == "R0":
                code.pop(i)
                return code
            
        # 29 BRP   -> JMP, NOP
        elif op == "BRP":
            if ops[0] == "R0":
                code[i] = "JMP " + ops[0]
                return code
        
        # 30 PSH   -> 
        elif op == "PSH":
            pass
        
        # 31 POP   -> INC
        elif op == "POP":
            if ops[0] == "R0":
                code[i] = "INC SP, SP"
                return code
        
        # 32 CAL   -> 
        elif op == "CAL":
            pass
        
        # 33 RET   -> 
        elif op == "RET":
            pass
        
        # 34 HLT   -> 
        elif op == "HLT":
            pass
        
        # 35 MLT   -> LSH, BSL, MOV, NOP
        elif op == "MLT":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0" or ops[2] == "0" or ops[2] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1] == "1":
                code[i] = "MOV " + ops[0] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[1] == "3":
                code[i] = "LSH " + ops[0] + ", " + ops[2]
                code.insert(i + 1, "ADD " + ops[0] + ", " + ops[0] + ", " + ops[2])
                return code
            elif ops[2] == "3":
                code[i] = "LSH " + ops[0] + ", " + ops[1]
                code.insert(i + 1, "ADD " + ops[0] + ", " + ops[0] + ", " + ops[1])
                return code
            elif ops[1] == "5":
                code[i] = "LSH " + ops[0] + ", " + ops[2]
                code.insert(i + 1, "LSH " + ops[0] + ", " + ops[0])
                code.insert(i + 1, "ADD " + ops[0] + ", " + ops[0] + ", " + ops[2])
                return code
            elif ops[2] == "5":
                code[i] = "LSH " + ops[0] + ", " + ops[1]
                code.insert(i + 1, "LSH " + ops[0] + ", " + ops[0])
                code.insert(i + 1, "ADD " + ops[0] + ", " + ops[0] + ", " + ops[1])
                return code
            elif ops[1][0].isnumeric():
                if int(ops[1], 0) in [2 ** i for i in range(BITS)]:
                    shift = str([2 ** i for i in range(BITS)].index(int(ops[1], 0)))
                    code[i] = "BSL " + ops[0] + ", " + ops[2] + ", " + shift
                    return code
            if ops[2][0].isnumeric():
                if int(ops[2], 0) in [2 ** i for i in range(BITS)]:
                    shift = str([2 ** i for i in range(BITS)].index(int(ops[2], 0)))
                    code[i] = "BSL " + ops[0] + ", " + ops[1] + ", " + shift
                    return code
        
        # 36 DIV   -> RSH, BSR, MOV, NOP
        elif op == "DIV":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "SETE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            elif ops[2] == "1":
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            if ops[2][0].isnumeric():
                if int(ops[2], 0) in [2 ** i for i in range(BITS)]:
                    shift = str([2 ** i for i in range(BITS)].index(int(ops[2], 0)))
                    code[i] = "BSR " + ops[0] + ", " + ops[1] + ", " + shift
                    return code
        
        # 37 MOD   -> AND, MOV, NOP
        elif op == "MOD":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == "1":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            if ops[2][0].isnumeric():
                if int(ops[2], 0) in [2 ** i for i in range(BITS)]:
                    code[i] = "AND " + ops[0] + ", " + ops[1] + ", " + str(int(ops[2], 0) - 1)
                    return code
        
        # 38 BSR   -> RSH, MOV, NOP
        elif op == "BSR":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "1":
                code[i] == "RSH " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "2":
                code[i] == "RSH " + ops[0] + ", " + ops[1]
                code[i] == "RSH " + ops[0] + ", " + ops[0]
                return code
            elif ops[2][0].isnumeric():
                if int(ops[2], 0) >= BITS:
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
        
        # 39 BSL   -> LSH, MOV, NOP
        elif op == "BSL":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] == "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "1":
                code[i] == "LSH " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "2":
                code[i] == "LSH " + ops[0] + ", " + ops[1]
                code[i] == "LSH " + ops[0] + ", " + ops[0]
                return code
            elif ops[2][0].isnumeric():
                if int(ops[2], 0) >= BITS:
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
        
        # 40 SRS   -> MOV, NOP
        elif op == "SRS":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            
        # 41 BSS   -> SRS, BSR, MOV, NOP
        elif op == "BSS":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "MOV " + ops[0] + ", " + ops[1]
                return code
            elif ops[2] == "1":
                code[i] = "SRS " + ops[0] + ", " + ops[1]
                return code
            elif ops[1][0].isnumeric():
                if int(ops[1], 0) < 2 ** (BITS - 1):
                    code[i] = "BSR " + ops[0] + ", " + ops[1] + ", " + ops[2]
                    return code

        # 42 SETE  -> MOV, NOP
        elif op == "SETE":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == ops[2]:
                code[i] = "IMM " + ops[0] + ", 1"
                return code
            elif ops[1][0].isnumeric():
                if ops[2] == "R0" and ops[1] != "0":
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
                elif ops[2] == "R0" and ops[1] == "0":
                    code[i] = "IMM " + ops[0] + ", 1"
                    return code
            if ops[2][0].isnumeric():
                if ops[1] == "R0" and ops[2] != "0":
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
                elif ops[1] == "R0" and ops[2] == "0":
                    code[i] = "IMM " + ops[0] + ", 1"
                    return code
                
        # 43 SETNE -> MOV, NOP
        elif op == "SETNE":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == ops[2]:
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1][0].isnumeric():
                if ops[2] == "R0" and ops[1] != "0":
                    code[i] = "IMM " + ops[0] + ", 1"
                    return code
                elif ops[2] == "R0" and ops[1] == "0":
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
            if ops[2][0].isnumeric():
                if ops[1] == "R0" and ops[2] != "0":
                    code[i] = "IMM " + ops[0] + ", 1"
                    return code
                elif ops[1] == "R0" and ops[2] == "0":
                    code[i] = "IMM " + ops[0] + ", 0"
                    return code
        
        # 44 SETG  -> MOV, NOP
        elif op == "SETG":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == ops[2]:
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "SETNE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 0"
                return code
        
        # 45 SETL  -> MOV, NOP
        elif op == "SETL":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == ops[2]:
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 0"
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "SETNE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
        
        # 46 SETGE -> MOV, NOP
        elif op == "SETGE":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 1"
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "SETE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            elif ops[2] == "0" or ops[2] == "R0":
                code[i] = "IMM " + ops[0] + ", 1"
                return code
        
        # 47 SETLE -> MOV, NOP
        elif op == "SETLE":
            if ops[0] == "R0":
                code.pop(i)
                return code
            elif ops[1] == str(2 ** BITS - 1):
                code[i] = "SETE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            elif ops[2] == str(2 ** BITS - 1):
                code[i] = "IMM " + ops[0] + ", 1"
                return code
            elif ops[1] == "0" or ops[1] == "R0":
                code[i] = "SETE " + ops[0] + ", " + ops[1] + ", " + ops[2]
                return code
            
        # 48 INC   -> NOP
        elif op == "INC":
            if ops[0] == "R0":
                code.pop(i)
                return code
        
        # 49 NOP   -> 
        elif op == "NOP":
            code.pop(i)
            return code
        
        # 50 IMM   -> NOP
        elif op == "IMM":
            if ops[0] == "R0":
                code.pop(i)
                return code
        
        # 51 IN    -> 
        elif op == "IN":
            pass
        
        # 52 OUT   -> 
        elif op == "OUT":
            pass
        
        elif op.startswith("."):
            pass
        
        else:
            raise Exception("FATAL - Unrecognised instruction: " + str(code[i]))
    return code

def readOperation(instruction: str) -> str:
    if instruction.find(" ") != -1:
        return instruction[: instruction.index(" ")]
    else:
        return instruction

def readOps(text: str) -> tuple:
    ops = ()
    temp = ""
    for i in text:
        if i == ",":
            ops += (temp,)
            temp = ""
        elif i == " ":
            pass
        else:
            temp += i
    if temp:
        ops += (temp,)
    return ops

def constantFolding(code: list, BITS: int) -> list:
    for i, j in enumerate(code):
        op = readOperation(j)
        ops = readOps(j[len(op): ])
        
        if op in ("ADD", "RSH", "BGE", "NOR", "SUB", "MOV", "LSH", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE", "INC"):
            if op == "ADD":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) + int(ops[2], 0))
                    return code
            elif op == "RSH":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) // 2)
                    return code
            elif op == "BGE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) >= int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "NOR":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS - 1) - (int(ops[1], 0) | int(ops[2], 0)))
                    return code
            elif op == "SUB":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) >= int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) - int(ops[2], 0))
                    else:
                        code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) - int(ops[2], 0) + (2 ** BITS))
                    return code
            elif op == "MOV":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + ops[1]
                    return code
            elif op == "LSH":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) * 2)
                    return code
            elif op == "DEC":
                if ops[1][0].isnumeric():
                    if ops[1] == "0":
                        code[i] = "IMM " + ops[0] + ", " + str(int(2 ** BITS - 1))
                    else:
                        code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) - 1)
                    return code
            elif op == "NEG":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS) - int(ops[1], 0))
                    return code
            elif op == "AND":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) & int(ops[2], 0))
                    return code
            elif op == "OR":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) | int(ops[2], 0))
                    return code
            elif op == "NOT":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS - 1) - int(ops[1], 0))
                    return code
            elif op == "XNOR":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS - 1) - (int(ops[1], 0) ^ int(ops[2], 0)))
                    return code
            elif op == "XOR":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) ^ int(ops[2], 0))
                    return code
            elif op == "NAND":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str((2 ** BITS - 1) - (int(ops[1], 0) & int(ops[2], 0)))
                    return code
            elif op == "BRL":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) < int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRG":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) > int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) == int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BNE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) != int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BOD":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) % 2 == 1:
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BEV":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) % 2 == 0:
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BLE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) <= int(ops[2], 0):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRZ":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) == 0:
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BNZ":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) != 0:
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRN":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) >= (2 ** (BITS - 1)):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "BRP":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) < (2 ** (BITS - 1)):
                        code[i] = "JMP " + ops[0]
                    else:
                        code.pop(i)
                    return code
            elif op == "MLT":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + correctValue(str(int(ops[1], 0) * int(ops[2], 0)), BITS)
                    return code
            elif op == "DIV":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) // int(ops[2], 0))
                    return code
            elif op == "MOD":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) % int(ops[2], 0))
                    return code
            elif op == "BSR":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) // 2 ** int(ops[2], 0))
                    return code
            elif op == "BSL":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + correctValue(str(int(ops[1], 0) * 2 ** int(ops[2], 0)), BITS)
                    return code
            elif op == "SRS":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) >= 2 ** (BITS - 1): 
                        code[i] = "IMM " + ops[0] + ", " + str(int(ops[1], 0) // 2 + 2 ** (BITS - 1))
                    else:
                        code[i] = "IMM " + ops[0] + ", " + correctValue(str(int(ops[1], 0) // 2), BITS)
                    return code
            elif op == "BSS":
                if ops[1][0].isnumeric():
                    if int(ops[1], 0) >= 2 ** (BITS - 1):
                        num = int(ops[1], 0)
                        for i in range(int(ops[2], 0)):
                            num // 2 + 2 ** (BITS - 1)
                        code[i] = "IMM " + ops[0] + ", " + str(num)
                    else:
                        code[i] = "IMM " + ops[0] + ", " + correctValue(str(int(ops[1], 0) // int(ops[2], 0)), BITS)
                    return code
            elif op == "SETE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) == int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETNE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) != int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETG":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) > int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETL":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) > int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETGE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) >= int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "SETLE":
                if ops[1][0].isnumeric() and ops[2][0].isnumeric():
                    if int(ops[1], 0) <= int(ops[2], 0):
                        code[i] = "IMM " + ops[0] + ", 1"
                    else:
                        code[i] = "IMM " + ops[0] + ", 0"
                    return code
            elif op == "INC":
                if ops[1][0].isnumeric():
                    code[i] = "IMM " + ops[0] + ", " + correctValue(str(int(ops[1], 0) + 1), BITS)
                    return code
            elif op == "NOP":
                code.pop(i)
                return code
            elif op == "IMM":
                pass
    return code

def correctValue(value: str, BITS: int) -> str:
    num = int(value, 0)
    if num >= (2 ** BITS):
        num %= 2 ** BITS
    while num < 0:
        num += 2 ** BITS
    return str(num)

def miscellaneousOptimisations(code: list, BITS: int) -> list:
    
    # SETBNZ
    oldCode = [i for i in code]
    returnedCode = SETBRZ(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
        
    # LODSTR
    oldCode = [i for i in code]
    returnedCode = LODSTR(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # STRLOD
    oldCode = [i for i in code]
    returnedCode = STRLOD(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
        
    # PSHPOP
    oldCode = [i for i in code]
    returnedCode = PSHPOP(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # POPPSH
    oldCode = [i for i in code]
    returnedCode = POPPSH(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode
    
    # INCDEC
    oldCode = [i for i in code]
    returnedCode = INCDEC(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode

    # DECINC
    oldCode = [i for i in code]
    returnedCode = DECINC(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode

    # STRPOP
    oldCode = [i for i in code]
    returnedCode = STRPOP(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode

    # repeated add and sub
    oldCode = [i for i in code]
    returnedCode = repeatedADDSUB(code)
    if oldCode != returnedCode:
        return returnedCode
    else:
        code = returnedCode

    return code

def SETBRZOrBNZ(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("SET"):
            firstOp = j[j.index(" ") + 1: ]
            firstOp = firstOp[: firstOp.index(",")]
            if j.startswith("SETL"):
                if code[i + 1].startswith("BRZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BGE " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
                if code[i + 1].startswith("BNZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BRL " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
            elif j.startswith("SETLE"):
                if code[i + 1].startswith("BRZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BRG " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
                if code[i + 1].startswith("BNZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BLE " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
            elif j.startswith("SETG"):
                if code[i + 1].startswith("BRZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BLE " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
                if code[i + 1].startswith("BNZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BRG " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
            elif j.startswith("SETGE"):
                if code[i + 1].startswith("BRZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BRL " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
                if code[i + 1].startswith("BNZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BGE " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
            elif j.startswith("SETE"):
                if code[i + 1].startswith("BRZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BNE " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
                if code[i + 1].startswith("BNZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BRE " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
            elif j.startswith("SETNE"):
                if code[i + 1].startswith("BRZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BRE " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
                if code[i + 1].startswith("BNZ"):
                    label = code[i + 1][4: code[i + 1].index(",")]
                    if label.startswith((".if", ".else", ".while")):
                        code[i] = "BNE " + label + j[j.index(","): ]
                        code.pop(i + 1)
                        return SETBRZOrBNZ(code)
            else:
                raise Exception()
            
    return code

def repeatedADDSUB(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith(("DEC", "SUB", "ADD", "INC")):
            change = 0
            ops = getOps(j)
            original = ops[0]
            bad = []
            if ops[0] == ops[1]:
                for k, l in enumerate(code[i:]):
                    if l.startswith(("JMP", "HLT", "RET", ".")):
                        break                   
                    if l.startswith("DEC"):
                        ops = getOps(l)
                        if ops[0] == ops[1] and ops[0] == original:
                            bad.append(k + i)
                            change -= 1
                    elif l.startswith("INC"):
                        ops = getOps(l)
                        if ops[0] == ops[1] and ops[0] == original:
                            bad.append(k + i)
                            change += 1
                    elif l.startswith("ADD"):
                        ops = getOps(l)
                        if ops[2][0].isnumeric():
                            if ops[0] == ops[1] and ops[0] == original:
                                bad.append(k + i)
                                change += int(ops[2], 0)
                        else:
                            if original in ops:
                                break
                    elif l.startswith("SUB"):
                        ops = getOps(l)
                        if ops[2][0].isnumeric():
                            if ops[0] == ops[1] and ops[0] == original:
                                bad.append(k + i)
                                change -= int(ops[2], 0)
                        else:
                            if original in ops:
                                break
                    else:
                        ops = readOps(l[l.find(" ") + 1:])
                        if original in ops:
                            break
                        elif (original == "SP") and ((l.startswith("PSH")) or (l.startswith("POP"))):
                            break
                if len(bad) > 1:
                    if change == 0:
                        for k in bad[:: -1]:
                            code.pop(k)
                        return repeatedADDSUB(code)
                    elif change > 0:
                        for k in bad[1:][:: -1]:
                            code.pop(k)
                        code[bad[0]] = "ADD " + original + ", " + original + ", " + str(change)
                        return repeatedADDSUB(code)
                    elif change < 0:
                        for k in bad[1:][:: -1]:
                            code.pop(k)
                        code[bad[0]] = "SUB " + original + ", " + original + ", " + str(change * -1)
                        return repeatedADDSUB(code)
    return code

def getOps(j):
    if j.startswith(("DEC", "INC")):
        return (j[4: j.find(",")], j[j.find(",") + 2: ])
    else:
        return (j[4: j.find(",")], j[j.find(",") + 2: ][: j[j.find(",") + 2: ].find(",")], j[j.find(",") + 2: ][j[j.find(",") + 2: ].find(",") + 2: ])

def STRPOP(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("STR SP, ") and code[i + 1].startswith("POP"):
            code[i] = "MOV " + code[i + 1][4: ] + ", " + j[j.find(",") + 2: ]
            code[i + 1] = "INC SP, SP"
            return STRPOP(code)
    return code

def DECINC(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("DEC"):
            target = j[4: j.find(",")]
            fetch = j[j.find(",") + 2: ]
            if code[i + 1].startswith("INC"):
                target2 = code[i + 1][4: code[i + 1].find(",")]
                fetch2 = code[i + 1][code[i + 1].find(",") + 2: ]
                if target2 == fetch2 and target == target2:
                    code[i] = "MOV " + target + ", " + fetch
                    code.pop(i + 1)
                    return DECINC(code)
    return code

def INCDEC(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("INC"):
            target = j[4: j.find(",")]
            fetch = j[j.find(",") + 1: ]
            if code[i + 1].startswith("DEC"):
                target2 = code[i + 1][4: code[i + 1].find(",")]
                fetch2 = code[i + 1][code[i + 1].find(",") + 1: ]
                if target2 == fetch2 and target == target2:
                    code[i] = "MOV " + target + ", " + fetch
                    code.pop(i + 1)
                    return INCDEC(code)
    return code

def SETBRZ(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("SET") and code[i + 1].startswith("BRZ") and code[i + 1][code[i + 1].find(",") + 2: ] == j[j.find(" ") + 1: j.find(",")]:
            if j[3: 5] == "GE":
                code[i + 1] = "BRL " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
                code.pop(i)
                return SETBRZ(code)
            elif j[3: 5] == "LE":
                code[i + 1] = "BRG " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
                code.pop(i)
                return SETBRZ(code)
            elif j[3] == "G":
                code[i + 1] = "BLE " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
                code.pop(i)
                return SETBRZ(code)
            elif j[3] == "L":
                code[i + 1] = "BGE " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
                code.pop(i)
                return SETBRZ(code)
    return code

def LODSTR(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("LOD") and code[i + 1].startswith("STR") and j[j.find(" ") + 1: j.find(",")] == code[i + 1][code[i + 1].index(",") + 2: ] and j[j.find(",") + 2: ] == code[i + 1][code[i + 1].find(" ") + 1: code[i + 1].find(",")]:
            code.pop(i + 1)
            return LODSTR(code)
    return code

def STRLOD(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("STR") and code[i + 1].startswith("LOD") and j[j.find(" ") + 1: j.find(",")] == code[i + 1][code[i + 1].find(",") + 2: ]:
            code[i + 1] = "MOV " + code[i + 1][4: code[i + 1].index(",")] + j[j.index(","): ]
            return STRLOD(code)
    return code

def PSHPOP(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("PSH") and code[i + 1].startswith("POP"):
            code[i + 1] = "MOV " + code[i + 1][code[i + 1].index(" ") + 1: ] + ", " + j[j.index(" ") + 1: ]
            code.pop(i)
            return PSHPOP(code)
    return code

def POPPSH(code: list) -> list:
    for i, j in enumerate(code):
        if i == len(code) - 1:
            break
        if j.startswith("POP") and code[i + 1].startswith("PSH"):
            code[i] = "LOD " + j[j.index(" ") + 1: ] + ", SP"
            code[i + 1] = "STR SP, " + code[i + 1][code[i + 1].index(" ") + 1: ]
            return POPPSH(code)
    return code

def unreachableCode(code: list) -> list:
    for i, j in enumerate(code[:-1]):
        if j.startswith("JMP") or j.startswith("HLT") or j.startswith("RET"):
            if not code[i + 1].startswith("."):
                code.pop(i + 1)
                return unreachableCode(code)
    return code

def optimiseWriteBeforeRead(code: list) -> list:
    # find code that writes to reg
    # check next instructions if not label or branch
    # if reg is read or untouched leave it
    # else if reg is overwritten delete original instruction
    
    for i, j in enumerate(code[:-1]):
        if not j.startswith(".") and not j.startswith(("STR", "JMP", "BGE", "NOP", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "OUT", "PSH", "CAL", "RET", "HLT")):
            op = readOperation(j)
            ops = readOps(j[len(op) + 1: ])
            nextInstructions = []
            for k in code[i + 1:]:
                if k.startswith(".") or k.startswith(("JMP", "BGE", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "CAL", "RET", "HLT")):
                    break
                nextInstructions.append(k)
            useful = False
            overwritten = False
            if ops.count(ops[0]) > 1:
                useful = True
            for k in nextInstructions:
                op2 = readOperation(k)
                ops2 = readOps(k[len(op2) + 1: ])
                # read ops
                if op2 not in ("NOP", "IMM", "POP", "RET", "HLT"):
                    if len(ops2) == 1:
                        if ops2[0] == ops[0]:
                            useful = True
                    elif len(ops2) == 2:
                        if ops2[1] == ops[0]:
                            useful = True
                    elif len(ops2) == 3:
                        if ops2[1] == ops[0]:
                            useful = True
                        elif ops2[2] == ops[0]:
                            useful = True
                # write ops
                if op2 not in ("JMP", "BGE", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "CAL", "RET", "HLT"):
                    if ops2[0] == ops[0]:
                        overwritten = True
                if not useful and overwritten:
                    code.pop(i)
                    return optimiseWriteBeforeRead(code)
            if not useful and overwritten:
                code.pop(i)
                return optimiseWriteBeforeRead(code)
    return code

def findMINREG(code: list) -> int:
    MINREG = 0
    for i, j in enumerate(code):
        while j.find("R") != -1:
            if j[j.find("R") + 1: j.find("R") + 2]:
                if j[j.find("R") + 1].isnumeric():
                    temp = readNum(j[j.find("R") + 1: ])
                    if temp > MINREG:
                        MINREG = temp
            code[i] = j.replace("R", "#", 1)
    return MINREG

def deleteHeaders(code: list) -> list:
    for i, j in enumerate(code):
        if j.startswith(("BITS", "MINREG", "MINRAM", "MINSTACK", "RUN")):
            code.pop(i)
            return deleteHeaders(code)
    return code

def optimiseIMM(code: list) -> list:
    for i, j in enumerate(code):
        if not j.startswith("."):
            op = readOperation(j)
            ops = readOps(j[len(op) + 1: ])
            if op not in ("NOP", "IMM", "POP", "RET", "HLT"):
                if len(ops) == 1:
                    if ops[0][0] == "R":
                        value = fetchValue(code, i, ops[0])
                        if value:
                            code[i] = code[i][: code[i].index(" ") + 1] + value + code[i][code[i].index(" ") + 1 + len(ops[0]): ]
                            return code
                if len(ops) == 2:
                    if ops[1][0] == "R":
                        value = fetchValue(code, i, ops[1])
                        if value:
                            code[i] = code[i][: code[i].index(",") + 2] + value + code[i][code[i].index(",") + 2 + len(ops[1]): ]
                            #code[i] = j.replace(ops[1], value)
                            return code
                if len(ops) == 3:
                    if ops[1][0] == "R":
                        value = fetchValue(code, i, ops[1])
                        if value:
                            code[i] = code[i][: code[i].index(",") + 2] + value + code[i][code[i].index(",") + 2 + len(ops[1]): ]
                            return code
                    if ops[2][0] == "R":
                        value = fetchValue(code, i, ops[2])
                        if value:
                            code[i] = code[i][: len(code[i]) - 1 - code[i][::-1].index(",") + 2] + value + code[i][len(code[i]) - 1 - code[i][::-1].index(",") + 2 + len(ops[2]): ]
                            #code[i] = j.replace(ops[2], value)
                            return code
    return code

def fetchValue(code: list, i: int, target) -> str:
    value = ""
    for k in code[: i][: : -1]:
        if k.startswith("."):
            break
        elif not k.startswith(("STR", "JMP", "BGE", "NOP", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "OUT", "PSH", "CAL", "RET", "HLT")):
            op2 = readOperation(k)
            ops2 = readOps(k[len(op2) + 1: ])
            if ops2[0] == target and op2 != "IMM":
                break
            elif ops2[0] == target and op2 == "IMM":
                value = ops2[1]
    return value

def PSHIMMthenPOP(code: list) -> list:
    for i, j in enumerate(code):
        if j.startswith("POP"):
            if j[j.index(" ") + 1: ][0] == "R":
                num = 0
                for k in code[: i][: : -1]:
                    num -= 1
                    if k.startswith((".", "CAL")) or k.find("SP, SP") != -1:
                        break
                    elif k.startswith("PSH"):
                        if k[k.index(" ") + 1: ][0].isnumeric():
                            code[i] = "IMM " + j[j.index(" ") + 1: ] + ", " + k[k.index(" ") + 1: ]
                            code.pop(i + num)
                            return PSHIMMthenPOP(code)
    return code




