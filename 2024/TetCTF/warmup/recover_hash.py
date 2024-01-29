import subprocess

from z3 import *

xorshift128 = list(map(int, subprocess.check_output("./recover_xorshift128")[:-2].split(b",")))

v11 = [0] * 21
v11[0] = 0xFFFFFF6F11B8034B
v11[1] = 0x673420DAF2
v11[2] = 0x45EB817F02C
v11[3] = 0xFFFFFE3099503945
v11[4] = 0x18F8DCE1227
v11[5] = 0x26050EA6875
v11[6] = 0x298599C4BF0
v11[7] = 0xFFFFF8A356CE9E58
v11[8] = 0xFFFFFED3C712CF36
v11[9] = 0xFFFFFE96846D630F
v11[10] = 0x58CB1CE3FF3
v11[11] = 0xFFFFFCCF182C2A63
v11[12] = 0xFFFFFE57FDF3F1DE
v11[13] = 0xFFFFFA603F35F962
v11[14] = 0xFFFFFF7884570B57
v11[15] = 0x4897C4D9C1
v11[16] = 0xFFFFFEB9355E5CB4
v11[17] = 0xDCEDF7D094
v11[18] = 0x3602E9CAC47
v11[19] = 0xFFFFFEE3667219D6
v11[20] = 0xFFFFFDC326C9B063

hash = BitVecs(" ".join(f"hash_{i}" for i in range(21)), 64)

s = Solver()
for m in range(21):
    equation = f"v11[{m}] == " + " + ".join(f"{xorshift128[m * 21 + n]}*hash[{n}]" for n in range(21))
    eval(f"s.add({equation})")

print(s.check())
m = s.model()

for k in hash:
    print(m[k], end=",\n")
