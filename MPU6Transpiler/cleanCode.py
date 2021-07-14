
from MPU6Transpiler.constants import MPU

def readNum(text: str) -> int:
    temp = ""
    for i in text:
        if (i.isnumeric()) or (i == "x"):
            temp += i
        else:
            return int(temp)

def uniqueNum() -> str:
    global uniqueNumber
    uniqueNumber += 1
    return str(uniqueNumber)

def cleanCode(code: tuple) -> list:
    global uniqueNumber; uniqueNumber = -1
    urclCode = list(code)
    line = 0
    while line < len(urclCode):

        while urclCode[line].startswith(" "):
            urclCode[line] = urclCode[line][1:]

        if urclCode[line].find("//") != -1:
            urclCode[line] = urclCode[line][: urclCode[line].find("//")]
            
        if urclCode[line].find("'") != -1:
            char = urclCode[line][urclCode[line].find("'") + 1: urclCode[line].find("'") + 2]
            urclCode[line] = urclCode[line][: urclCode[line].find("'")] + MPU(char) + urclCode[line][urclCode[line].find("'") + 3:]
        
        if urclCode[line].find('"') != -1:
            char = urclCode[line][urclCode[line].find('"') + 1: urclCode[line].find('"') + 2]
            urclCode[line] = urclCode[line][: urclCode[line].find('"')] + MPU(char) + urclCode[line][urclCode[line].find('"') + 3:]

        if urclCode[line].find("+") != -1:
            num = readNum(urclCode[urclCode[line].find("+") + 1:])
            label = ".RELATIVE" + uniqueNum()
            urclCode.insert(line + num, label)
            urclCode[line] = urclCode[line][: urclCode[line].find("+")] + label + urclCode[line][urclCode[line].find("+") + len(str(num)) + 1:]
    
        if urclCode[line].find("-") != -1:
            num = readNum(urclCode[urclCode[line].find("-") + 1:])
            label = ".RELATIVE" + uniqueNum()
            urclCode.insert(line - num, label)
            urclCode[line] = urclCode[line][: urclCode[line].find("-")] + label + urclCode[line][urclCode[line].find("-") + len(str(num)) + 1:]
    
        if urclCode[line].find("SP") != -1:
            urclCode[line] = urclCode[line].replace("SP", "R10")
    
        if urclCode[line].startswith(("BITS", "MINREG", "MINHEAP", "RUN ROM", "RUN RAM")):
            urclCode[line] = ""
    
        if not(urclCode[line]):
            urclCode.pop(line)
        else:
            line += 1
            
    return urclCode