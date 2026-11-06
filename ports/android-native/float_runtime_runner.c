#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "float_runtime_vectors.h"

extern double native_main_0202263c(double, double);
extern double native_main_02022684(double, int *);
extern double native_main_02022740(double, int);
extern int native_main_02023e48(double);
extern int native_main_02023e5c(double);
extern double native_main_02022664(double);
extern double native_main_02023ecc(double, int);
extern int native_main_02023ef8(const unsigned char *, const unsigned char *);

typedef union {
    uint64_t bits;
    double value;
} Binary64;

int main(void) {
    unsigned count = 0;
    for (unsigned i = 0; i < FLOAT_VECTOR_COUNT; ++i) {
        const FloatVector *item = &float_vectors[i];
        Binary64 x = {.bits = item->x}, y = {.bits = item->y}, result;
        uint64_t bits;
        switch (item->kind) {
            case 0:
                result.value = native_main_0202263c(x.value, y.value);
                bits = result.bits;
                break;
            case 1: {
                struct { uint32_t before; int exponent; uint32_t after; } output = {0x12345678u, 99, 0xA5A55A5Au};
                result.value = native_main_02022684(x.value, &output.exponent);
                if (output.before != 0x12345678u || output.after != 0xA5A55A5Au || output.exponent != item->exponent) return 2;
                bits = result.bits;
                break;
            }
            case 2:
                result.value = native_main_02022740(x.value, item->scale);
                bits = result.bits;
                break;
            case 3:
                bits = (uint32_t)native_main_02023e48(x.value);
                break;
            case 4:
                bits = (uint32_t)native_main_02023e5c(x.value);
                break;
            case 5:
                result.value = native_main_02022664(x.value);
                bits = result.bits;
                break;
            case 6:
                result.value = native_main_02023ecc(x.value, item->scale);
                bits = result.bits;
                break;
            default:
                return 3;
        }
        if (bits != item->result) {
            printf("Float case %u failed\n", i);
            return 4;
        }
        ++count;
    }
    for (unsigned i = 0; i < BYTE_VECTOR_COUNT; ++i) {
        const ByteVector *item = &byte_vectors[i];
        unsigned char left[160], right[160];
        memcpy(left, item->left, sizeof(left));
        memcpy(right, item->right, sizeof(right));
        const unsigned char *second = item->aliased ? left : right;
        uint32_t result = (uint32_t)native_main_02023ef8(left, second);
        if (result != item->result || memcmp(left, item->left, sizeof(left)) || memcmp(right, item->right, sizeof(right))) {
            printf("Byte case %u failed\n", i);
            return 5;
        }
        ++count;
    }
    if (count != 2912) return 6;
    printf("J2P float runtime: %u cases passed\n", count);
    return 0;
}
