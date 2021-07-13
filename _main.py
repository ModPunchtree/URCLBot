# main file for offline testing

from bCompiler.bCompiler import bCompiler
from genericURCLOptimiser.genericURCLOptimiser import genericURCLoptimiser
from URCLEmulator.URCLEmulator import emulate
from bCompilerOLD.bCompiler import compile
from MPU6Transpiler.MPU6Transpiler import MPU6Transpile

f = open("offlineInput.txt", "r+")
code = f.read()

#code = code[5:]
#code = code.split("\n")
#print(MPU6Transpile(code))

#print(compile(code[7:], 8, 2))
#print("\n".join(genericURCLoptimiser(compile(code[7:], 8, 2), 8)))

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

#print("\n".join(bCompiler(code)))
#print("\n".join(genericURCLoptimiser([i.replace(" ", ",").replace(",", " ", 1).replace(",", ", ") for i in bCompiler(code)], 8)))

print("\n".join(genericURCLoptimiser(code, 8)))
