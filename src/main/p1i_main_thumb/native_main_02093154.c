#include "context.h"

/* Convert big-endian byte words into host words. */
void native_main_02093154(u32 *destination, const u8 *source, u32 bytes)
{
    u32 offset;

    for (offset = 0; offset < bytes; offset += 4) {
        u32 value = ((u32)source[offset] << 24) | ((u32)source[offset + 1] << 16) |
                    ((u32)source[offset + 2] << 8) | (u32)source[offset + 3];

        *destination = value;
        destination++;
    }
}
