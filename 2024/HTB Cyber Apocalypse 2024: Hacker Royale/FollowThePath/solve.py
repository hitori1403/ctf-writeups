import sys

from qiling import Qiling
from qiling.const import QL_VERBOSE
from qiling.extensions import pipe

flag = []


def captain_hook(ql: Qiling, addr: int):
    xor_src = int.from_bytes(ql.mem.read(addr - 4, 4), "little")
    cmp_src = int.from_bytes(ql.mem.read(addr, 7)[-4:], "little")

    flag.append(cmp_src ^ xor_src)

    ql.arch.regs.r8 = cmp_src
    addr += 0x39
    ql.hook_address(captain_hook, addr, user_data=addr)


binary = ["../tools/rootfs/x8664_windows/chall.exe"]
rootfs = "/home/hitori/tools/rootfs/x8664_windows/"

ql = Qiling(binary, rootfs, verbose=QL_VERBOSE.OFF)

base_addr = ql.loader.images[0].base
cmp_inst = base_addr + 0x100E

ql.hook_address(captain_hook, cmp_inst, user_data=cmp_inst)

ql.os.stdin = pipe.SimpleInStream(sys.stdin.fileno())
ql.os.stdin.write(b"a" * 0x7F)

ql.run()

print(bytes(flag))
