#include <assert.h>
#include <limits.h>
#include <stdio.h>

__u_int key[] = {19088743, 2309737967, 4275878552, 1985229328};

int main() {
    int v4 = 0;
    for (int i = 0; i < 32; ++i) {
        v4 -= 0x61C88647;
    }

    __u_int part1 = 0xF27AEDBF, part2 = 0xED00B66C;

    for (int i = 31; i >= 0; --i) {
        printf("%d\n", i);

        // part1 += (part2 + v4) ^ (16 * part2 + *key) ^ ((part2 >> 5) + key[1]);
        // v4 -= 0x61C88647;
        // part2 += ((part1 >> 5) + key[3]) ^ (part1 + v4) ^ (16 * part1 + key[2]);

        __u_int p1 = 0, p2 = 0;
        int found = 0;

        for (; p2 <= UINT_MAX; ++p2) {
            if (part2 == p2 + (((part1 >> 5) + key[3]) ^ (part1 + v4) ^ (16 * part1 + key[2]))) {
                found = 1;
                break;
            }
        }
        assert(found);
        part2 = p2;

        v4 += 0x61C88647;

        found = 0;
        for (; p1 <= UINT_MAX; ++p1) {
            if (part1 == p1 + ((part2 + v4) ^ (16 * part2 + *key) ^ ((part2 >> 5) + key[1]))) {
                found = 1;
                break;
            }
        }
        assert(found);
        part1 = p1;
    }

    printf("%u %u\n", part1, part2);
    // 141414 161616
}
