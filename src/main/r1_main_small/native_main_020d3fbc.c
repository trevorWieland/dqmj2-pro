/* Tail-call a helper with the constant 0x2a and a byte-truncated argument.
   Unknowns: the callee role and the constant meaning. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

extern u32 native_fn_0203d0c0(u32, u32);
u32 native_main_020d3fbc(u32 value) {
    return native_fn_0203d0c0(0x2a, (u8)value);
}