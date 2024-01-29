#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char charset[] = "!_acdefghilmnoprstuwy";

__int64_t hash_64_fnv1a(__int64_t begin, __uint64_t size) {
    int i;          // [rsp+14h] [rbp-1Ch]
    __int64_t hash; // [rsp+18h] [rbp-18h]

    hash = 0xCBF29CE484222325LL;
    for (i = 0; size > i; ++i)
        hash = 0x100000001B3LL * (*(__uint8_t *)(i + begin) ^ (__uint64_t)hash);
    return hash;
}

void bruteforce_key(__int64_t hash) {
    char key[4];
    int n = strlen(charset);

    for (int i = 0; i < n; ++i) {
        key[0] = charset[i];
        for (int j = 0; j < n; ++j) {
            key[1] = charset[j];
            for (int k = 0; k < n; ++k) {
                key[2] = charset[k];
                for (int l = 0; l < n; ++l) {
                    key[3] = charset[l];
                    if ((int)hash_64_fnv1a(&key, 4) == hash) {
                        printf("%s", key);
                        return;
                    }
                }
            }
        }
    }
    abort();
}

__int64_t hash[] = {18446744072877646971ULL,
                    842869369,
                    18446744071836832300ULL,
                    1874430657,
                    1643673264,
                    842869369,
                    18446744073484664935ULL,
                    51900271,
                    1261422793,
                    1041996681,
                    1470239221,
                    18446744073176831124ULL,
                    18446744072242323754ULL,
                    18446744073420943119ULL,
                    18446744071890218065ULL,
                    18446744073352623759ULL,
                    18446744073662195859ULL,
                    18446744072184189399ULL,
                    2055041019,
                    18446744072723039299ULL,
                    72314917};

int main() {
    for (int m = 0; m < 21; ++m) {
        bruteforce_key(hash[m]);
    }
}
