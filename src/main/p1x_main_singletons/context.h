#ifndef P1X_CONTEXT_H
#define P1X_CONTEXT_H

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

/* Mechanism index for the main-module singletons:
   - 0x020b4108: consumer of the record tagged at +2 (tail call);
   - 0x02096ffc: consumer of the object word at +0x24 (tail call);
   - 0x020e33e4 + 4: word forwarded to the ARM routine 0x02006acc for small
     indices (< 0x20). */

#endif
