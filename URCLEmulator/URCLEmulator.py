
def emulate(raw: str) -> str:
    
    # pre-process
    # 1 remove spaces
    # 2 remove line comments
    
    # headers
    # 1 find word length header, else assume 8 bits
    # 2 find MINREG, else calculate it
    # 3 find MINRAM, MINSTACK delete it
    # 4 find IMPORT, return error
    
    # setup
    # 1 make global list for registers + ram + SP
    # 2 resolve define macros
    # 3 replace relatives with literals
    # 4 replace labels with literals
    # 5 put code in ram, then set M0 offset
    # 6 PC = 0, R0 = 0, branch = False, ect.
    
    # main
    # 1 .startswith() to find instruction
    # 2 ops() to get list of ops
    # 3 opsType() to get types
    # 4 check types are valid and check number of ops
    # 5 check if fetched operands are uninitialised -> append warning
    # 6 check if write location is not valid -> return error or append warning
    # 6 fetch values from reg/ram
    # 7 do operation
    # 8 truncate result
    # 9 write result
    # 10 R0 = 0
    # 11 if not branch -> PC += 1
    
    # pre-process
    # 1 remove spaces
    global code
    code = raw[5:]
    code = code.replace(" ", "")
    code = code.split("\n")
    
    # 2 remove line comments
    code = [code[i][: code[i].find("//")] if code[i].find("//") != -1 else code[i] for i in range(len(code))]
    
    # headers
    # 1 find word length header, else assume 8 bits
    BITS = findBITSHeader()

    # 2 find MINREG, else calculate it
    MINREG = findMINREGHeader()
    
    # 3 find MINRAM, MINSTACK delete it
    MINRAM = findMINRAMMINSTACKRUNHeaders()
    
    # 4 find IMPORT, return error
    findIMPORTHeader()
    
    # setup
    # 1 make global list for registers + ram + SP
    registers = [2 ** BITS - 1 for i in range(MINREG + 1)]
    uninitialisedReg = [False for i in range(MINREG + 1)]
    registers[0] = 0
    uninitialisedReg[0] = True
    memory = [2 ** BITS - 1 for i in range(MINRAM)]
    global SP; SP = 2 ** BITS
    
    # 2 resolve define macros
    
    
    return "\n".join(code)

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

def findMINRAMMINSTACKRUNHeaders() -> tuple:
    MINRAM = 2 ** BITS
    if MINRAM > 2 ** 16:
        MINRAM = 2 ** 16
    
    for i in range(len(code)):
        if code[i].startswith(("MINRAM", "RUNRAM")):
            code.pop(i)
        elif code[i] == "RUNROM":
            raise Exception("FATAL - RUN ROM is not supported on this emulator")
    
    return MINRAM

def findIMPORTHeader() -> None:
    for i in code:
        if i.startswith("IMPORT"):
            raise Exception("FATAL - Libraries are not supported on this emulator")