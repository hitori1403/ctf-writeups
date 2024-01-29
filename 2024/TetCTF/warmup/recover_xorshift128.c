#include <stdio.h>
#include <string.h>

int x = 123456789;
int y = 362436069;
int z = 521288629;
int w = -559038737;

__int64_t xorshift128() {
    unsigned int v1; // [rsp+0h] [rbp-4h]

    v1 = (((x << 11) ^ (unsigned int)x) >> 8) ^ (x << 11) ^ x;
    x = y;
    y = z;
    z = w;
    w ^= (unsigned int)w >> 19;
    w ^= v1;
    return (unsigned int)w;
}

int main() {
    for (int m = 0; m <= 0x14; ++m) {
        for (int n = 0; n <= 0x14; ++n) {
            printf("%d, ", (int)xorshift128() % 1024);
        }
    }
}
