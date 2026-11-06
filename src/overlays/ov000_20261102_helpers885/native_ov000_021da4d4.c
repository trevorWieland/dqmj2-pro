#include "context.h"
u32 native_ov000_021da4d4(u32 output, u32 offset, s32 count)
{
    s32 written;
    s32 ordinal;
    u32 choice;
    u32 bound;
    written = 0;
    ordinal = written;
    bound = (u32) count - 1U;
    do {
        do {
            choice = offset + (u32) native_fn_ov000_021da484(ordinal);
            ordinal++;
        } while (choice > bound);
        ((u8 *) output)[written] = (u8) choice;
        written++;
    } while (written < count);
    return (u32) ordinal;
}
