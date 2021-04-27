
from MPU6Transpiler.cleanCode import cleanCode
from MPU6Transpiler.singleURCLTranslations import singleUrclTranslations
from MPU6Transpiler.constants import URCLInstructions, alpha

def readOps(text: str) -> tuple:
    char = 0
    ops = ()
    temp = ""
    while char < len(text):
        if text[char] == " ":
            pass
        elif text[char] == ",":
            if temp[0] == "M":
                temp = temp[1:]
            ops += (temp,)
            temp = ""
        else:
            temp += text[char]
        char += 1
    if temp:
        ops += (temp,)
    return ops

def getOpTypes(ops: tuple) -> tuple:
    types = ()
    for i in ops:
        if (i[0].isnumeric()) or (i[0] == "."):
            types += ("IMM",)
        elif i[0] == "R":
            types += ("REG",)
        else:
            types += (i,)
    return types
            
def MPU6Transpile(code: tuple) -> tuple:
    output = ("LDI(R10, 32);;",)
    line = 0
    urclCode = cleanCode(code)

    while line < len(urclCode):
        if urclCode[line].startswith(URCLInstructions()):
            if urclCode[line][:5] in URCLInstructions():
                op = urclCode[line][:5]
            elif urclCode[line][:4] in URCLInstructions():
                op = urclCode[line][:4]
            elif urclCode[line][:3] in URCLInstructions():
                op = urclCode[line][:3]
            elif urclCode[line][:2] in URCLInstructions():
                op = urclCode[line][:2]
            else:
                return "FATAL 0x02 - Unrecognised instruction: " + urclCode[line]
            
            ops = readOps(urclCode[line][len(op):])
            opTypes = getOpTypes(ops)
            
            if op not in ("XNOR", "XOR"):
                translation = singleUrclTranslations()[" ".join((op,) + opTypes)]
                
                for i, j in enumerate(ops):
                    for k, l in enumerate(translation):
                        translation[k] = l.replace("<" + alpha()[i] + ">", j)
                
                for i in translation:
                    output += (i,)

                line += 1
                
            elif op == "XNOR":
                temp = []
                if ops[1] == ops[2]:
                    temp.append("NOR <A>, 0, 0")
                elif ops[0] != "R1":
                    temp.append("AND <A>, <B>, <C>")
                    temp.append("PSH R1")
                    temp.append("NOR R1, <B>, <C>")
                    temp.append("NOR <A>, <A>, R1")
                    temp.append("POP R1")
                    temp.append("NOR <A>, <A>, 0")
                else:
                    temp.append("AND <A>, <B>, <C>")
                    temp.append("PSH R2")
                    temp.append("NOR R1, <B>, <C>")
                    temp.append("NOR <A>, <A>, R2")
                    temp.append("POP R2")
                    temp.append("NOR <A>, <A>, 0")
                    
                for i, j in enumerate(ops):
                    for k, l in enumerate(temp):
                        temp[k] = l.replace("<" + alpha()[i] + ">", j)
                urclCode = urclCode[: line] + temp + urclCode[line + 1:]
            
            elif op == "XOR":
                temp = []
                if ops[1] == ops[2]:
                    temp.append("ADD <A>, 0, 0")
                elif ops[0] != "R1":
                    temp.append("AND <A>, <B>, <C>")
                    temp.append("PSH R1")
                    temp.append("NOR R1, <B>, <C>")
                    temp.append("NOR <A>, <A>, R1")
                    temp.append("POP R1")
                else:
                    temp.append("AND <A>, <B>, <C>")
                    temp.append("PSH R2")
                    temp.append("NOR R2, <B>, <C>")
                    temp.append("NOR <A>, <A>, R2")
                    temp.append("POP R2")
                    
                for i, j in enumerate(ops):
                    for k, l in enumerate(temp):
                        temp[k] = l.replace("<" + alpha()[i] + ">", j)
                urclCode = urclCode[: line] + temp + urclCode[line + 1:]

        elif urclCode[line].startswith("."):
            output += (urclCode[line],)
            line += 1

        else:
            return "FATAL 0x01 - Unrecognised instruction: " + urclCode[line]
    
    return "\n".join(output)

