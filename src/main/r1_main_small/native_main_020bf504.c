/* Halfword table read with a two-byte stride from 0x020e2cb0.
   Unknowns: the table contents and the index domain. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

extern u8 native_data_020e2cb0[];
u32 native_main_020bf504(u32 index) {
    return M2C_FIELD(native_data_020e2cb0, u16 *, index * 2);
}