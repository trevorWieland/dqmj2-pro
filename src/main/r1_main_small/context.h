#ifndef R1_MAIN_SMALL_CONTEXT_H
#define R1_MAIN_SMALL_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Byte-offset field access on a measured global block. The pool word stays the
   block base address, so the field offset shows up in the instruction — which is
   what the image holds; folding base+offset into one literal does not match. */
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

#endif
