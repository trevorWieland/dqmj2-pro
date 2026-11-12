/* Increment byte 0x26 of the 0x020f69c4 block and return the new value.
   Unknowns: the block role and why the counter increments. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

extern u8 native_data_020f69c4[];
u32 native_main_0204448c(void) {
    u8 *p = native_data_020f69c4;
    u32 v = (u32)p[0x26] + 1;
    p[0x26] = (u8)v;
    return v & 0xff;
}