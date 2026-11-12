/* Read a word from a record, or an indexed word through the caller pointer.
   Unknowns: the record layout and the null-pointer contract. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

u32 native_main_0202bba0(u8 *p, u8 *q) {
    if (q == 0)
        return M2C_FIELD(p, u32 *, 4);
    return *(u32 *)(q + M2C_FIELD(p, u16 *, 0xa));
}