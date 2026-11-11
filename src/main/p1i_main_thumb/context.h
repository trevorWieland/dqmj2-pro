#ifndef P1I_CONTEXT_H
#define P1I_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Mechanism index shared by the Thumb helper batch: records here expose their
   payload slot through +0x0c, the event mask through +0x08, and dispatch a
   thunk through the first word.  Mechanism indices for the call sites are in
   each file's comment (BL = Thumb callee, BLX = ARM callee). */

#endif
