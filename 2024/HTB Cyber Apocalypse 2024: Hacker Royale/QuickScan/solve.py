import struct
from base64 import b64decode

from capstone import Cs
from pwn import *
from qiling import Qiling
from qiling.const import QL_VERBOSE


def captain_hook(ql: Qiling, addr: int, size: int, md: Cs):
    buf = ql.mem.read(addr, size)
    for inst in md.disasm(buf, addr):
        if inst.mnemonic == "syscall":
            content = ""
            for _ in range(3):
                content += struct.pack("<Q", ql.stack_pop()).hex()

            log.info(content)
            r.sendline(content.encode())


binary = ["./bin"]
rootfs = "/home/hitori/tools/rootfs/x8664_linux/"

r = remote("94.237.49.197", 30192)

while True:
    try:
        r.recvuntil(b"ELF:  ")
        elf_content = r.recvline()
        r.recvuntil(b"Bytes? ")

        with open("./bin", "wb") as f:
            f.write(b64decode(elf_content))

        ql = Qiling(binary, rootfs, verbose=QL_VERBOSE.OFF)
        ql.hook_code(captain_hook, user_data=ql.arch.disassembler)
        ql.run()
    except:
        print(r.recvall())
        break
