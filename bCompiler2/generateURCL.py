
# 4: Generate URCL
    # 1: traverse tokens left to right, converting to URCL
    # 2: return URCL code as a list with markers for temporary variables

def generateURCL(tokens, tokenMap, variables, functions, arrays: list) -> list:
    output = []

    number = 0
    while number < len(tokens):
        token = tokens[number]

        # auto or auto*
            # variable
            # function
            # array
        # while
        # if elseif else
        # asm
        # return
        # symbol
            # unary
            # binary
        # number or variable or %array

    return output
