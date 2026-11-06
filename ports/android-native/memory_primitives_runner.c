#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "memory_primitive_vectors.h"

extern void *native_main_0201b21c(const void *, int, unsigned int);
extern int native_main_0201b248(const void *, const void *, unsigned int);
extern void native_main_0201b288(void *, int, unsigned int);
_Static_assert(sizeof(unsigned int) == 4, "32-bit native word");
_Static_assert(sizeof(void *) == 8, "64-bit target pointer");

int main(void) {
    unsigned char *buffer = malloc(4096);
    unsigned char expected[4096];
    unsigned int tag;
    if (!buffer) {
        return 2;
    }
    for (tag = 0; tag < MEMORY_VECTOR_COUNT; ++tag) {
        const MemoryVector *v = &memory_vectors[tag];
        unsigned int index;
        unsigned int offset = 0x100 + v->alignment;
        unsigned int other = 0x600 + v->alignment;
        int result = 0;
        for (index = 0; index < 4096; ++index) {
            buffer[index] = (unsigned char)(index * 73 + tag * 11);
        }
        if (v->mode == 0) {
            for (index = 0; index < v->count; ++index) {
                buffer[offset + index] = (unsigned char)(v->value + 1);
            }
            if (v->count && v->relation != 2) {
                buffer[offset + (v->relation == 0 ? 0 : v->count - 1)] = (unsigned char)v->value;
            }
        } else if (v->mode == 1) {
            for (index = 0; index < v->count; ++index) {
                buffer[offset + index] = buffer[other + index] = (unsigned char)v->value;
            }
            if (v->relation) {
                buffer[other + (v->relation == 1 ? 0 : v->count - 1)] = (unsigned char)(v->value + v->relation);
            }
        }
        memcpy(expected, buffer, 4096);
        if (v->mode == 2) {
            for (index = 0; index < v->count; ++index) {
                expected[offset + index] = (unsigned char)v->value;
            }
            native_main_0201b288(buffer + offset, (int)v->value, v->count);
        } else if (v->mode == 0) {
            void *found = native_main_0201b21c(buffer + offset, (int)(v->value | (tag << 8)), v->count);
            result = found ? (int)((unsigned char *)found - buffer) : -1;
        } else {
            result = native_main_0201b248(buffer + offset, buffer + other, v->count);
        }
        if (result != v->expected || memcmp(buffer, expected, 4096)) {
            printf("failed vector %u mode %u\n", tag, v->mode);
            free(buffer);
            return 1;
        }
    }
    free(buffer);
    printf("J2P memory primitives: %u cases passed\n", MEMORY_VECTOR_COUNT);
    return 0;
}
