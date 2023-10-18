from string import ascii_lowercase, digits, punctuation


def rev_arr(n):
    global stack
    stack = stack[:-n] + stack[-n:][::-1]


def char2bin():
    n = stack[-1]
    stack.pop()
    for _ in range(8):
        stack.append(n & 1)
        n >>= 1


def bruteforce_char(x):
    for c in ascii_lowercase + digits + punctuation:
        stack[0] = ord(c)
        char2bin()
        stack.append(0xFF)
        rev_arr(9)
        rev_arr(8)
        stack.append(0)

        while True:
            rev_arr(2)
            stack.append(stack[-1] ^ 0xFF & 0xFF)

            if stack[-1] == 0:
                stack.pop()
                stack.pop()
                break

            stack.pop()
            if stack[-1]:
                stack[-2] = stack[-2] + 1 & 0xFF

            stack.pop()
            stack[-1] = stack[-1] * 3 & 0xFF
        if stack[0] == x:
            return c
    return None


cipher = [
    198,
    139,
    217,
    207,
    99,
    96,
    216,
    123,
    216,
    96,
    246,
    211,
    123,
    246,
    216,
    193,
    207,
    208,
    246,
    114,
    99,
    117,
    190,
    246,
    127,
    216,
    99,
    231,
    109,
    246,
    99,
    207,
    246,
    216,
    246,
    216,
    99,
    231,
    109,
    180,
    136,
    114,
    112,
    117,
    184,
    117,
]

stack = [0]

for c in cipher[::-1]:
    print(bruteforce_char(c), end="")
