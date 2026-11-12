/* Pop one halfword through a caller cursor and advance it by two bytes.
   Unknowns: the stream format and the cursor owner. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

u32 native_main_02034b18(u16 **cursor) {
    u16 *p = *cursor;
    u16 value = *p++;
    *cursor = p;
    return value;
}