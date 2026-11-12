/* Spin until the word at 0x020edf84+4 becomes zero.
   Unknowns: which producer clears the word and the timeout contract. */
#include "context.h"
#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H


/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */

#endif

extern u8 native_data_020edf84[];
void native_main_0202e35c(void) {
    while (M2C_FIELD(native_data_020edf84, volatile u32 *, 4) != 0) {
    }
}