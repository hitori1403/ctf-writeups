#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int global[] = {115, 82, 52, 149, 136, 67, 76, 97, 71, 90, 71, 74, 124, 104, 84, 67, 114, 127, 52, 31};
int pos[] = {1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12, 17, 18, 19, 16};
int enc[] = {38793, 584,   738,   38594, 63809, 647,   833,   63602, 47526, 494,
             663,   47333, 67041, 641,   791,   66734, 35553, 561,   673,   35306};

int cmp_with_enc(int arr[]) {
    // for (int i = 0; i < 20; ++i) {
    //     printf("%d\n", arr[i]);
    // }
    for (int i = 0; i < 20; ++i) {
        if (arr[i] != enc[i]) {
            printf("mismatched %d\n", i);
            return 0;
        }
    }
    return 1;
}

void array_fill(int arr[], int pos, int value) {
    value += 83;
    arr[pos] = value;
}

void process(int arr[], int opr, int pos, int value) {
    value += arr[pos];
    switch (opr) {
    case 0:
        value ^= 32;
        break;
    case 1:
        value ^= 36;
        break;
    case 2:
        value ^= 19;
        break;
    case 3:
        value ^= 55;
        break;
    }
    array_fill(arr, pos, value);
}

int check(int arr[]) {
    for (int i = 0; i < 20; ++i) {
        int value = 0;
        switch (i % 4) {
        case 0:
            value = arr[i] + global[i];
            break;
        case 1:
            value = arr[i] - global[i];
            break;
        case 2:
            value = arr[i] * global[i];
            break;
        case 3:
            value = arr[i] ^ global[i];
            break;
        }
        process(arr, i % 4, pos[i], value);
    }
    return cmp_with_enc(arr);
}

int main() {
    char flag[] = "TetCTF{aaaaaaaaaaaaaaaaaaa}";

    int arr[20];

    for (int i = 0; i < 20; ++i) {
        array_fill(arr, i, flag[i + 7]);
    }

    printf("%d", check(arr));
}
