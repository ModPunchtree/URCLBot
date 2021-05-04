
def urcl() -> tuple:
    return ("ADD", "RSH", "LOD", "STR", "JMP", "BGE", "NOR", "SUB", "MOV", "NOP", "IMM", "LSH", "INC", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BZR", "BNZ", "BZN", "BRN", "BRP", "IN", "OUT", "PSH", "POP", "CAL", "RET", "HLT", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE")

def numberOfOps() -> tuple:
    return ( 3,     2,     2,     2,     1,     3,     3,     3,     2,     0,     2,     2,     2,     2,     2,     3,     3,    3,     3,      3,     3,      3,     3,     3,     3,     2,     2,     3,     2,     2,     2,     2,     2,     2,     2,    2,     1,     1,     1,     0,     0,     3,     3,     3,     3,     3,     2,     3,     3,      3,       3,      3,      3,       3)

def validOpTypes() -> tuple:
    one = ("REG", "REG", "REG")
    two = ("REG", "REG", "IMM")
    three = ("REG", "IMM", "IMM")
    four = ("REG", "REG")
    five = ("REG", "IMM")
    six = ("REG", "MEM")
    seven = ("PC", "REG")
    eight = ("MEM", "REG")
    nine = ("MEM", "IMM")
    ten = ("IMM",)
    eleven = ("REG",)
    twelve = ("IMM", "REG", "REG")
    thirteen = ("IMM", "REG", "IMM")
    fourteen = ("IMM", "IMM", "REG")
    seventeen = ("REG", "IMM", "REG")
    eighteen = ("IMM", "REG")
    nineteen = ("REG", "PORT")
    twenty = ("PORT", "REG")
    twentyone = ("PORT", "IMM")
    twentytwo = ("IMM", "IMM")
    twentythree = ()
    
    ADD = (one, two, seventeen, three)
    RSH = (four, five)
    LOD = (six, four, seven, five)
    STR = (eight, four, nine, five, eighteen, twentytwo)
    JMP = (ten, eleven)
    BGE = (twelve, thirteen, fourteen, one, two, seventeen)
    NOR = (one, two, seventeen)
    SUB = (one, two, seventeen, three)
    MOV = (four, five)
    NOP = (twentythree,)
    IMM = (five,)
    LSH = (four, five)
    INC = (four, five)
    DEC = (four, five)
    NEG = (four, five)
    AND = (one, two, seventeen, three)
    OR = (one, two, seventeen, three)
    NOT = (four, five)
    XNOR = (one, two, seventeen, three)
    XOR = (one, two, seventeen, three)
    NAND = (one, two, seventeen, three)
    BRL = (twelve, thirteen, fourteen, one, two, seventeen)
    BRG = (twelve, thirteen, fourteen, one, two, seventeen)
    BRE = (twelve, thirteen, fourteen, one, two, seventeen, three)
    BNE = (twelve, thirteen, fourteen, one, two, seventeen, three)
    BOD = (eighteen, four)
    BEV = (eighteen, four)
    BLE = (twelve, thirteen, fourteen, one, two, seventeen)
    BRZ = (eighteen, four)
    BZR = (eighteen, four)
    BNZ = (eighteen, four)
    BZN = (eighteen, four)
    BRN = (eighteen, four)
    BRP = (eighteen, four)
    IN = (nineteen,)
    OUT = (twenty, twentyone)
    PSH = (eleven, ten)
    POP = (eleven,)
    CAL = (eleven, ten)
    RET = (twentythree,)
    HLT = (twentythree,)
    MLT = (one, two, seventeen)
    DIV = (one, two, seventeen)
    MOD = (one, two, seventeen)
    BSR = (one, two, seventeen)
    BSL = (one, two, seventeen)
    SRS = (four, five)
    BSS = (one, two, seventeen)
    SETE = (one, two, seventeen, three)
    SETNE = (one, two, seventeen, three)
    SETG = (one, two, seventeen)
    SETL = (one, two, seventeen)
    SETGE = (one, two, seventeen)
    SETLE = (one, two, seventeen)

    return (ADD, RSH, LOD, STR, JMP, BGE, NOR, SUB, MOV, NOP, IMM, LSH, INC, DEC, NEG, AND, OR, NOT, XNOR, XOR, NAND, BRL, BRG, BRE, BNE, BOD, BEV, BLE, BRZ, BZR, BNZ, BZN, BRN, BRP, IN, OUT, PSH, POP, CAL, RET, HLT, MLT, DIV, MOD, BSR, BSL, SRS, BSS, SETE, SETNE, SETG, SETL, SETGE, SETLE)

def fetchTwoThree(op: str) -> bool:
    if op in ("ADD", "NOR", "SUB", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "MLT", "DIV", "MOD", "BSR", "BSL", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE"):
        return True
    return False

def fetchOneTwoThree(op: str) -> bool:
    if op in ("BGE", "BRL", "BRG", "BRE", "BNE", "BLE"):
        return True
    return False

def fetchTwo(op: str) -> bool:
    if op in ("RSH", "LOD", "STR", "MOV", "IMM", "LSH", "INC", "DEC", "NEG", "NOT", "IN", "OUT", "SRS"):
        return True
    return False

def fetchOneTwo(op: str) -> bool:
    if op in ("BOD", "BEV", "BRZ", "BZR", "BNZ", "BZN", "BRN", "BRP"):
        return True
    return False

def fetchOne(op: str) -> bool:
    if op in ("JMP", "PSH", "CAL"):
        return True
    return False

def fetchNone(op: str) -> bool:
    if op in ("NOP", "POP", "RET", "HLT"):
        return True
    return False

def alpha() -> str:
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
