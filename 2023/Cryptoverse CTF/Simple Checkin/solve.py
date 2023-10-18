import sys

from qiling import Qiling
from qiling.const import QL_VERBOSE
from qiling.extensions import pipe

enc = []
pattern = []


def copy_pattern(ql: Qiling):
    global pattern
    pattern.append(ql.arch.regs.ecx)


def copy_enc(ql: Qiling) -> None:
    global enc
    enc.append(ql.arch.regs.eax)
    ql.arch.regs.ecx = ql.arch.regs.eax


def sandbox(path, rootfs):
    ql = Qiling(path, rootfs, verbose=QL_VERBOSE.OFF)

    base_addr = ql.loader.images[0].base

    ql.hook_address(copy_pattern, base_addr + 0x2DCE)
    ql.hook_address(copy_enc, base_addr + 0x2DDD)

    ql.os.stdin = pipe.SimpleInStream(sys.stdin.fileno())
    ql.os.stdin.write(b"a")

    ql.run()


sandbox(["./challenge"], "/home/meo/tools/qiling/rootfs/x8664_linux")

for i, j in zip(enc, pattern):
    print(chr(i ^ j), end="")

print()
