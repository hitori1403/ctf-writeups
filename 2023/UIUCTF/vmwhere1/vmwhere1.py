import logging
import sys

# logging.basicConfig(level=logging.DEBUG)


def bruteforce_char(c):
    for x in range(32, 128):
        if x ^ (x >> 4) ^ prev_cipher == c:
            print(chr(x), end="")


def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)  # compute negative value
    return val  # return positive value as is


def add():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x + y)
    logging.debug(f"add {x} {y}")


def sub():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x - y)
    logging.debug(f"sub {x} {y}")


def _and():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x & y)
    logging.debug(f"and {x} {y}")


def _or():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x | y)
    logging.debug(f"or {x} {y}")


def xor():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()

    # --- for finding flag
    if prev_opcode[-2:] == [15, 10]:
        bruteforce_char(y)
        x = y
        stack.append(0)

        global prev_cipher
        prev_cipher = y
    else:
        # --- real xor function
        stack.append(x ^ y)

    logging.debug(f"xor {x} {y}")


def shl():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x << y)
    logging.debug(f"shl {x} {y}")


def sar():
    x, y = stack[-2:]
    stack.pop()
    stack.pop()
    stack.append(x >> y)
    logging.debug(f"sar {x} {y}")


def push_getchar():
    # x = sys.stdin.read(1)
    x = "a"
    stack.append(ord(x))
    logging.debug(f"push_getchar {ord(x)} {x.encode()}")


def pop_putchar():
    c = stack[-1]
    stack.pop()
    print(chr(c), end="")
    logging.debug(f"pop_putchar {c} {chr(c).encode()}")


def push():
    global rip
    x = mem[rip]
    stack.append(x)
    logging.debug(f"push {x} \t{chr(x).encode()}")
    rip += 1


def js():
    global rip
    if stack[-1] < 0:
        x, y = mem[rip : rip + 2]
        dest = twos_comp(x << 8 | y, 16)
        logging.debug(f"js {dest}")
    else:
        logging.debug("[x] js")
    rip += 2


def jz():
    global rip
    if stack[-1] == 0:
        x, y = mem[rip : rip + 2]
        dest = twos_comp(x << 8 | y, 16)
        rip += dest
        logging.debug(f"jz {dest}")
    else:
        logging.debug("[x] jz")
    rip += 2


def jmp():
    global rip
    x, y = mem[rip : rip + 2]
    dest = twos_comp(x << 8 | y, 16)
    rip += dest
    logging.debug(f"jmp {dest}")
    rip += 2


def pop():
    stack.pop()
    logging.debug("pop")


def dup():
    stack.append(stack[-1])
    logging.debug("dup")


def reverse_arr():
    global rip, stack
    n = mem[rip]
    stack = stack[:-n] + stack[-n:][::-1]
    logging.debug(f"reverse_arr {n}")
    rip += 1


def print_stack():
    logging.debug("print_stack")


instructions_table = {
    0: "mov eax, 0",
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
    40: print_stack,
}


with open("program", "rb") as f:
    mem = f.read()

prev_opcode = []
prev_cipher = 0
stack = []
rip = 0

while rip < len(mem):
    opcode = mem[rip]
    rip += 1

    if opcode in instructions_table:
        inst = instructions_table[opcode]
        if isinstance(inst, str):
            logging.debug(inst)
        else:
            inst()
        prev_opcode.append(opcode)
    else:
        logging.debug("Unknown opcode:", opcode)

print()
