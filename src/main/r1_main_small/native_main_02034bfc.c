/* Pop one byte through a caller cursor and advance it by one byte.
   Unknowns: the stream format and the cursor owner. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

u32 native_main_02034bfc(u8 **cursor) {
    u8 *p = *cursor;
    u8 value = *p++;
    *cursor = p;
    return value;
}