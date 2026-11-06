#include "context.h"
u32 native_ov000_021da57c(u32 contextWord, u32 index, u32 triangle, u32 meshWord)
{
    u8 *context;
    u8 *mesh;
    s32 block;
    u32 ordinal;
    u32 prefix;
    s32 blockCount;
    context = (u8 *) contextWord;
    mesh = (u8 *) meshWord;
    context[0] = 1;
    *(u32 *) (context + 8) = index;
    *(u32 *) (context + 0xC) = triangle;
    blockCount = *(s16 *) (mesh + 8);
    ordinal = 0;
    prefix = 0;
    block = 0;
    if (blockCount > 0) {
        do {
            u32 next;
            next = prefix + *(u32 *) (mesh + 0x10);
            if ((s32) next <= (s32) index) {
                prefix = next;
                ordinal++;
            } else {
                index -= prefix;
                break;
            }
            block++;
            mesh += 0xC;
        } while (block < blockCount);
    }
    context[1] = (u8) ordinal;
    *(u32 *) (context + 4) = index;
    return contextWord;
}
