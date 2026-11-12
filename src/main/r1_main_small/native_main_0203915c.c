/* Publish two recorded words from the object reached through 0x020f4c44.
   Unknowns: the record layout at +0x7c/+0x80 and the output owner. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

extern u8 native_data_020f4c44[];
void native_main_0203915c(u32 *out) {
    u8 *p = *(u8 **)native_data_020f4c44;
    u32 a = M2C_FIELD(p, volatile u32 *, 0x7c);
    u32 b = M2C_FIELD(p, volatile u32 *, 0x80);
    out[0] = a;
    out[1] = b;
}