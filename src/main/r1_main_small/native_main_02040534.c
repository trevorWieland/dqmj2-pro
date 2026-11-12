/* Clear the requested bits of a global control word using orr+eor.
   Unknowns: the block role and the bit meanings. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

extern u8 native_data_020f6054[];
u32 native_main_02040534(u32 mask) {
    u32 old = M2C_FIELD(native_data_020f6054, u32 *, 0x34);
    u32 both = old | mask;
    M2C_FIELD(native_data_020f6054, u32 *, 0x34) = both ^ mask;
    return old;
}