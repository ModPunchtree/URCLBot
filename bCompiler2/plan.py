
# 0: Clean Code

# 1: Tokeniser
    # 1: loop over chars in code
    # 2: read each identifier/symbol into a list
    # 3: return tokens, tokenMap

# 2: Preprocess
    # 1: check brackets match
    # 2: check for ;
    # 3: find variables (including lists) and functions
    # 4: check for undefined identifers
    # 5: convert +/-/&/*/auto * into something unambiguous
    # 6: convert (auto) and (auto*) into something unambiguous
    # 7: return variables, functions, tokens, tokenMap

# 3: Reverse Polish
    # 1: convert to reverse polish using shunting yard
    # 2: return tokens, tokenMap

# 4: Generate URCL
    # 1: traverse tokens left to right, converting to URCL
    # 2: return URCL code as a list with markers for temporary variables

# 5: Compiler Optimisations
    # 1: optimise temporary variables
    # 2: return URCL code

# 6: General Optimisations


