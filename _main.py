# main file for offline testing

from genericURCLOptimiser.genericURCLOptimiser import genericURCLoptimiser
from URCLEmulator.URCLEmulator import emulate
from bCompiler.bCompiler import compile
from MPU6Transpiler.MPU6Transpiler import MPU6Transpile

f = open("offlineInput.txt", "r+")
code = f.read()

#code = code[5:]
#code = code.split("\n")
#print(MPU6Transpile(code))

print(compile(code[7:], 8, 8))
print(genericURCLoptimiser(compile(code[7:], 8, 8), 8))
