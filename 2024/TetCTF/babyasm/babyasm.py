from z3 import *

g = [115, 82, 52, 149, 136, 67, 76, 97, 71, 90, 71, 74, 124, 104, 84, 67, 114, 127, 52, 31]
pos = [1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12, 17, 18, 19, 16]
enc = [
    38793,
    584,
    738,
    38594,
    63809,
    647,
    833,
    63602,
    47526,
    494,
    663,
    47333,
    67041,
    641,
    791,
    66734,
    35553,
    561,
    673,
    35306,
]

operator = ["+", "-", "*", "^"]
xor_val = [32, 36, 19, 55]

a = BitVecs(" ".join(f"a{i}" for i in range(20)), 8)
touched = [False] * 20

s = Solver()

for i in range(20):
    equation = (
        f"{enc[pos[i]]} == ((("
        + (str(enc[i]) if touched[i] else f"a[{i}]")
        + f"{operator[i % 4]} {g[i]}) + a[{pos[i]}]) ^ {xor_val[i % 4]}) + 83"
    )
    touched[pos[i]] = True
    eval(f"s.add({equation})")

print(s.check())
m = s.model()

print("TetCTF{", end="")
for i in range(20):
    print(chr(m[a[i]].as_long() - 83), end="")
