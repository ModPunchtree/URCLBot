def cleanCode(code: list) -> str:
    
    for i in range(len(code)):
        if code[i].find("//") != -1:
            code[i] = code[i][:code[i].find("//")]
        
    code = " ".join(code)
    code = code.replace("  ", " ")
    code = code.replace("  ", " ")
    
    while code.find("/*") != -1:
        code = code[: code.find("/*")] + code[code.find("*/") + 2:]
    
    return code