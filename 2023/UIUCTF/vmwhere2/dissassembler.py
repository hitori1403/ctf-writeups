import ctypes

DEBUG = True

colors = {
    "red": "\x1b[1;31;40m",
    "green": "\x1b[1;32;40m",
    "blue": "\x1b[1;34;40m",
}


def debug(msg, color="green"):
    if DEBUG:
        print(f"{colors[color]}{vip - 1}: {msg}\x1b[0m")


def ret():
    debug("mov eax, 0")


def add():
    debug("add")


def sub():
    debug("sub")


def _and():
    debug("and")


def _or():
    debug("or")


def xor():
    debug("xor")


def shl():
    debug("shl")


def sar():
    debug("sar")


def getchar():
    debug("getchar", 'red')


def putchar():
    debug("putchar")


def push():
    global vip
    x = mem[vip]
    debug(f"push {x} \t{chr(x).encode()}", 'red')
    vip += 1


def js():
    global vip
    dest = vip + 2 + ctypes.c_int16(int.from_bytes(mem[vip : vip + 2], "big")).value
    debug(f"js {dest}", "blue")
    vip += 2


def jz():
    global vip
    dest = vip + 2 + ctypes.c_int16(int.from_bytes(mem[vip : vip + 2], "big")).value
    debug(f"jz {dest}", "blue")
    vip += 2


def jmp():
    global vip
    dest = vip + 2 + ctypes.c_int16(int.from_bytes(mem[vip : vip + 2], "big")).value
    debug(f"jmp {dest}", "blue")
    vip += 2


def pop():
    debug("pop")


def dup():
    debug("dup")


def rev_arr():
    global vip, stack
    n = mem[vip]
    debug(f"rev_arr {n}")
    vip += 1


def char2bin():
    debug("char2bin")


def bin2char():
    debug("bin2char")


def print_stack():
    debug("print_stack")


instructions_table = {
    0: ret,
    1: add,
    2: sub,
    3: _and,
    4: _or,
    5: xor,
    6: shl,
    7: sar,
    8: getchar,
    9: putchar,
    10: push,
    11: js,
    12: jz,
    13: jmp,
    14: pop,
    15: dup,
    16: rev_arr,
    17: char2bin,
    18: bin2char,
    40: print_stack,
}


with open("program", "rb") as f:
    mem = f.read()

vip = 0

while vip < len(mem):
    opcode = mem[vip]
    vip += 1

    if opcode in instructions_table:
        instructions_table[opcode]()
    else:
        debug(f"Unknown opcode: {hex(opcode)[2:]}")
        break
