
from bCompiler.constants import URCLOperations

def JMPtoJMP() -> None:
    line = 0
    while line + 1 < len(output):
        if output[line][:3] == "JMP":
            label = output[line][4:]
            if output[output.index(label) + 1][:3] == "JMP":
                output[line] = "JMP " + output[output.index(label) + 1][4:]
                line = 0
            else:
                line += 1
        else:
            line += 1

def optimiseLabels() -> None:
    
    def deleteDuplicateLabels() -> None:
        line = 0
        while line + 1 < len(output):
            if output[line][:1] == ".":
                label1 = output[line]
                line1 = line
                while output[line + 1][:2] == "//":
                    line += 1
                if output[line + 1][:1] == ".":
                    label2 = output[line + 1]
                    for i in range(len(output)):
                        output[i] = output[i].replace(label1, label2)
                    output.pop(line1)
                    line = 0
                else:
                    line += 1
            else:
                line += 1
        
    def deleteUselessLabels() -> None:
        line = 0
        while line < len(output):
            if output[line][:1] == ".":
                notFound = True
                for i in output:
                    if (i.find(output[line]) != -1) and (i[:1] != "."):
                        notFound = False
                if notFound:
                    output.pop(line)
                    line = 0
                else:
                    line += 1
            else:
                line += 1

    deleteDuplicateLabels()
    deleteUselessLabels()

def SETBRZ() -> None:
    line = 0
    while line + 1 < len(output):
        if output[line].startswith("SET"):
            line1 = line
            while output[line + 1].startswith("//"):
                line += 1
            if output[line + 1].startswith("BRZ"):
                label = output[line + 1][output[line + 1].index("."): output[line + 1].index(",")]
                if output[line1].startswith("SETNE"):
                    temp = "BRE "
                elif output[line1].startswith("SETGE"):
                    temp = "BRL "
                elif output[line1].startswith("SETLE"):
                    temp = "BRG "
                elif output[line1].startswith("SETE"):
                    temp = "BNE "
                elif output[line1].startswith("SETG"):
                    temp = "BLE "
                elif output[line1].startswith("SETL"):
                    temp = "BGE "
                output[line + 1] = temp + label + output[line1][output[line1].index(","):]
                output.pop(line1)
                line = 0
            else:
                line += 1
        else:
            line += 1

def LODURCLOperation() -> None:
    line = 0
    while line + 1 < len(output):
        if output[line].startswith("LOD"):
            line1 = line
            op1 = output[line][4: output[line].index(",")]
            while output[line + 1].startswith("//"):
                line += 1
            if output[line + 1].startswith(URCLOperations()):
                if output[line + 1].find(",") == -1:
                    op2 = output[line + 1][4:]
                else:
                    op2 = output[line + 1][4: output[line + 1].index(",")]
                if op1 == op2:
                    output.pop(line1)
                    line = 0
                else:
                    line += 1
            else:
                line += 1
        else:
            line += 1

def MOVtoIMM() -> None:
    for i in range(len(output)):
        if output[i].startswith("MOV"):
            op2 = output[i][output[i].find(",") + 2:]
            if op2.isnumeric():
                output[i] = "IMM" + output[i][3:]

def BRZIMM() -> None:
    for i in range(len(output)):
        if output[i].startswith("BRZ"):
            op2 = output[i][output[i].find(",") + 2:]
            if op2.isnumeric():
                if op2 == "0":
                    output[i] = "JMP" + output[i][3: output[i].find(",")]
                else:
                    output.pop(i)
                    return BRZIMM()

def RETJMP() -> None:
    for i in range(len(output) - 1):
        if output[i] == "RET":
            while output[i + 1].startswith("//"):
                i += 1
            if output[i + 1].startswith("JMP"):
                output.pop(i + 1)
                return RETJMP()
            elif output[i + 1].startswith("PSH") and output[i + 2].startswith("RET"):
                output.pop(i + 2)
                output.pop(i + 1)
                return RETJMP()

def ADDSUBtoINCDEC() -> None:
    for i in range(len(output)):
        if output[i].endswith(" 1"):
            if output[i].startswith("ADD"):
                output[i] = "INC" + output[i][3:-3]
            elif output[i].startswith("SUB"):
                output[i] = "DEC" + output[i][3:-3]

def URCLOperationMOV() -> None:
    line = 0
    while line < (len(output) - 2):
        if output[line].startswith(URCLOperations()):
            if output[line].find(",") != -1:
                op1 = output[line][output[line].index(" ") + 1: output[line].index(",")]
            else:
                op1 = output[line][output[line].index(" ") + 1:]
            if output[line + 1] == "//TEMP":
                if output[line + 2].startswith("MOV"):
                    op2 = output[line + 2][output[line + 2].index(",") + 2:]
                    if op1 == op2:
                        op3 = output[line + 2][4: output[line + 2].index(",")]
                        output[line] = output[line][: output[line].index(" ") + 1] + op3 + output[line][output[line].index(","):]
                        output.pop(line + 2)
                        line = 0
                    else:
                        line += 1
                else:
                    line += 1
            else:
                line += 1
        else:
            line += 1

def delTEMP() -> None:
    line = 0
    while line < len(output):
        if output[line] == "//TEMP":
            output.pop(line)
        else:
            line += 1

def optimise(output_: list) -> list:
    
    global output; output = output_
    
    optimiseLabels()
    JMPtoJMP()
    optimiseLabels()
    SETBRZ()
    LODURCLOperation()
    MOVtoIMM()
    BRZIMM()
    optimiseLabels()
    RETJMP()
    optimiseLabels()
    ADDSUBtoINCDEC()
    URCLOperationMOV()
    delTEMP()
    
    return output


