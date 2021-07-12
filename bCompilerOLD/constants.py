def alpha() -> str:
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def numeric() -> str:
    return "0123456789"

def unaryOperators() -> tuple:
    return ("!", "~", "-", "+", "*", "&", "++", "--", "auto", "return")

def binaryOperators() -> tuple:
    return ("||", "&&", "|", "^", "&", "!=", "==", ">=", ">", "<=", "<", ">>", "<<", "-", "+", "%", "/", "*")

def assignmentOperators() -> tuple:
    return ("=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=")

def operators() -> tuple:
    return (",",) + assignmentOperators() + binaryOperators() + unaryOperators()

def precedence(operator: str) -> int:
    if operator == "return":
        return 16
    if operator in operators():
        return operators().index(operator)
    return 0

def split(string: str) -> list:
    return [char for char in string]

def URCLOperations() -> tuple:
    return ("ADD", "RSH", "LOD", "NOR", "SUB", "MOV", "IMM", "LSH", "INC", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "IN", "POP", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE")


