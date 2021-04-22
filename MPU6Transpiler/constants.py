
def URCLInstructions() -> tuple:
    return ("ADD", "RSH", "LOD", "STR", "JMP", "BGE", "NOR", "SUB", "MOV", "NOP", "IMM", "LSH", "INC", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BZR", "BNZ", "BZN", "BRN", "BRP", "IN", "OUT", "PSH", "POP", "CAL", "RET", "HLT", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE")

def alpha() -> str:
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def MPU(char: str) -> str:
    return str("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_,?><≥≤=-+ǁΣ√()/\^✓✘ΔδλθΠ.∞ ".index(char))
