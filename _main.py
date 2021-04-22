# main file for offline testing

from bCompiler.bCompiler import compile
from MPU6Transpiler.MPU6Transpiler import MPU6Transpile

f = open("offlineInput.txt", "r+")
code = f.read()

print(compile(code[2:], 8, 2))