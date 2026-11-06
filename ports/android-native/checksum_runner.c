#include <limits.h>
#include <stdio.h>
#include "generated/checksum_vectors.h"

_Static_assert(CHAR_BIT == 8, "Eight-bit bytes required");
_Static_assert(sizeof(unsigned int) == 4, "32-bit unsigned int required");
unsigned int save_payload_checksum(const void *block);
unsigned int save_header_checksum(const unsigned int *block);

static void fill(unsigned int *words, const ChecksumVector *vector) {
    unsigned int index;
    unsigned int state = vector->seed;
    for (index = 0; index < 0x1c40; index++) {
        unsigned int value = 0;
        switch (vector->kind) {
            case 1: value = 0xffffffffu; break;
            case 2: value = index * 0x9e3779b9u; break;
            case 3: value = (index & 1u) ? 0x55555555u : 0xaaaaaaaau; break;
            case 4:
                state ^= state << 13;
                state ^= state >> 17;
                state ^= state << 5;
                value = state;
                break;
            case 5: value = index == vector->index ? vector->value : 0; break;
            default: break;
        }
        words[index] = value;
    }
}

int main(void) {
    unsigned int words[0x1c40];
    unsigned int index;
    unsigned int failures = 0;
    unsigned int endian = 1;
    const char *target = "host";
#if defined(__ANDROID__)
    target = "android-native";
#endif
    if (*(const unsigned char *)&endian != 1) {
        fputs("Unsupported byte order\n", stderr);
        return 2;
    }
    for (index = 0; index < CHECKSUM_VECTOR_COUNT; index++) {
        const ChecksumVector *vector = &checksum_vectors[index];
        unsigned int payload;
        unsigned int header;
        fill(words, vector);
        payload = save_payload_checksum(words);
        header = save_header_checksum(words);
        if (payload != vector->payload || header != vector->header) {
            fprintf(stderr, "vector%u payload=%08x expected=%08x header=%08x expected=%08x\n",
                    index, payload, vector->payload, header, vector->header);
            failures++;
        }
    }
    printf("{\"target\":\"%s\",\"pointerBytes\":%u,\"vectors\":%u,\"functionComparisons\":%u,\"failures\":%u}\n",
           target, (unsigned int)sizeof(void *), CHECKSUM_VECTOR_COUNT, CHECKSUM_VECTOR_COUNT * 2u, failures);
    return failures ? 1 : 0;
}
