import logging
import sys

from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)  # set level=20 or logging.INFO to turn of debug
logger = logging.getLogger("rich")


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)  # compute negative value
    return val  # return positive value as is


def ret():
    logger.debug("ret")
    exit()


def add():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x + y & 0xFF)
    logger.debug(f"add {x} {y}")


def sub():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x - y & 0xFF)
    logger.debug(f"sub {x} {y}")


def _and():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x & y & 0xFF)
    logger.debug(f"and {x} {y}")


def _or():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x | y & 0xFF)
    logger.debug(f"or {x} {y}")


def xor():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x ^ y & 0xFF)
    logger.debug(f"xor {x} {y}")


def shl():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x << y & 0xFF)
    logger.debug(f"shl {x} {y}")


def sar():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x >> y & 0xFF)
    logger.debug(f"sar {x} {y}")


def push_getchar():
    x = sys.stdin.read(1)
    stack.append(ord(x))
    logger.info(f"push_getchar {ord(x)} {x.encode()}")


def pop_putchar():
    c = stack[-1]
    stack.pop()
    # print(chr(c), end="")
    logger.debug(f"pop_putchar {c} {chr(c).encode()}")


def push():
    global rip
    x = mem[rip]
    stack.append(x)
    logger.info(f"push {x} \t{chr(x).encode()}")
    rip += 1


def js():
    global rip
    if stack[-1] < 0:
        x, y = mem[rip : rip + 2]
        dest = twos_comp(x << 8 | y, 16)
        rip += dest
        logger.debug(f"js {dest}")
    else:
        logger.warning("js")
    rip += 2


def jz():
    global rip
    if stack[-1] == 0:
        x, y = mem[rip : rip + 2]
        dest = twos_comp(x << 8 | y, 16)
        rip += dest
        logger.debug(f"jz {dest}")
    else:
        logger.warning("jz")
    rip += 2


def jmp():
    global rip
    x, y = mem[rip : rip + 2]
    dest = twos_comp(x << 8 | y, 16)
    rip += dest
    logger.debug(f"jmp {dest}")
    rip += 2


def pop():
    stack.pop()
    logger.debug("pop")


def dup():
    stack.append(stack[-1])
    logger.debug("dup")


def reverse_arr():
    global rip, stack
    n = mem[rip]
    stack = stack[:-n] + stack[-n:][::-1]
    logger.debug(f"reverse_arr {n}")
    rip += 1


def char2bin():
    nn = n = stack[-1]
    stack.pop()
    for _ in range(8):
        stack.append(n & 1)
        n >>= 1
    logger.debug(f"char2bin {nn}")


def bin2char():
    n = 0
    for _ in range(8):
        n = n << 1 | stack[-1]
        stack.pop()
    stack.append(n)
    logger.debug(f"bin2char {chr(n).encode()}")


def print_stack():
    logger.debug("print_stack")


instructions_table = {
    0: ret,
    1: add,
    2: sub,
    3: _and,
    4: _or,
    5: xor,
    6: shl,
    7: sar,
    8: push_getchar,
    9: pop_putchar,
    10: push,
    11: js,
    12: jz,
    13: jmp,
    14: pop,
    15: dup,
    16: reverse_arr,
    17: char2bin,
    18: bin2char,
    40: print_stack,
}


with open("program", "rb") as f:
    mem = f.read()

stack = []
rip = 0

while rip < len(mem):
    opcode = mem[rip]
    rip += 1

    if opcode in instructions_table:
        inst = instructions_table[opcode]
        # logger.debug(stack)
        inst()
    else:
        logger.debug(f"Unknown opcode: {hex(opcode)[2:]}")
        break
