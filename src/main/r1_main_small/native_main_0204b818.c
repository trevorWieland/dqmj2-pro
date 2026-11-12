/* Tail-call a helper with two byte-truncated arguments.
   Unknowns: the callee role and why only the low bytes survive. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

extern u32 native_fn_02063e04(u32, u32);
u32 native_main_0204b818(u32 a, u32 b) {
    return native_fn_02063e04((u8)a, (u8)b);
}