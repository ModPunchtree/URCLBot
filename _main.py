# main file for offline testing

from bCompiler2.bCompiler import bCompiler2
from genericURCLOptimiser.genericURCLOptimiser import genericURCLoptimiser
from URCLEmulator.URCLEmulator import emulate
from bCompiler.bCompiler import compile
from MPU6Transpiler.MPU6Transpiler import MPU6Transpile

f = open("offlineInput.txt", "r+")
code = f.read()

#code = code[5:]
#code = code.split("\n")
#print(MPU6Transpile(code))

#print(compile(code[7:], 8, 9))
print("\n".join(genericURCLoptimiser(compile(code[7:], 8, 9), 8)))

"""
text = code[5: ]
text = text.upper()
while text.find("  ") != -1:
    text = text.replace("  ", " ")
text = text.split("\n")
for i, j in enumerate(text):
    if (j.find(",") == -1) and (j.find("=") == -1):
        text[i] = (j.replace(" ", ", ")).replace(", ", " ", 1)
text = "\n".join(text)
print(emulate(text, True, False))
"""

#print(emulate(code[5: ].upper(), True, False))

#print(bCompiler2(code))
