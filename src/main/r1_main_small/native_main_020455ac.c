/* Set bit N of a global halfword, where N is the caller selector.
   Unknowns: the block role, the selector domain and the halfword owner. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

extern u8 native_data_020f6ae4[];
void native_main_020455ac(u32 bit) {
    u32 old = M2C_FIELD(native_data_020f6ae4, u16 *, 0);
    u32 value = old | (1 << bit);
    M2C_FIELD(native_data_020f6ae4, u16 *, 0) = value;
}