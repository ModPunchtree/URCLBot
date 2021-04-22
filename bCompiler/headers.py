
def headers(output: list, BITS) -> list:
    head = []
    
    head.append("BITS == " + str(BITS))
    
    regs = [0]
    for i in output:
        while i.find("R") != -1:
            if i[i.find("R") + 1: i.find("R") + 3].isnumeric():
                num = int(i[i.find("R") + 1: i.find("R") + 3])
            elif i[i.find("R") + 1: i.find("R") + 2].isnumeric():
                num = int(i[i.find("R") + 1: i.find("R") + 2])
            else:
                num = 0
            regs.append(num)
            i = i.replace("R", "$", 1)
    REG = str(max(regs))
    head.append("MINREG " + REG)
    
    mems = [0]
    for i in output:
        while i.find("M") != -1:
            if i[i.find("M") + 1: i.find("M") + 4].isnumeric():
                num = int(i[i.find("M") + 1: i.find("M") + 4])
            if i[i.find("M") + 1: i.find("M") + 3].isnumeric():
                num = int(i[i.find("M") + 1: i.find("M") + 3])
            elif i[i.find("M") + 1: i.find("M") + 2].isnumeric():
                num = int(i[i.find("M") + 1: i.find("M") + 2])
            else:
                num = 0
            mems.append(num)
            i = i.replace("M", "#", 1)
    MEM = str(max(mems))
    head.append("MINRAM " + MEM)
    
    output = head + output
    
    return output