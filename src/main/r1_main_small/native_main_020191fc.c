/* Return the one-bit flag stored in byte 5 of the 0x027ffc30 block.
   Unknowns: the block owner and what the flag gates. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

typedef struct { u8 pad[5]; u8 flag : 1; } T;
extern u8 native_data_027ffc30[];
u32 native_main_020191fc(void) {
    return ((T *)native_data_027ffc30)->flag;
}