# main file for offline testing

from URCLEmulator.URCLEmulator import emulate
from bCompiler.bCompiler import compile
from MPU6Transpiler.MPU6Transpiler import MPU6Transpile

f = open("offlineInput.txt", "r+")
code = f.read()

code = code[5:]
code = code.split("\n")
print(MPU6Transpile(code))
