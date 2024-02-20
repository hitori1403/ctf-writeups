# tag: easy, nanomites, jzjnz

from ctypes import *

enc = bytes.fromhex("0c5c60206963640f4f1e333a682a7cd9d5d0c9e7c3f0bcab9bd7988bafb0f84749164968")

for i in range(0, 0x24):
    xor_result = c_uint8((i + 1 >> 5) | (i + 1 << 3) ^ 0xCA ^ 0xFE).value
    # xor_result = c_uint8(xor_result | 0x7FFC9286A800).value # no effect
    print(chr(xor_result ^ enc[i]), end="")

# 0xL4ugh{3z_n4n0mites_t0_g3t_st4rt3d}
